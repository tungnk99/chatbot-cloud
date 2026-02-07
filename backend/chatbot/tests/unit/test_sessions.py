"""Unit test: POST /api/sessions, GET /api/sessions/{id}/messages."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_create_session() -> None:
    r = client.post("/api/sessions")
    assert r.status_code == 201
    data = r.json()
    assert "session_id" in data
    assert data["session_id"].startswith("sess_")
    assert "created_at" in data


def test_get_messages_empty_session_404() -> None:
    """Session chưa có message -> 404."""
    r = client.get("/api/sessions/sess_nonexistent123/messages")
    assert r.status_code == 404
