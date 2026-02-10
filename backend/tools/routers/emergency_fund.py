"""
Router: Tính quỹ dự phòng khẩn cấp.

POST /tools/emergency-fund
"""

import logging

from fastapi import APIRouter, HTTPException

from .schemas import EmergencyFundRequest, EmergencyFundResponse

logger = logging.getLogger(__name__)
router = APIRouter()

SUGGESTIONS = {
    3: "Quỹ dự phòng 3 tháng là mức tối thiểu. Nên nâng lên 6 tháng để an toàn hơn.",
    6: "Quỹ dự phòng 6 tháng là mức được khuyến nghị cho hầu hết mọi người.",
    12: "Quỹ dự phòng 12 tháng rất tốt, đặc biệt cho người làm tự do hoặc thu nhập không ổn định.",
}


@router.post("/emergency-fund", response_model=EmergencyFundResponse)
def calculate_emergency_fund(body: EmergencyFundRequest) -> EmergencyFundResponse:
    """
    Tính số tiền cần cho quỹ dự phòng khẩn cấp.

    Args:
        body: monthly_expenses, months_coverage (3-12 tháng).

    Returns:
        target_amount và gợi ý.

    Raises:
        HTTPException: 400 khi input không hợp lệ.
    """
    monthly_expenses = body.monthly_expenses
    months_coverage = body.months_coverage
    
    logger.info("🆘 [Emergency Fund] ===== REQUEST START =====")
    logger.info("🆘 [Emergency Fund] INPUT: monthly_expenses=%.2f, months=%d",
                monthly_expenses, months_coverage)

    if monthly_expenses <= 0:
        logger.warning("⚠️  [Emergency Fund] Invalid expenses: %.2f", monthly_expenses)
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_INPUT",
                "message": "monthly_expenses must be positive",
            },
        )

    if not (3 <= months_coverage <= 12):
        logger.warning("⚠️  [Emergency Fund] Invalid coverage months: %d", months_coverage)
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_INPUT",
                "message": "months_coverage must be between 3 and 12",
            },
        )

    target_amount = monthly_expenses * months_coverage
    
    # Chọn gợi ý phù hợp
    if months_coverage <= 3:
        suggestion = SUGGESTIONS[3]
    elif months_coverage <= 6:
        suggestion = SUGGESTIONS[6]
    else:
        suggestion = SUGGESTIONS[12]
    
    result = EmergencyFundResponse(
        monthly_expenses=monthly_expenses,
        months_coverage=months_coverage,
        target_amount=round(target_amount, 2),
        suggestion=suggestion,
    )
    
    logger.info("✅ [Emergency Fund] OUTPUT: target_amount=%.2f for %d months",
                result.target_amount, months_coverage)
    logger.info("✅ [Emergency Fund] SUGGESTION: %s", suggestion)
    logger.info("✅ [Emergency Fund] ===== REQUEST END =====")
    
    return result
