"""
Client gọi Tools service (Backend/tools) qua HTTP.
"""

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class ToolsClient:
    """Gọi API Tools: interest, savings-rate."""

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
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(
                f"{self.base_url}/tools/interest",
                json={
                    "principal": principal,
                    "rate_percent": rate_percent,
                    "months": months,
                    "compound": compound,
                },
            )
            r.raise_for_status()
            return r.json()

    async def savings_rate(self, income: float, savings: float) -> dict[str, Any]:
        """POST /tools/savings-rate."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(
                f"{self.base_url}/tools/savings-rate",
                json={"income": income, "savings": savings},
            )
            r.raise_for_status()
            return r.json()
