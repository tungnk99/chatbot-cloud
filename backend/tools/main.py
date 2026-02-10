"""
Tools Service - Microservice tính toán tài chính (Serverless, Cloud Run).

Cung cấp: tính lãi đơn/ghép, tỷ lệ tiết kiệm so với thu nhập.
Chatbot gọi qua HTTP khi cần.
"""

import logging
import sys
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from routers import (
    interest, 
    savings_rate, 
    loan_payment, 
    investment_return, 
    budget_breakdown, 
    currency_convert, 
    emergency_fund
)

# Configure logging with format
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


class ErrorBody(BaseModel):
    """Định dạng body lỗi thống nhất."""

    code: str
    message: str
    details: dict[str, Any] | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle: startup/shutdown."""
    logger.info("🚀 Tools Service starting up...")
    yield
    logger.info("🛑 Tools Service shutting down...")


app = FastAPI(
    title="Chatbot Tools API",
    description="Công cụ tính toán tài chính cho Chatbot",
    version="2.0.0",
    lifespan=lifespan,
)

# Include các routers
app.include_router(interest.router, prefix="/tools", tags=["tools"])
app.include_router(savings_rate.router, prefix="/tools", tags=["tools"])
app.include_router(loan_payment.router, prefix="/tools", tags=["tools"])
app.include_router(investment_return.router, prefix="/tools", tags=["tools"])
app.include_router(budget_breakdown.router, prefix="/tools", tags=["tools"])
app.include_router(currency_convert.router, prefix="/tools", tags=["tools"])
app.include_router(emergency_fund.router, prefix="/tools", tags=["tools"])


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check cho Cloud Run."""
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> dict[str, str]:
    """Readiness check."""
    return {"status": "ready"}
