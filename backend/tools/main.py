"""
Tools Service - Microservice tính toán tài chính (Serverless, Cloud Run).

Cung cấp: tính lãi đơn/ghép, tỷ lệ tiết kiệm so với thu nhập.
Chatbot gọi qua HTTP khi cần.
"""

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from routers import interest, savings_rate


class ErrorBody(BaseModel):
    """Định dạng body lỗi thống nhất."""

    code: str
    message: str
    details: dict[str, Any] | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle: startup/shutdown."""
    yield


app = FastAPI(
    title="Chatbot Tools API",
    description="Công cụ tính toán tài chính cho Chatbot (lãi, tỷ lệ tiết kiệm)",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(interest.router, prefix="/tools", tags=["tools"])
app.include_router(savings_rate.router, prefix="/tools", tags=["tools"])


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check cho Cloud Run."""
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> dict[str, str]:
    """Readiness check."""
    return {"status": "ready"}
