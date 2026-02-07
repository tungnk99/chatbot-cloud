"""Pydantic schemas cho Chatbot API."""

from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """POST /api/chat body."""

    session_id: str = Field(..., min_length=1, max_length=128)
    message: str = Field(..., min_length=1, max_length=4096)


class ToolCallItem(BaseModel):
    """Một tool call trong response."""

    tool: str
    input: dict[str, Any]
    output: dict[str, Any]


class ChatResponse(BaseModel):
    """Response POST /api/chat."""

    session_id: str
    message_id: str
    content: str
    tool_calls: list[ToolCallItem] = Field(default_factory=list)
    # Khi async=1: status="pending", content rỗng; client poll GET messages để lấy kết quả
    status: str = "completed"  # "completed" | "pending"


class MessageItem(BaseModel):
    """Một message trong GET sessions/messages."""

    message_id: str
    role: str
    content: str
    created_at: str
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)


class GetMessagesResponse(BaseModel):
    """GET /api/sessions/{id}/messages."""

    session_id: str
    messages: list[MessageItem]


class CreateSessionResponse(BaseModel):
    """POST /api/sessions."""

    session_id: str
    created_at: str


class SessionListItem(BaseModel):
    """Một phiên trong danh sách GET /api/sessions."""

    session_id: str
    updated_at: str


class ListSessionsResponse(BaseModel):
    """GET /api/sessions."""

    sessions: list[SessionListItem]
