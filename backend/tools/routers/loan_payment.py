"""
Router: Tính khoản trả góp hàng tháng cho khoản vay.

POST /tools/loan-payment
"""

import logging

from fastapi import APIRouter, HTTPException

from .schemas import LoanPaymentRequest, LoanPaymentResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/loan-payment", response_model=LoanPaymentResponse)
def calculate_loan_payment(body: LoanPaymentRequest) -> LoanPaymentResponse:
    """
    Tính khoản trả góp hàng tháng theo công thức amortization.

    Args:
        body: principal, annual_rate, months.

    Returns:
        monthly_payment, total_payment, total_interest.

    Raises:
        HTTPException: 400 khi input không hợp lệ.
    """
    principal = body.principal
    annual_rate = body.annual_rate
    months = body.months
    
    logger.info("🏦 [Loan Payment] ===== REQUEST START =====")
    logger.info("🏦 [Loan Payment] INPUT: principal=%.2f, annual_rate=%.2f%%, months=%d",
                principal, annual_rate, months)

    if principal <= 0 or annual_rate < 0 or months <= 0:
        logger.warning("⚠️  [Loan Payment] Invalid input: principal=%s, rate=%s, months=%s",
                      principal, annual_rate, months)
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_INPUT",
                "message": "principal, annual_rate, months must be positive",
            },
        )

    # Tính khoản trả hàng tháng theo công thức amortization
    # M = P * [r(1+r)^n] / [(1+r)^n - 1]
    if annual_rate == 0:
        # Không có lãi suất
        monthly_payment = principal / months
    else:
        monthly_rate = (annual_rate / 100.0) / 12.0
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / \
                         ((1 + monthly_rate) ** months - 1)

    total_payment = monthly_payment * months
    total_interest = total_payment - principal
    
    result = LoanPaymentResponse(
        principal=principal,
        monthly_payment=round(monthly_payment, 2),
        total_payment=round(total_payment, 2),
        total_interest=round(total_interest, 2),
        annual_rate=annual_rate,
        months=months,
    )
    
    logger.info("✅ [Loan Payment] OUTPUT: monthly_payment=%.2f, total_payment=%.2f, interest=%.2f",
                result.monthly_payment, result.total_payment, result.total_interest)
    logger.info("✅ [Loan Payment] ===== REQUEST END =====")
    
    return result
