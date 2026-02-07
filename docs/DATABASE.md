# Thiết Kế Database – Chatbot Tài Chính (Demo)

## 1. Tổng quan

Hệ thống lưu trữ **phiên hội thoại (session)** và **tin nhắn (message)** để phục vụ chat và lịch sử. Thiết kế đơn giản, phù hợp demo và kiến trúc serverless (GCP). Có thể dùng **Cloud Storage (GCS)** hoặc **Firestore** tùy triển khai.

---

## 2. Mô hình dữ liệu (Logical)

### 2.1 Entity chính

| Entity    | Mô tả |
|----------|--------|
| **Session** | Một phiên chat (1 user, 1 tab/trình duyệt). Có thể không đăng nhập, session_id sinh ngẫu nhiên. |
| **Message** | Một tin nhắn trong session: do user gửi hoặc do assistant (chatbot) trả lời. |

### 2.2 Quan hệ

- Một **Session** có nhiều **Message** (1–N).
- Message được sắp theo thời gian (chronological).

### 2.3 Thuộc tính chi tiết

**Session**

| Thuộc tính   | Kiểu   | Mô tả |
|-------------|--------|--------|
| `session_id` | string | ID duy nhất (UUID hoặc nanoid). |
| `created_at` | string (ISO 8601) | Thời điểm tạo session. |
| `updated_at` | string (ISO 8601) | Thời điểm cập nhật cuối (tin nhắn mới nhất). |

**Message**

| Thuộc tính   | Kiểu   | Mô tả |
|-------------|--------|--------|
| `message_id` | string | ID duy nhất trong session. |
| `role`       | string | `"user"` \| `"assistant"`. |
| `content`    | string | Nội dung tin nhắn. |
| `created_at` | string (ISO 8601) | Thời điểm gửi. |
| `tool_calls` | array (optional) | Danh sách tool được gọi (tên, input, output) – dùng cho hiển thị/log. |

---

## 3. Phương án lưu trữ

### 3.1 Phương án A: Cloud Storage (GCS) – Khuyến nghị cho demo

Lưu mỗi session thành **một file JSON** trong bucket. Đường dẫn gợi ý:

```
gs://<bucket>/chat/sessions/<session_id>.json
```

**Cấu trúc file JSON:**

```json
{
  "session_id": "sess_abc123",
  "created_at": "2025-02-07T10:00:00Z",
  "updated_at": "2025-02-07T10:05:00Z",
  "messages": [
    {
      "message_id": "msg_001",
      "role": "user",
      "content": "Lãi suất tiết kiệm 1 năm là bao nhiêu?",
      "created_at": "2025-02-07T10:00:00Z"
    },
    {
      "message_id": "msg_002",
      "role": "assistant",
      "content": "Hiện tại lãi suất tiết kiệm kỳ hạn 12 tháng...",
      "created_at": "2025-02-07T10:00:03Z",
      "tool_calls": []
    }
  ]
}
```

- **Ưu điểm**: Đơn giản, không cần DB server, phù hợp serverless, chi phí thấp.
- **Hạn chế**: Cập nhật = read → append message → write cả file (hoặc append-only log nếu mở rộng). Không query phức tạp.

**Quy ước tên bucket**: Ví dụ `chatbot-cloud-<project>-sessions` (tránh public list, dùng IAM).

---

### 3.2 Phương án B: Firestore

Dùng 2 collection:

- **sessions**: document id = `session_id`, fields: `created_at`, `updated_at`.
- **messages**: subcollection `sessions/{session_id}/messages`, document id = `message_id`, fields: `role`, `content`, `created_at`, `tool_calls` (optional).

**Ưu điểm**: Query linh hoạt, realtime, scale tốt. **Nhược điểm**: Cần cấu hình Firestore, chi phí theo read/write.

---

## 4. Quy ước và ràng buộc

- **session_id**, **message_id**: không trùng, có thể dùng UUID v4 hoặc nanoid.
- **created_at**, **updated_at**: ISO 8601 (UTC).
- **content**: plain text; nếu sau này hỗ trợ markdown/HTML thì mở rộng field hoặc thêm `content_type`.
- **tool_calls**: mảng object `{ "tool": "interest_calculator", "input": {...}, "output": {...} }` – dùng cho log và hiển thị kết quả tool trong demo.

---

## 5. Không lưu (theo PRD)

- Không lưu thông tin tài chính nhạy cảm thật (số tài khoản, số tiền thật của user).
- Không bắt buộc user profile / đăng nhập cho phiên demo.

---

*Tài liệu thiết kế database đơn giản cho demo – có thể bổ sung index, retention policy khi mở rộng.*
