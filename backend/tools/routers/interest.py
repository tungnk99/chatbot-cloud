"""
Router: Tính lãi đơn / lãi kép.

POST /tools/interest
"""

from fastapi import APIRouter, HTTPException

from .schemas import InterestRequest, InterestResponse

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

    if principal <= 0 or rate_percent < 0 or months <= 0:
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

    return InterestResponse(
        principal=principal,
        interest=round(interest_amount, 2),
        total=round(total, 2),
        rate_percent=rate_percent,
        months=months,
        compound=compound,
    )
