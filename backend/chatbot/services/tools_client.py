"""
Client gọi Tools service (Backend/tools) qua HTTP.
"""

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class ToolsClient:
    """Gọi API Tools: interest, savings-rate, loan-payment, investment-return, budget-breakdown, currency-convert, emergency-fund."""

    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def interest(
        self,
        principal: float,
        rate_percent: float,
        months: float,
        compound: bool = False,
    ) -> dict[str, Any]:
        """POST /tools/interest."""
        url = f"{self.base_url}/tools/interest"
        payload = {
            "principal": principal,
            "rate_percent": rate_percent,
            "months": months,
            "compound": compound,
        }
        logger.info("🌐 HTTP POST %s với payload: %s", url, payload)
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            result = r.json()
            logger.info("✅ Tools API trả về: %s", result)
            return result

    async def savings_rate(self, income: float, savings: float) -> dict[str, Any]:
        """POST /tools/savings-rate."""
        url = f"{self.base_url}/tools/savings-rate"
        payload = {"income": income, "savings": savings}
        logger.info("🌐 HTTP POST %s với payload: %s", url, payload)
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            result = r.json()
            logger.info("✅ Tools API trả về: %s", result)
            return result

    async def loan_payment(
        self,
        principal: float,
        annual_rate: float,
        months: int,
    ) -> dict[str, Any]:
        """POST /tools/loan-payment."""
        url = f"{self.base_url}/tools/loan-payment"
        payload = {
            "principal": principal,
            "annual_rate": annual_rate,
            "months": months,
        }
        logger.info("🌐 HTTP POST %s với payload: %s", url, payload)
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            result = r.json()
            logger.info("✅ Tools API trả về: %s", result)
            return result

    async def investment_return(
        self,
        initial_amount: float,
        monthly_contribution: float,
        annual_return: float,
        years: float,
    ) -> dict[str, Any]:
        """POST /tools/investment-return."""
        url = f"{self.base_url}/tools/investment-return"
        payload = {
            "initial_amount": initial_amount,
            "monthly_contribution": monthly_contribution,
            "annual_return": annual_return,
            "years": years,
        }
        logger.info("🌐 HTTP POST %s với payload: %s", url, payload)
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            result = r.json()
            logger.info("✅ Tools API trả về: %s", result)
            return result

    async def budget_breakdown(self, monthly_income: float) -> dict[str, Any]:
        """POST /tools/budget-breakdown."""
        url = f"{self.base_url}/tools/budget-breakdown"
        payload = {"monthly_income": monthly_income}
        logger.info("🌐 HTTP POST %s với payload: %s", url, payload)
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            result = r.json()
            logger.info("✅ Tools API trả về: %s", result)
            return result

    async def currency_convert(
        self,
        amount: float,
        from_currency: str,
        to_currency: str,
    ) -> dict[str, Any]:
        """POST /tools/currency-convert."""
        url = f"{self.base_url}/tools/currency-convert"
        payload = {
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
        }
        logger.info("🌐 HTTP POST %s với payload: %s", url, payload)
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            result = r.json()
            logger.info("✅ Tools API trả về: %s", result)
            return result

    async def emergency_fund(
        self,
        monthly_expenses: float,
        months_coverage: int = 6,
    ) -> dict[str, Any]:
        """POST /tools/emergency-fund."""
        url = f"{self.base_url}/tools/emergency-fund"
        payload = {
            "monthly_expenses": monthly_expenses,
            "months_coverage": months_coverage,
        }
        logger.info("🌐 HTTP POST %s với payload: %s", url, payload)
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            result = r.json()
            logger.info("✅ Tools API trả về: %s", result)
            return result
