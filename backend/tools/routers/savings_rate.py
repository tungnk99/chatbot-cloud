"""
Router: Tính tỷ lệ tiết kiệm so với thu nhập.

POST /tools/savings-rate
"""

import logging

from fastapi import APIRouter, HTTPException

from .schemas import SavingsRateRequest, SavingsRateResponse

logger = logging.getLogger(__name__)
router = APIRouter()

SUGGESTIONS = [
    "Tỷ lệ tiết kiệm dưới 10% – nên cố gắng tăng dần để có quỹ dự phòng.",
    "Tỷ lệ tiết kiệm 10–20% thu nhập là mức tốt, thường được khuyến nghị.",
    "Tỷ lệ tiết kiệm trên 20% – rất tốt cho tích lũy dài hạn.",
]


@router.post("/savings-rate", response_model=SavingsRateResponse)
def calculate_savings_rate(body: SavingsRateRequest) -> SavingsRateResponse:
    """
    Tính tỷ lệ % tiết kiệm so với thu nhập và gợi ý ngắn.

    Args:
        body: income, savings.

    Returns:
        savings_rate_percent và suggestion.

    Raises:
        HTTPException: 400 khi input không hợp lệ.
    """
    income = body.income
    savings = body.savings
    
    logger.info("📊 [Savings Rate] ===== REQUEST START =====")
    logger.info("📊 [Savings Rate] INPUT: income=%.2f, savings=%.2f", 
                income, savings)

    if income <= 0:
        logger.warning("⚠️  [Savings Rate] Invalid income: %.2f", income)
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_INPUT",
                "message": "income must be positive",
            },
        )
    if savings < 0:
        logger.warning("⚠️  [Savings Rate] Invalid savings: %.2f", savings)
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_INPUT",
                "message": "savings must be non-negative",
            },
        )

    rate = (savings / income) * 100.0

    if rate < 10:
        suggestion = SUGGESTIONS[0]
    elif rate <= 20:
        suggestion = SUGGESTIONS[1]
    else:
        suggestion = SUGGESTIONS[2]
    
    result = SavingsRateResponse(
        income=income,
        savings=savings,
        savings_rate_percent=round(rate, 2),
        suggestion=suggestion,
    )
    
    logger.info("✅ [Savings Rate] OUTPUT: rate=%.2f%%, income=%.2f, savings=%.2f",
                result.savings_rate_percent, income, savings)
    logger.info("✅ [Savings Rate] SUGGESTION: %s", suggestion)
    logger.info("✅ [Savings Rate] ===== REQUEST END =====")
    
    return result
