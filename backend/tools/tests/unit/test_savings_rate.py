"""Unit test: POST /tools/savings-rate."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_savings_rate_20_percent() -> None:
    """Thu nhập 20tr, tiết kiệm 4tr -> 20%."""
    r = client.post(
        "/tools/savings-rate",
        json={"income": 20_000_000, "savings": 4_000_000},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["savings_rate_percent"] == 20.0
    assert "suggestion" in data


def test_savings_rate_invalid_income() -> None:
    """income <= 0 -> 400/422."""
    r = client.post(
        "/tools/savings-rate",
        json={"income": 0, "savings": 1000},
    )
    assert r.status_code in (400, 422)
