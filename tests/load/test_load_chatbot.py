"""
Load test Chatbot API – pytest.

Gửi nhiều request đồng thời: health, create session, chat (cần Chatbot + Tools chạy; chat gọi LLM nên chậm).
Chạy: CHATBOT_URL=http://localhost:8080 pytest tests/load/test_load_chatbot.py -v -s
"""

import os
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest
import httpx

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8080").rstrip("/")
NUM_REQUESTS = int(os.getenv("LOAD_NUM_REQUESTS", "20"))
NUM_WORKERS = int(os.getenv("LOAD_NUM_WORKERS", "5"))
TIMEOUT = 60.0  # chat có thể chậm do LLM


def _get_health() -> tuple[float, int]:
    start = time.perf_counter()
    r = httpx.get(f"{CHATBOT_URL}/health", timeout=10.0)
    elapsed = time.perf_counter() - start
    return elapsed, r.status_code


def _post_sessions() -> tuple[float, int]:
    start = time.perf_counter()
    r = httpx.post(f"{CHATBOT_URL}/api/sessions", timeout=10.0)
    elapsed = time.perf_counter() - start
    return elapsed, r.status_code


def _post_chat(session_id: str) -> tuple[float, int]:
    start = time.perf_counter()
    r = httpx.post(
        f"{CHATBOT_URL}/api/chat",
        json={"session_id": session_id, "message": "Lãi suất tiết kiệm 1 năm?"},
        timeout=TIMEOUT,
    )
    elapsed = time.perf_counter() - start
    return elapsed, r.status_code


@pytest.mark.skipif(
    os.getenv("SKIP_LOAD_TEST") == "1",
    reason="Bỏ qua load test",
)
def test_load_chatbot_health() -> None:
    """Nhiều request GET /health đồng thời."""
    latencies = []
    codes = []
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as ex:
        futures = [ex.submit(_get_health) for _ in range(NUM_REQUESTS)]
        for f in as_completed(futures):
            elapsed, code = f.result()
            latencies.append(elapsed)
            codes.append(code)
    ok = sum(1 for c in codes if c == 200)
    avg_ms = (sum(latencies) / len(latencies)) * 1000
    rps = NUM_REQUESTS / sum(latencies) if latencies else 0
    print(f"\n[Chatbot /health] requests={NUM_REQUESTS}, ok={ok}, avg_ms={avg_ms:.1f}, rps={rps:.1f}")
    assert ok == NUM_REQUESTS


@pytest.mark.skipif(
    os.getenv("SKIP_LOAD_TEST") == "1",
    reason="Bỏ qua load test",
)
def test_load_chatbot_sessions() -> None:
    """Nhiều request POST /api/sessions đồng thời."""
    latencies = []
    codes = []
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as ex:
        futures = [ex.submit(_post_sessions) for _ in range(NUM_REQUESTS)]
        for f in as_completed(futures):
            elapsed, code = f.result()
            latencies.append(elapsed)
            codes.append(code)
    ok = sum(1 for c in codes if c == 201)
    avg_ms = (sum(latencies) / len(latencies)) * 1000
    rps = NUM_REQUESTS / sum(latencies) if latencies else 0
    print(f"\n[Chatbot /api/sessions] requests={NUM_REQUESTS}, ok={ok}, avg_ms={avg_ms:.1f}, rps={rps:.1f}")
    assert ok == NUM_REQUESTS


@pytest.mark.skipif(
    os.getenv("SKIP_LOAD_TEST") == "1",
    reason="Bỏ qua load test",
)
def test_load_chatbot_chat() -> None:
    """Nhiều request POST /api/chat đồng thời (mỗi request dùng session riêng)."""
    session_ids = [f"sess_{uuid.uuid4().hex[:16]}" for _ in range(min(NUM_REQUESTS, 10))]
    latencies = []
    codes = []
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as ex:
        futures = [
            ex.submit(_post_chat, session_ids[i % len(session_ids)])
            for i in range(NUM_REQUESTS)
        ]
        for f in as_completed(futures):
            elapsed, code = f.result()
            latencies.append(elapsed)
            codes.append(code)
    ok = sum(1 for c in codes if c == 200)
    avg_ms = (sum(latencies) / len(latencies)) * 1000
    total_time = sum(latencies)
    rps = NUM_REQUESTS / total_time if total_time > 0 else 0
    print(f"\n[Chatbot /api/chat] requests={NUM_REQUESTS}, ok={ok}, avg_ms={avg_ms:.1f}, rps={rps:.2f}")
    assert ok >= NUM_REQUESTS - 2, f"Too many failures: {codes}"  # cho phép 1–2 lỗi do timeout/rate limit
