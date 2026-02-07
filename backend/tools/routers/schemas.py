"""Pydantic schemas cho Tools API."""

from pydantic import BaseModel, Field


class InterestRequest(BaseModel):
    """Request tính lãi."""

    principal: float = Field(..., gt=0, description="Số tiền gốc")
    rate_percent: float = Field(..., ge=0, description="Lãi suất %/năm")
    months: float = Field(..., gt=0, description="Kỳ hạn (tháng)")
    compound: bool = Field(False, description="True = lãi kép, False = lãi đơn")


class InterestResponse(BaseModel):
    """Response tính lãi."""

    principal: float
    interest: float
    total: float
    rate_percent: float
    months: float
    compound: bool


class SavingsRateRequest(BaseModel):
    """Request tỷ lệ tiết kiệm."""

    income: float = Field(..., gt=0, description="Thu nhập")
    savings: float = Field(..., ge=0, description="Số tiền tiết kiệm")


class SavingsRateResponse(BaseModel):
    """Response tỷ lệ tiết kiệm."""

    income: float
    savings: float
    savings_rate_percent: float
    suggestion: str
