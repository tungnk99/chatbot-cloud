"""Storage abstraction cho session và message."""

from .base import MessageRecord, SessionData, Storage
from .local import LocalStorage

__all__ = ["Storage", "SessionData", "SessionListItem", "MessageRecord", "LocalStorage"]

try:
    from .gcs import GCSStorage
    __all__.append("GCSStorage")
except ImportError:
    GCSStorage = None  # type: ignore
