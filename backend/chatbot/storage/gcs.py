"""Lưu session vào Google Cloud Storage (GCS)."""

import json
from datetime import timezone
from datetime import datetime

from .base import MessageRecord, SessionData, SessionListItem, Storage

try:
    from google.cloud import storage
except ImportError:
    storage = None  # type: ignore


class GCSStorage(Storage):
    """Lưu mỗi session thành một object JSON trong bucket: chat/sessions/<session_id>.json."""

    def __init__(self, bucket_name: str, prefix: str = "chat/sessions") -> None:
        if storage is None:
            raise RuntimeError("google-cloud-storage is required for GCSStorage")
        self.client = storage.Client()
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(bucket_name)
        self.prefix = prefix.rstrip("/")

    def _blob_name(self, session_id: str) -> str:
        safe_id = "".join(c for c in session_id if c.isalnum() or c in "-_")
        return f"{self.prefix}/{safe_id}.json"

    def get_session(self, session_id: str) -> SessionData | None:
        blob = self.bucket.blob(self._blob_name(session_id))
        try:
            data = json.loads(blob.download_as_string().decode("utf-8"))
            return SessionData.model_validate(data)
        except Exception:
            return None

    def save_session(self, data: SessionData) -> None:
        blob = self.bucket.blob(self._blob_name(data.session_id))
        blob.upload_from_string(
            data.model_dump_json(indent=2),
            content_type="application/json",
        )

    def append_message(self, session_id: str, message: MessageRecord) -> None:
        session = self.get_session(session_id)
        if session is None:
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
        """Liệt kê session theo thời gian cập nhật object GCS mới nhất trước."""
        prefix = f"{self.prefix}/"
        blobs = list(self.bucket.list_blobs(prefix=prefix, max_results=limit * 2))
        items: list[SessionListItem] = []
        for b in sorted(blobs, key=lambda x: x.updated or x.time_created, reverse=True):
            if len(items) >= limit:
                break
            if not b.name.endswith(".json") or b.name == prefix:
                continue
            name = b.name
            if name.startswith(prefix):
                name = name[len(prefix) :]
            session_id = name.removesuffix(".json")
            updated = b.updated or b.time_created
            updated_at = updated.strftime("%Y-%m-%dT%H:%M:%SZ") if updated else ""
            if session_id:
                items.append(SessionListItem(session_id=session_id, updated_at=updated_at))
        return items[:limit]
