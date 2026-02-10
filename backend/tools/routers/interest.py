"""
Router: Tính lãi đơn / lãi kép.

POST /tools/interest
"""

import logging

from fastapi import APIRouter, HTTPException

from .schemas import InterestRequest, InterestResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/interest", response_model=InterestResponse)
def calculate_interest(body: InterestRequest) -> InterestResponse:
    """
    Tính lãi đơn hoặc lãi kép.

    Args:
        body: principal, rate_percent, months, compound.

    Returns:
        interest, total, và các tham số đã dùng.

    Raises:
        HTTPException: 400 khi input không hợp lệ.
    """
    principal = body.principal
    rate_percent = body.rate_percent
    months = body.months
    compound = body.compound
    
    logger.info("💰 [Interest Calculator] ===== REQUEST START =====")
    logger.info("💰 [Interest Calculator] INPUT: principal=%.2f, rate=%.2f%%, months=%.1f, compound=%s",
                principal, rate_percent, months, compound)

    if principal <= 0 or rate_percent < 0 or months <= 0:
        logger.warning("⚠️  [Interest Calculator] Invalid input: principal=%s, rate=%s, months=%s",
                      principal, rate_percent, months)
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_INPUT",
                "message": "principal, rate_percent, months must be positive",
            },
        )

    rate_decimal = rate_percent / 100.0
    years = months / 12.0

    if compound:
        # Lãi kép: A = P * (1 + r)^t
        total = principal * ((1 + rate_decimal) ** years)
    else:
        # Lãi đơn: I = P * r * t, total = P + I
        interest_amount = principal * rate_decimal * years
        total = principal + interest_amount

    interest_amount = total - principal
    
    result = InterestResponse(
        principal=principal,
        interest=round(interest_amount, 2),
        total=round(total, 2),
        rate_percent=rate_percent,
        months=months,
        compound=compound,
    )
    
    logger.info("✅ [Interest Calculator] OUTPUT: interest=%.2f, total=%.2f, principal=%.2f",
                result.interest, result.total, result.principal)
    logger.info("✅ [Interest Calculator] ===== REQUEST END ===== (method=%s)",
                "compound" if compound else "simple")
    
    return result
