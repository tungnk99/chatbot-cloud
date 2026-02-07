"""Unit test: POST /tools/interest."""

import pytest
from fastapi.testclient import TestClient

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from main import app

client = TestClient(app)


def test_interest_simple() -> None:
    """Lãi đơn: 100tr, 6%/năm, 12 tháng -> lãi 6tr, total 106tr."""
    r = client.post(
        "/tools/interest",
        json={"principal": 100_000_000, "rate_percent": 6, "months": 12, "compound": False},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["principal"] == 100_000_000
    assert data["interest"] == 6_000_000
    assert data["total"] == 106_000_000
    assert data["compound"] is False


def test_interest_compound() -> None:
    """Lãi kép: 100, 10%/năm, 12 tháng."""
    r = client.post(
        "/tools/interest",
        json={"principal": 100, "rate_percent": 10, "months": 12, "compound": True},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["compound"] is True
    assert data["total"] > 100
    assert data["interest"] == data["total"] - 100


def test_interest_invalid_principal() -> None:
    """principal <= 0 -> 422 hoặc 400."""
    r = client.post(
        "/tools/interest",
        json={"principal": 0, "rate_percent": 6, "months": 12},
    )
    assert r.status_code in (400, 422)
