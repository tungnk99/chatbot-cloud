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


class LoanPaymentRequest(BaseModel):
    """Request tính khoản trả góp."""

    principal: float = Field(..., gt=0, description="Số tiền vay")
    annual_rate: float = Field(..., ge=0, description="Lãi suất %/năm")
    months: int = Field(..., gt=0, description="Số tháng trả góp")


class LoanPaymentResponse(BaseModel):
    """Response tính khoản trả góp."""

    principal: float
    monthly_payment: float
    total_payment: float
    total_interest: float
    annual_rate: float
    months: int


class InvestmentReturnRequest(BaseModel):
    """Request tính lợi nhuận đầu tư."""

    initial_amount: float = Field(..., ge=0, description="Số tiền ban đầu")
    monthly_contribution: float = Field(..., ge=0, description="Đóng góp hàng tháng")
    annual_return: float = Field(..., description="Lợi nhuận %/năm")
    years: float = Field(..., gt=0, description="Số năm đầu tư")


class InvestmentReturnResponse(BaseModel):
    """Response tính lợi nhuận đầu tư."""

    initial_amount: float
    monthly_contribution: float
    total_contributed: float
    final_value: float
    total_return: float
    annual_return: float
    years: float


class BudgetBreakdownRequest(BaseModel):
    """Request phân tích ngân sách."""

    monthly_income: float = Field(..., gt=0, description="Thu nhập hàng tháng")


class BudgetBreakdownResponse(BaseModel):
    """Response phân tích ngân sách theo quy tắc 50/30/20."""

    monthly_income: float
    needs: float  # 50% - nhu cầu thiết yếu
    wants: float  # 30% - mong muốn
    savings: float  # 20% - tiết kiệm
    suggestion: str


class CurrencyConvertRequest(BaseModel):
    """Request chuyển đổi tiền tệ."""

    amount: float = Field(..., gt=0, description="Số tiền")
    from_currency: str = Field(..., description="Mã tiền tệ nguồn (VND, USD, EUR, ...)")
    to_currency: str = Field(..., description="Mã tiền tệ đích (VND, USD, EUR, ...)")


class CurrencyConvertResponse(BaseModel):
    """Response chuyển đổi tiền tệ."""

    amount: float
    from_currency: str
    to_currency: str
    converted_amount: float
    exchange_rate: float


class EmergencyFundRequest(BaseModel):
    """Request tính quỹ dự phòng."""

    monthly_expenses: float = Field(..., gt=0, description="Chi tiêu hàng tháng")
    months_coverage: int = Field(6, ge=3, le=12, description="Số tháng dự phòng (3-12)")


class EmergencyFundResponse(BaseModel):
    """Response tính quỹ dự phòng."""

    monthly_expenses: float
    months_coverage: int
    target_amount: float
    suggestion: str
