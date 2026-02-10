"""
Router: Chuyển đổi tiền tệ.

POST /tools/currency-convert
"""

import logging

from fastapi import APIRouter, HTTPException

from .schemas import CurrencyConvertRequest, CurrencyConvertResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Tỷ giá cố định (có thể mở rộng với API thực tế sau)
# Base: USD
EXCHANGE_RATES = {
    "USD": 1.0,
    "VND": 24000.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 148.0,
    "CNY": 7.24,
    "KRW": 1320.0,
    "THB": 35.0,
    "SGD": 1.34,
    "AUD": 1.52,
}


@router.post("/currency-convert", response_model=CurrencyConvertResponse)
def convert_currency(body: CurrencyConvertRequest) -> CurrencyConvertResponse:
    """
    Chuyển đổi tiền tệ sử dụng tỷ giá cố định.

    Args:
        body: amount, from_currency, to_currency.

    Returns:
        converted_amount, exchange_rate.

    Raises:
        HTTPException: 400 khi input không hợp lệ hoặc không hỗ trợ tiền tệ.
    """
    amount = body.amount
    from_currency = body.from_currency.upper()
    to_currency = body.to_currency.upper()
    
    logger.info("💱 [Currency Convert] ===== REQUEST START =====")
    logger.info("💱 [Currency Convert] INPUT: %.2f %s -> %s",
                amount, from_currency, to_currency)

    if amount <= 0:
        logger.warning("⚠️  [Currency Convert] Invalid amount: %.2f", amount)
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_INPUT",
                "message": "amount must be positive",
            },
        )

    if from_currency not in EXCHANGE_RATES:
        logger.warning("⚠️  [Currency Convert] Unsupported currency: %s", from_currency)
        raise HTTPException(
            status_code=400,
            detail={
                "code": "UNSUPPORTED_CURRENCY",
                "message": f"Currency {from_currency} is not supported",
                "supported": list(EXCHANGE_RATES.keys()),
            },
        )

    if to_currency not in EXCHANGE_RATES:
        logger.warning("⚠️  [Currency Convert] Unsupported currency: %s", to_currency)
        raise HTTPException(
            status_code=400,
            detail={
                "code": "UNSUPPORTED_CURRENCY",
                "message": f"Currency {to_currency} is not supported",
                "supported": list(EXCHANGE_RATES.keys()),
            },
        )

    # Chuyển đổi: from_currency -> USD -> to_currency
    usd_amount = amount / EXCHANGE_RATES[from_currency]
    converted_amount = usd_amount * EXCHANGE_RATES[to_currency]
    exchange_rate = EXCHANGE_RATES[to_currency] / EXCHANGE_RATES[from_currency]
    
    result = CurrencyConvertResponse(
        amount=amount,
        from_currency=from_currency,
        to_currency=to_currency,
        converted_amount=round(converted_amount, 2),
        exchange_rate=round(exchange_rate, 6),
    )
    
    logger.info("✅ [Currency Convert] OUTPUT: %.2f %s = %.2f %s (rate: %.6f)",
                amount, from_currency, result.converted_amount, to_currency, exchange_rate)
    logger.info("✅ [Currency Convert] ===== REQUEST END =====")
    
    return result
