"""Lưu session vào thư mục local (file JSON)."""

import json
import os
from pathlib import Path

from .base import MessageRecord, SessionData, SessionListItem, Storage


class LocalStorage(Storage):
    """Lưu mỗi session thành một file JSON."""

    def __init__(self, base_path: str = "./data/sessions") -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _path(self, session_id: str) -> Path:
        safe_id = "".join(c for c in session_id if c.isalnum() or c in "-_")
        return self.base_path / f"{safe_id}.json"

    def get_session(self, session_id: str) -> SessionData | None:
        p = self._path(session_id)
        if not p.exists():
            return None
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            return SessionData.model_validate(data)
        except (json.JSONDecodeError, ValueError):
            return None

    def save_session(self, data: SessionData) -> None:
        p = self._path(data.session_id)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(data.model_dump_json(indent=2), encoding="utf-8")

    def append_message(self, session_id: str, message: MessageRecord) -> None:
        session = self.get_session(session_id)
        if session is None:
            from datetime import timezone

            now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            session = SessionData(
                session_id=session_id,
                created_at=now,
                updated_at=now,
                messages=[],
            )
        session.messages.append(message)
        session.updated_at = message.created_at
        self.save_session(session)

    def list_sessions(self, limit: int = 50) -> list[SessionListItem]:
        """Liệt kê session theo updated_at mới nhất trước."""
        items: list[SessionListItem] = []
        for p in sorted(self.base_path.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            if len(items) >= limit:
                break
            session = self.get_session(p.stem)
            if session:
                items.append(SessionListItem(session_id=session.session_id, updated_at=session.updated_at))
        return items
