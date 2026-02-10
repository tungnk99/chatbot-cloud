"""
Router: Tính lợi nhuận đầu tư với đóng góp định kỳ.

POST /tools/investment-return
"""

import logging

from fastapi import APIRouter, HTTPException

from .schemas import InvestmentReturnRequest, InvestmentReturnResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/investment-return", response_model=InvestmentReturnResponse)
def calculate_investment_return(body: InvestmentReturnRequest) -> InvestmentReturnResponse:
    """
    Tính lợi nhuận đầu tư với đóng góp hàng tháng.

    Args:
        body: initial_amount, monthly_contribution, annual_return, years.

    Returns:
        final_value, total_return, total_contributed.

    Raises:
        HTTPException: 400 khi input không hợp lệ.
    """
    initial_amount = body.initial_amount
    monthly_contribution = body.monthly_contribution
    annual_return = body.annual_return
    years = body.years
    
    logger.info("📈 [Investment Return] ===== REQUEST START =====")
    logger.info("📈 [Investment Return] INPUT: initial=%.2f, monthly=%.2f, return=%.2f%%, years=%.1f",
                initial_amount, monthly_contribution, annual_return, years)

    if initial_amount < 0 or monthly_contribution < 0 or years <= 0:
        logger.warning("⚠️  [Investment Return] Invalid input")
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_INPUT",
                "message": "initial_amount, monthly_contribution must be non-negative, years must be positive",
            },
        )

    monthly_rate = (annual_return / 100.0) / 12.0
    total_months = int(years * 12)
    
    # Tính giá trị tương lai với đóng góp hàng tháng
    # FV = P(1+r)^n + PMT * [((1+r)^n - 1) / r]
    if annual_return == 0:
        final_value = initial_amount + (monthly_contribution * total_months)
    else:
        # Giá trị của số tiền ban đầu sau n tháng
        fv_initial = initial_amount * ((1 + monthly_rate) ** total_months)
        
        # Giá trị của các khoản đóng góp hàng tháng
        fv_contributions = monthly_contribution * (((1 + monthly_rate) ** total_months - 1) / monthly_rate)
        
        final_value = fv_initial + fv_contributions
    
    total_contributed = initial_amount + (monthly_contribution * total_months)
    total_return = final_value - total_contributed
    
    result = InvestmentReturnResponse(
        initial_amount=initial_amount,
        monthly_contribution=monthly_contribution,
        total_contributed=round(total_contributed, 2),
        final_value=round(final_value, 2),
        total_return=round(total_return, 2),
        annual_return=annual_return,
        years=years,
    )
    
    logger.info("✅ [Investment Return] OUTPUT: final_value=%.2f, total_return=%.2f, contributed=%.2f",
                result.final_value, result.total_return, result.total_contributed)
    logger.info("✅ [Investment Return] ===== REQUEST END =====")
    
    return result
