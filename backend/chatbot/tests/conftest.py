"""Pytest fixtures cho Chatbot API."""

import sys
from pathlib import Path

# Đảm bảo backend/chatbot trên path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
