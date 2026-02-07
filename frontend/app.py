"""
Frontend Chatbot - Giao diện chat (Streamlit).

Gọi Backend Chatbot API: POST /api/chat, GET /api/sessions/{id}/messages, POST /api/sessions.
"""

import os
import uuid

import httpx
import streamlit as st

CHATBOT_API_URL = os.getenv("CHATBOT_API_URL", "http://localhost:8080")
API_PREFIX = "/api"


def get_session_id() -> str:
    """Lấy hoặc tạo session_id trong session_state."""
    if "session_id" not in st.session_state:
        try:
            r = httpx.post(
                f"{CHATBOT_API_URL}{API_PREFIX}/sessions",
                timeout=10.0,
            )
            r.raise_for_status()
            data = r.json()
            st.session_state.session_id = data["session_id"]
        except Exception:
            st.session_state.session_id = f"sess_{uuid.uuid4().hex[:16]}"
    return st.session_state.session_id


def load_history(session_id: str) -> list[dict]:
    """Lấy lịch sử tin nhắn từ API."""
    try:
        r = httpx.get(
            f"{CHATBOT_API_URL}{API_PREFIX}/sessions/{session_id}/messages",
            timeout=10.0,
        )
        if r.status_code == 404:
            return []
        r.raise_for_status()
        data = r.json()
        return data.get("messages", [])
    except Exception:
        return []


def send_message(session_id: str, message: str, use_async: bool = False) -> dict | None:
    """Gửi tin nhắn tới Chatbot API. use_async=True: đẩy vào Pub/Sub, trả về pending; client cần poll messages."""
    try:
        url = f"{CHATBOT_API_URL}{API_PREFIX}/chat"
        params = {"async": "1"} if use_async else None
        r = httpx.post(
            url,
            json={"session_id": session_id, "message": message},
            params=params,
            timeout=60.0,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Lỗi kết nối: {e}")
        return None


def wait_for_assistant_message(
    session_id: str,
    current_count: int,
    poll_interval: float = 2.0,
    timeout_seconds: float = 120.0,
) -> list[dict] | None:
    """Poll GET messages cho tới khi có thêm assistant message hoặc timeout. Trả về danh sách messages mới hoặc None."""
    import time

    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            r = httpx.get(
                f"{CHATBOT_API_URL}{API_PREFIX}/sessions/{session_id}/messages",
                timeout=10.0,
            )
            if r.status_code == 404:
                time.sleep(poll_interval)
                continue
            r.raise_for_status()
            data = r.json()
            messages = data.get("messages", [])
            if len(messages) > current_count and messages[-1].get("role") == "assistant":
                return messages
        except Exception:
            pass
        time.sleep(poll_interval)
    return None


def main() -> None:
    st.set_page_config(
        page_title="Chatbot Tài Chính",
        page_icon="💬",
        layout="centered",
    )

    st.title("💬 Chatbot Tài Chính")
    st.caption("Hỏi đáp tài chính cơ bản • Tính lãi • Tỷ lệ tiết kiệm")

    session_id = get_session_id()

    if "messages" not in st.session_state:
        st.session_state.messages = []
        history = load_history(session_id)
        for m in history:
            st.session_state.messages.append(
                {"role": m["role"], "content": m["content"], "tool_calls": m.get("tool_calls", [])}
            )

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("tool_calls"):
                with st.expander("Công cụ đã dùng"):
                    for tc in msg["tool_calls"]:
                        st.json({"tool": tc.get("tool"), "output": tc.get("output")})

    if prompt := st.chat_input("Nhập câu hỏi..."):
        st.session_state.messages.append({"role": "user", "content": prompt, "tool_calls": []})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Đang xử lý..."):
                resp = send_message(session_id, prompt, use_async=use_async)
            if resp:
                if resp.get("status") == "pending":
                    # Bất đồng bộ: poll GET messages cho tới khi có assistant reply (sau user vừa gửi)
                    count_before = len(st.session_state.messages) - 1  # trước khi thêm user
                    with st.spinner("Đang chờ phản hồi từ hàng đợi..."):
                        new_messages = wait_for_assistant_message(session_id, count_before + 1)
                    if new_messages:
                        for m in new_messages[count_before:]:
                            if m["role"] == "assistant":
                                content = m.get("content", "")
                                tool_calls = m.get("tool_calls", [])
                                st.markdown(content)
                                if tool_calls:
                                    with st.expander("Công cụ đã dùng"):
                                        for tc in tool_calls:
                                            st.json({"tool": tc.get("tool"), "output": tc.get("output")})
                                st.session_state.messages.append(
                                    {"role": "assistant", "content": content, "tool_calls": tool_calls}
                                )
                                break
                    else:
                        st.warning("Hết thời gian chờ phản hồi. Thử tải lại lịch sử hoặc gửi lại.")
                else:
                    content = resp.get("content", "")
                    tool_calls = resp.get("tool_calls", [])
                    st.markdown(content)
                    if tool_calls:
                        with st.expander("Công cụ đã dùng"):
                            for tc in tool_calls:
                                st.json({"tool": tc.get("tool"), "output": tc.get("output")})
                    st.session_state.messages.append(
                        {"role": "assistant", "content": content, "tool_calls": tool_calls}
                    )
            else:
                st.session_state.messages.pop()

    st.sidebar.markdown("### Phiên chat")
    st.sidebar.code(session_id, language=None)
    use_async = st.sidebar.checkbox(
        "Xử lý bất đồng bộ (Pub/Sub)",
        value=False,
        help="Đẩy tin nhắn vào hàng đợi, tránh treo kết nối khi LLM xử lý lâu. Cần bật Pub/Sub trên backend.",
    )
    if st.sidebar.button("Tạo phiên mới"):
        st.session_state.session_id = f"sess_{uuid.uuid4().hex[:16]}"
        st.session_state.messages = []
        st.rerun()


if __name__ == "__main__":
    main()
