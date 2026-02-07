"""Interface lưu trữ session/message."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class MessageRecord(BaseModel):
    """Một tin nhắn trong session."""

    message_id: str
    role: str  # "user" | "assistant"
    content: str
    created_at: str  # ISO 8601
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)


class SessionData(BaseModel):
    """Dữ liệu một session."""

    session_id: str
    created_at: str
    updated_at: str
    messages: list[MessageRecord] = Field(default_factory=list)


class Storage(ABC):
    """Abstract storage cho session."""

    @abstractmethod
    def get_session(self, session_id: str) -> SessionData | None:
        """Lấy session theo id. Trả về None nếu không tồn tại."""
        ...

    @abstractmethod
    def save_session(self, data: SessionData) -> None:
        """Lưu hoặc cập nhật session."""
        ...

    @abstractmethod
    def append_message(self, session_id: str, message: MessageRecord) -> None:
        """Thêm một message vào session (tạo session nếu chưa có)."""
        ...
