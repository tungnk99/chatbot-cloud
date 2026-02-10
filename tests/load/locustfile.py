"""
Load test – Locust.

Mô phỏng nhiều user gọi Chatbot API và Tools API.
Chạy: locust -f tests/load/locustfile.py --host=http://localhost:8080
Hoặc: CHATBOT_URL=http://localhost:8080 TOOLS_URL=http://localhost:8081 locust -f tests/load/locustfile.py
Mở http://localhost:8089 để điều khiển và xem báo cáo.
"""

import os
import uuid
from locust import HttpUser, task, between

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8080").rstrip("/")
TOOLS_URL = os.getenv("TOOLS_URL", "http://localhost:8081").rstrip("/")


class ChatbotUser(HttpUser):
    """User gọi Chatbot API: health, tạo session, gửi tin nhắn."""

    host = CHATBOT_URL
    wait_time = between(1, 3)

    def on_start(self) -> None:
        """Tạo session khi user bắt đầu."""
        r = self.client.post(
            "/api/sessions",
            name="/api/sessions [create]",
        )
        if r.status_code == 201:
            self.session_id = r.json().get("session_id", f"sess_{uuid.uuid4().hex[:16]}")
        else:
            self.session_id = f"sess_{uuid.uuid4().hex[:16]}"

    @task(3)
    def health(self) -> None:
        self.client.get("/health", name="/health")

    @task(5)
    def chat(self) -> None:
        """Send simple chat message"""
        self.client.post(
            "/api/chat",
            json={
                "session_id": self.session_id,
                "message": "Xin chào",
            },
            name="/api/chat",
        )

    @task(2)
    def create_multiple_sessions(self) -> None:
        """Create multiple sessions to generate load"""
        self.client.post(
            "/api/sessions",
            name="/api/sessions [create]",
        )

    @task(3)
    def get_messages(self) -> None:
        """Get messages - may return empty but shouldn't error"""
        self.client.get(
            f"/api/sessions/{self.session_id}/messages",
            name="/api/sessions/{id}/messages",
        )


# ToolsUser disabled - chỉ test Chatbot API
# Uncomment nếu muốn test Tools API riêng
# class ToolsUser(HttpUser):
#     """User gọi Tools API: health, interest, savings-rate."""
#
#     host = TOOLS_URL
#     wait_time = between(0.5, 2)
#
#     @task(2)
#     def health(self) -> None:
#         self.client.get("/health", name="/health")
#
#     @task(4)
#     def interest(self) -> None:
#         self.client.post(
#             "/tools/interest",
#             json={
#                 "principal": 100_000_000,
#                 "rate_percent": 6,
#                 "months": 12,
#                 "compound": False,
#             },
#             name="/tools/interest",
#         )
#
#     @task(3)
#     def savings_rate(self) -> None:
#         self.client.post(
#             "/tools/savings-rate",
#             json={"income": 20_000_000, "savings": 4_000_000},
#             name="/tools/savings-rate",
#         )
