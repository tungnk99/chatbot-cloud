"""
Chatbot Service - Điều phối LLM, Tools, Storage (Cloud Run).

API: POST /api/chat, GET /api/sessions/{id}/messages, POST /api/sessions,
     POST /api/pubsub/chat-handler (nhận push từ Pub/Sub), GET /health.
"""

import asyncio
import base64
import json
import logging
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from schemas import (
    ChatRequest,
    ChatResponse,
    CreateSessionResponse,
    GetMessagesResponse,
    MessageItem,
    ToolCallItem,
)
from services.llm_client import LLMClient
from services.pubsub_client import publish_chat_request
from services.tools_client import ToolsClient
from storage import LocalStorage, MessageRecord, SessionData, Storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Globals (injected in lifespan)
storage: Storage
llm_client: LLMClient
tools_client: ToolsClient


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _create_storage() -> Storage:
    """Tạo storage theo cấu hình (local hoặc gcs)."""
    if settings.storage_backend == "gcs" and settings.gcs_bucket:
        try:
            from storage import GCSStorage
            if GCSStorage:
                return GCSStorage(bucket_name=settings.gcs_bucket, prefix="chat/sessions")
        except Exception as e:
            logger.warning("GCS storage init failed, fallback to local: %s", e)
    return LocalStorage(base_path=settings.local_storage_path)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Khởi tạo storage, LLM client, Tools client."""
    global storage, llm_client, tools_client
    storage = _create_storage()
    llm_client = LLMClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )
    tools_client = ToolsClient(base_url=settings.tools_base_url)
    yield


app = FastAPI(
    title="Chatbot API",
    description="Chatbot tài chính - gọi LLM và Tools",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS (AGENT: allow_origins cụ thể)
_origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Rate limiting in-memory cho /api/chat (AGENT: rate limiting endpoint public)
_rate_limit: dict[str, list[float]] = {}
_RATE_WINDOW = 60.0  # giây


def _check_rate_limit(client_key: str) -> None:
    if settings.rate_limit_per_minute <= 0:
        return
    now = time.time()
    if client_key not in _rate_limit:
        _rate_limit[client_key] = []
    times = _rate_limit[client_key]
    times[:] = [t for t in times if now - t < _RATE_WINDOW]
    if len(times) >= settings.rate_limit_per_minute:
        raise HTTPException(status_code=429, detail={"code": "RATE_LIMIT", "message": "Too many requests"})
    times.append(now)


def _session_messages_to_openai(session_data: Any) -> list[dict[str, str]]:
    """Chuyển messages trong session sang format OpenAI (role, content)."""
    out = []
    for m in session_data.messages:
        out.append({"role": m.role, "content": m.content})
    return out


@app.post(f"{settings.api_prefix}/chat", response_model=ChatResponse)
async def chat(
    request: Request,
    body: ChatRequest,
    async_mode: bool = Query(False, alias="async"),  # ?async=1 để xử lý bất đồng bộ qua Pub/Sub
) -> ChatResponse:
    """
    Gửi tin nhắn user. Mặc định xử lý đồng bộ.
    Nếu async_mode=1 (query) và bật Pub/Sub: đẩy vào hàng đợi, trả về pending; client poll GET messages.
    """
    client_key = request.client.host if request.client else "unknown"
    _check_rate_limit(client_key)
    session_id = body.session_id.strip()
    message_text = body.message.strip()
    if not session_id or not message_text:
        raise HTTPException(
            status_code=400,
            detail={"code": "INVALID_INPUT", "message": "session_id and message are required"},
        )

    user_msg_id = f"msg_{uuid.uuid4().hex[:12]}"
    user_msg = MessageRecord(
        message_id=user_msg_id,
        role="user",
        content=message_text,
        created_at=_now_iso(),
        tool_calls=[],
    )
    storage.append_message(session_id, user_msg)

    if async_mode and settings.use_pubsub_async and settings.pubsub_topic:
        ok = await asyncio.to_thread(
            publish_chat_request,
            settings.pubsub_topic,
            {"session_id": session_id, "message": message_text, "user_msg_id": user_msg_id},
        )
        if ok:
            return ChatResponse(
                session_id=session_id,
                message_id=user_msg_id,
                content="",
                tool_calls=[],
                status="pending",
            )
        logger.warning("Pub/Sub publish failed, fallback to sync")

    # Đồng bộ hoặc Pub/Sub không khả dụng
    session_data = storage.get_session(session_id)
    messages_for_llm = _session_messages_to_openai(session_data)
    content, tool_calls_made = await llm_client.chat_with_tools(
        messages=messages_for_llm,
        tools_client=tools_client,
    )
    assistant_msg_id = f"msg_{uuid.uuid4().hex[:12]}"
    tool_items = [
        ToolCallItem(tool=t["tool"], input=t["input"], output=t["output"])
        for t in tool_calls_made
    ]
    assistant_msg = MessageRecord(
        message_id=assistant_msg_id,
        role="assistant",
        content=content,
        created_at=_now_iso(),
        tool_calls=[{"tool": t.tool, "input": t.input, "output": t.output} for t in tool_items],
    )
    storage.append_message(session_id, assistant_msg)
    return ChatResponse(
        session_id=session_id,
        message_id=assistant_msg_id,
        content=content,
        tool_calls=tool_items,
        status="completed",
    )


@app.post(f"{settings.api_prefix}/pubsub/chat-handler")
async def pubsub_chat_handler(request: Request) -> dict[str, str]:
    """
    Nhận push từ Pub/Sub: decode message, gọi LLM, lưu assistant message.
    Trả về 200 để ack message (tránh retry).
    """
    try:
        envelope = await request.json()
        message = envelope.get("message", {})
        data_b64 = message.get("data")
        if not data_b64:
            logger.warning("Pub/Sub push missing message.data")
            return {"status": "ok"}
        data = base64.b64decode(data_b64).decode("utf-8")
        payload = json.loads(data)
        session_id = payload.get("session_id", "").strip()
        message_text = payload.get("message", "").strip()
        if not session_id or not message_text:
            logger.warning("Pub/Sub payload missing session_id or message")
            return {"status": "ok"}
        session_data = storage.get_session(session_id)
        if not session_data:
            logger.warning("Session not found: %s", session_id)
            return {"status": "ok"}
        messages_for_llm = _session_messages_to_openai(session_data)
        content, tool_calls_made = await llm_client.chat_with_tools(
            messages=messages_for_llm,
            tools_client=tools_client,
        )
        assistant_msg_id = f"msg_{uuid.uuid4().hex[:12]}"
        tool_items = [
            ToolCallItem(tool=t["tool"], input=t["input"], output=t["output"])
            for t in tool_calls_made
        ]
        assistant_msg = MessageRecord(
            message_id=assistant_msg_id,
            role="assistant",
            content=content,
            created_at=_now_iso(),
            tool_calls=[{"tool": t.tool, "input": t.input, "output": t.output} for t in tool_items],
        )
        storage.append_message(session_id, assistant_msg)
        logger.info("Pub/Sub chat handled: session_id=%s message_id=%s", session_id, assistant_msg_id)
    except Exception as e:
        logger.exception("Pub/Sub chat handler error: %s", e)
        raise HTTPException(status_code=500, detail="Handler failed")
    return {"status": "ok"}


@app.get(
    f"{settings.api_prefix}/sessions/{{session_id}}/messages",
    response_model=GetMessagesResponse,
)
async def get_messages(session_id: str) -> GetMessagesResponse:
    """Lấy lịch sử tin nhắn trong session."""
    session_data = storage.get_session(session_id)
    if session_data is None or not session_data.messages:
        raise HTTPException(
            status_code=404,
            detail={"code": "NOT_FOUND", "message": "Session not found or no messages"},
        )
    return GetMessagesResponse(
        session_id=session_id,
        messages=[
            MessageItem(
                message_id=m.message_id,
                role=m.role,
                content=m.content,
                created_at=m.created_at,
                tool_calls=m.tool_calls,
            )
            for m in session_data.messages
        ],
    )


@app.post(f"{settings.api_prefix}/sessions", response_model=CreateSessionResponse)
async def create_session() -> CreateSessionResponse:
    """Tạo session mới."""
    session_id = f"sess_{uuid.uuid4().hex[:16]}"
    now = _now_iso()
    storage.save_session(
        SessionData(
            session_id=session_id,
            created_at=now,
            updated_at=now,
            messages=[],
        )
    )
    return CreateSessionResponse(session_id=session_id, created_at=now)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check cho Cloud Run."""
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> dict[str, str]:
    """Readiness check."""
    return {"status": "ready"}
