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

# Mock API: test giao diện không cần backend (MOCK_API=true hoặc 1)
_MOCK_API = os.getenv("MOCK_API", "false").lower() in ("true", "1", "yes")


# -----------------------------------------------------------------------------
# API (thật hoặc mock)
# -----------------------------------------------------------------------------

def get_session_id() -> str:
    """Lấy hoặc tạo session_id trong session_state."""
    if "session_id" not in st.session_state:
        if _MOCK_API:
            st.session_state.session_id = f"sess_mock_{uuid.uuid4().hex[:12]}"
        else:
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


def load_sessions(limit: int = 30) -> list[dict]:
    """Lấy danh sách phiên chat (lịch sử) từ API."""
    if _MOCK_API:
        return [
            {"session_id": "sess_mock_1", "updated_at": "2025-02-07T10:00:00Z"},
            {"session_id": "sess_mock_2", "updated_at": "2025-02-07T09:30:00Z"},
        ]
    try:
        r = httpx.get(
            f"{CHATBOT_API_URL}{API_PREFIX}/sessions",
            params={"limit": limit},
            timeout=10.0,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("sessions", [])
    except Exception:
        return []


def load_history(session_id: str) -> list[dict]:
    """Lấy lịch sử tin nhắn từ API."""
    if _MOCK_API:
        return []
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
    """Gửi tin nhắn tới Chatbot API."""
    if _MOCK_API:
        return {
            "session_id": session_id,
            "message_id": f"msg_mock_{uuid.uuid4().hex[:8]}",
            "content": f"*[Mock]* Đây là phản hồi giả. Bạn đã hỏi: \"{message}\". Bật backend và tắt MOCK_API để nhận phản hồi thật từ LLM.",
            "tool_calls": [],
            "status": "completed",
        }
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
    """Poll GET messages cho tới khi có assistant message hoặc timeout."""
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


# -----------------------------------------------------------------------------
# Theme & layout
# -----------------------------------------------------------------------------

def inject_theme() -> None:
    """CSS theme AI: gradient, spacing, chat bubbles, sidebar, empty state."""
    st.markdown(
        """
        <style>
        /* Nền */
        .stApp {
            background: linear-gradient(165deg, #0a0c10 0%, #0e1117 35%, #131720 70%, #0d1117 100%);
        }
        .main .block-container {
            padding: 1rem 1rem 2.5rem;
            max-width: 44rem;
        }
        /* Header */
        .app-header {
            text-align: center;
            padding: 1rem 0 1.25rem;
            margin-bottom: 0.75rem;
            border-bottom: 1px solid rgba(0, 212, 170, 0.1);
        }
        .app-header .logo {
            font-size: 1.6rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            background: linear-gradient(135deg, #00d4aa 0%, #22d3c4 50%, #7c3aed 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
        }
        .app-header .subtitle {
            color: rgba(250, 250, 250, 0.55);
            font-size: 0.8rem;
            margin-top: 0.35rem;
            letter-spacing: 0.02em;
        }
        /* Empty state */
        .empty-state {
            text-align: center;
            padding: 2.5rem 1rem;
            margin: 1rem 0;
            border-radius: 16px;
            background: rgba(0, 212, 170, 0.04);
            border: 1px dashed rgba(0, 212, 170, 0.2);
        }
        .empty-state .title {
            color: rgba(250, 250, 250, 0.9);
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .empty-state .hint {
            color: rgba(250, 250, 250, 0.5);
            font-size: 0.8rem;
            margin-bottom: 1.25rem;
        }
        .suggestion-chip {
            display: inline-block;
            padding: 0.45rem 0.85rem;
            margin: 0.25rem;
            border-radius: 20px;
            background: rgba(26, 29, 36, 0.8);
            border: 1px solid rgba(0, 212, 170, 0.2);
            color: rgba(250, 250, 250, 0.85);
            font-size: 0.8rem;
            cursor: pointer;
            transition: border-color 0.2s, background 0.2s;
        }
        .suggestion-chip:hover {
            border-color: rgba(0, 212, 170, 0.45);
            background: rgba(0, 212, 170, 0.08);
        }
        /* Chat area */
        [data-testid="stChatMessage"] {
            padding: 0.6rem 0;
            margin-bottom: 0.2rem;
        }
        [data-testid="stChatMessage"] > div:first-child {
            border-radius: 14px;
            padding: 0.9rem 1.1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            background: rgba(26, 29, 36, 0.7);
            border: 1px solid rgba(0, 212, 170, 0.12);
        }
        /* Input */
        [data-testid="stChatInput"] {
            padding-top: 0.75rem;
        }
        [data-testid="stChatInput"] textarea {
            border: 1px solid rgba(0, 212, 170, 0.22) !important;
            border-radius: 14px !important;
            background: rgba(20, 23, 30, 0.9) !important;
            font-size: 0.95rem !important;
        }
        [data-testid="stChatInput"] textarea:focus {
            box-shadow: 0 0 0 2px rgba(0, 212, 170, 0.18) !important;
            border-color: rgba(0, 212, 170, 0.4) !important;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color: rgba(250, 250, 250, 0.4) !important;
        }
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f1218 0%, #0a0c10 100%);
            border-right: 1px solid rgba(0, 212, 170, 0.08);
        }
        [data-testid="stSidebar"] .stMarkdown { color: rgba(250, 250, 250, 0.9); }
        .sidebar-section {
            margin-bottom: 1.35rem;
        }
        .sidebar-section-title {
            font-size: 0.68rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: rgba(0, 212, 170, 0.85);
            margin-bottom: 0.5rem;
        }
        .session-id-box {
            font-size: 0.72rem;
            padding: 0.5rem 0.65rem;
            background: rgba(0, 212, 170, 0.05);
            border: 1px solid rgba(0, 212, 170, 0.12);
            border-radius: 8px;
            word-break: break-all;
            color: rgba(250, 250, 250, 0.75);
        }
        .session-list { max-height: 220px; overflow-y: auto; margin-bottom: 0.5rem; }
        /* Buttons sidebar */
        [data-testid="stSidebar"] button {
            border-radius: 8px !important;
            font-size: 0.8rem !important;
        }
        [data-testid="stSidebar"] button[kind="primary"] {
            background: linear-gradient(135deg, rgba(0, 212, 170, 0.2) 0%, rgba(124, 58, 237, 0.15) 100%) !important;
            border: 1px solid rgba(0, 212, 170, 0.25) !important;
        }
        /* Expander */
        .streamlit-expanderHeader { color: #00d4aa !important; }
        .stSpinner label { color: rgba(250, 250, 250, 0.75) !important; }
        /* Footer */
        .app-footer {
            text-align: center;
            padding: 1rem 0 0.5rem;
            margin-top: 1rem;
            border-top: 1px solid rgba(0, 212, 170, 0.08);
            color: rgba(250, 250, 250, 0.4);
            font-size: 0.7rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <div class="app-header">
            <p class="logo">◇ Chatbot Tài Chính</p>
            <p class="subtitle">Tư vấn tài chính · Lãi suất · Tiết kiệm · Vay vốn · Đầu tư · Ngân sách · Powered by AI</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Gợi ý câu hỏi khi chưa có tin nhắn - Bao gồm cả 7 tools
SUGGESTIONS = [
    # Tools cũ
    "Tính lãi 100 triệu gửi 12 tháng, lãi suất 6%/năm?",
    "Tỷ lệ tiết kiệm nếu thu nhập 20 triệu, tiết kiệm 5 triệu?",
    # Tools mới
    "Vay 500 triệu lãi 8%/năm trả góp 10 năm, mỗi tháng trả bao nhiêu?",
    "Đầu tư 10tr ban đầu + 2tr/tháng, lợi nhuận 8%/năm trong 10 năm được bao nhiêu?",
    "Thu nhập 20 triệu/tháng nên phân bổ ngân sách thế nào?",
    "1000 USD bằng bao nhiêu tiền Việt?",
    "Chi tiêu 15 triệu/tháng cần bao nhiêu tiền dự phòng?",
    "Cách lập quỹ dự phòng 6 tháng chi tiêu?",
]


def render_empty_state() -> None:
    """Hiển thị welcome + gợi ý khi chưa có tin nhắn."""
    st.markdown(
        """
        <div class="empty-state">
            <p class="title">Chào bạn! Tôi có thể giúp gì cho bạn?</p>
            <p class="hint">7 công cụ tài chính: Lãi suất, Tiết kiệm, Vay vốn, Đầu tư, Ngân sách, Chuyển đổi tiền tệ, Quỹ dự phòng</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("**💡 Gợi ý câu hỏi:**")
    cols = st.columns(2)
    for i, text in enumerate(SUGGESTIONS):
        with cols[i % 2]:
            if st.button(f"💡 {text}", key=f"suggest_{i}", use_container_width=True):
                st.session_state.pending_suggestion = text
                st.rerun()


def _format_session_date(updated_at: str) -> str:
    """Chuyển updated_at ISO sang dạng ngắn (vd: 7/2 14:30)."""
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        return dt.strftime("%d/%m %H:%M")
    except Exception:
        return updated_at[:16] if len(updated_at) >= 16 else updated_at


def render_sidebar(session_id: str) -> None:
    """Render sidebar: phiên hiện tại, lịch sử phiên, hành động."""
    with st.sidebar:
        if _MOCK_API:
            st.info("🧪 **Mock API** – đang dùng dữ liệu giả (MOCK_API=true)")
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-section-title">Phiên hiện tại</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="session-id-box">{session_id}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-section-title">Lịch sử phiên</p>', unsafe_allow_html=True)
        sessions = load_sessions(limit=30)
        for s in sessions:
            sid = s.get("session_id", "")
            if not sid:
                continue
            label = f"{sid[:14]}... — {_format_session_date(s.get('updated_at', ''))}"
            is_current = sid == session_id
            if is_current:
                st.caption(f"● {label}")
            elif st.button(label, key=f"session_{sid}", use_container_width=True):
                st.session_state.session_id = sid
                st.session_state.messages = []
                st.rerun()
        if not sessions:
            st.caption("Chưa có phiên nào.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        if st.button("Tạo phiên mới", use_container_width=True):
            st.session_state.session_id = f"sess_{uuid.uuid4().hex[:16]}"
            st.session_state.messages = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def render_message(msg: dict) -> None:
    """Render một tin nhắn (user hoặc assistant) kèm tool_calls nếu có."""
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("tool_calls"):
            with st.expander("Công cụ đã dùng"):
                for tc in msg["tool_calls"]:
                    st.json({"tool": tc.get("tool"), "output": tc.get("output")})


def handle_send_message(session_id: str, prompt: str, use_async: bool) -> None:
    """Xử lý gửi tin nhắn: sync hoặc async (poll)."""
    st.session_state.messages.append({"role": "user", "content": prompt, "tool_calls": []})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):
            resp = send_message(session_id, prompt, use_async=use_async)

        if not resp:
            st.session_state.messages.pop()
            return

        if resp.get("status") == "pending":
            count_before = len(st.session_state.messages) - 1
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
                st.warning("Hết thời gian chờ phản hồi. Thử tải lại hoặc gửi lại.")
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


def main() -> None:
    st.set_page_config(
        page_title="Chatbot Tài Chính",
        page_icon="◇",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    inject_theme()
    render_header()

    session_id = get_session_id()
    render_sidebar(session_id)

    if "messages" not in st.session_state:
        st.session_state.messages = []
        for m in load_history(session_id):
            st.session_state.messages.append({
                "role": m["role"],
                "content": m["content"],
                "tool_calls": m.get("tool_calls", []),
            })

    # Empty state: welcome + gợi ý
    if not st.session_state.messages:
        render_empty_state()

    for msg in st.session_state.messages:
        render_message(msg)

    # Xử lý gợi ý đã chọn (sau khi rerun)
    prompt = None
    if "pending_suggestion" in st.session_state:
        prompt = st.session_state.pop("pending_suggestion", None)
    if prompt is None:
        prompt = st.chat_input("Nhập câu hỏi...")

    if prompt:
        handle_send_message(session_id, prompt, use_async=False)

    # Footer
    st.markdown(
        '<p class="app-footer">Chatbot Tài Chính · Powered by AI</p>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
