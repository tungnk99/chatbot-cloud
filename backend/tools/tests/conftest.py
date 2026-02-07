"""Pytest fixtures cho Tools API."""

import pytest
from fastapi.testclient import TestClient

# Chạy test từ backend/tools; sys.path có backend/tools
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app


@pytest.fixture
def client() -> TestClient:
    """FastAPI test client."""
    return TestClient(app)
