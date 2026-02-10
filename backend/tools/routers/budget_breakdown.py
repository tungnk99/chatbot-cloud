"""
Router: Phân tích ngân sách theo quy tắc 50/30/20.

POST /tools/budget-breakdown
"""

import logging

from fastapi import APIRouter, HTTPException

from .schemas import BudgetBreakdownRequest, BudgetBreakdownResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/budget-breakdown", response_model=BudgetBreakdownResponse)
def calculate_budget_breakdown(body: BudgetBreakdownRequest) -> BudgetBreakdownResponse:
    """
    Phân tích ngân sách theo quy tắc 50/30/20.
    - 50% cho nhu cầu thiết yếu (nhà ở, ăn uống, đi lại, bảo hiểm)
    - 30% cho mong muốn (giải trí, du lịch, sở thích)
    - 20% cho tiết kiệm và đầu tư

    Args:
        body: monthly_income.

    Returns:
        needs (50%), wants (30%), savings (20%).

    Raises:
        HTTPException: 400 khi input không hợp lệ.
    """
    monthly_income = body.monthly_income
    
    logger.info("💼 [Budget Breakdown] ===== REQUEST START =====")
    logger.info("💼 [Budget Breakdown] INPUT: monthly_income=%.2f", monthly_income)

    if monthly_income <= 0:
        logger.warning("⚠️  [Budget Breakdown] Invalid income: %.2f", monthly_income)
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_INPUT",
                "message": "monthly_income must be positive",
            },
        )

    needs = monthly_income * 0.50
    wants = monthly_income * 0.30
    savings = monthly_income * 0.20
    
    suggestion = (
        f"Theo quy tắc 50/30/20: dành {needs:,.0f} VNĐ cho nhu cầu thiết yếu, "
        f"{wants:,.0f} VNĐ cho mong muốn, và {savings:,.0f} VNĐ cho tiết kiệm."
    )
    
    result = BudgetBreakdownResponse(
        monthly_income=monthly_income,
        needs=round(needs, 2),
        wants=round(wants, 2),
        savings=round(savings, 2),
        suggestion=suggestion,
    )
    
    logger.info("✅ [Budget Breakdown] OUTPUT: needs=%.2f (50%%), wants=%.2f (30%%), savings=%.2f (20%%)",
                result.needs, result.wants, result.savings)
    logger.info("✅ [Budget Breakdown] ===== REQUEST END =====")
    
    return result
