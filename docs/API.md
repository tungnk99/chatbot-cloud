# Thiết Kế API – Chatbot Tài Chính (Demo)

## 1. Tổng quan

API REST cho **Chatbot Service** (Frontend ↔ Backend/Chatbot) và **Tools** (Chatbot ↔ Backend/Tools). Định dạng JSON, UTF-8. Base URL ví dụ:

- Chatbot (Backend): `https://chatbot-xxxx.run.app`
- Tools (Backend): `https://tools-xxxx.run.app` (hoặc cùng domain với path `/tools` tùy triển khai)

---

## 2. Chatbot Service API

### 2.1 Gửi tin nhắn và nhận phản hồi

**POST** `/chat` hoặc `/api/chat`

Gửi tin nhắn user, nhận phản hồi từ chatbot (có thể gọi LLM + Tools).

**Request**

| Header        | Mô tả |
|---------------|--------|
| `Content-Type` | `application/json` |

**Body**

```json
{
  "session_id": "sess_abc123",
  "message": "Nếu gửi 100 triệu, lãi suất 6%/năm, 12 tháng thì lãi bao nhiêu?"
}
```

| Field        | Kiểu   | Bắt buộc | Mô tả |
|-------------|--------|----------|--------|
| `session_id` | string | Có       | ID phiên chat (tạo mới nếu chưa có). |
| `message`    | string | Có       | Nội dung tin nhắn user. |

**Response 200**

```json
{
  "session_id": "sess_abc123",
  "message_id": "msg_002",
  "content": "Với 100 triệu, lãi suất 6%/năm, kỳ hạn 12 tháng, tiền lãi khoảng 6 triệu (lãi đơn)...",
  "tool_calls": [
    {
      "tool": "interest_calculator",
      "input": { "principal": 100000000, "rate_percent": 6, "months": 12 },
      "output": { "interest": 6000000, "total": 106000000 }
    }
  ]
}
```

| Field        | Kiểu   | Mô tả |
|-------------|--------|--------|
| `session_id` | string | Trùng request. |
| `message_id` | string | ID tin nhắn assistant vừa tạo. |
| `content`    | string | Nội dung trả lời. |
| `tool_calls` | array  | (Optional) Các tool đã gọi trong lượt này. |

**Lỗi thường gặp**

- `400 Bad Request`: Thiếu `session_id` hoặc `message`, body không hợp lệ.
- `500 Internal Server Error`: Lỗi LLM, Tools hoặc Storage.

---

### 2.2 Lấy lịch sử hội thoại

**GET** `/sessions/{session_id}/messages` hoặc `/api/sessions/{session_id}/messages`

Trả về danh sách tin nhắn trong session (để hiển thị lại lịch sử).

**Response 200**

```json
{
  "session_id": "sess_abc123",
  "messages": [
    {
      "message_id": "msg_001",
      "role": "user",
      "content": "Lãi suất tiết kiệm 1 năm?",
      "created_at": "2025-02-07T10:00:00Z"
    },
    {
      "message_id": "msg_002",
      "role": "assistant",
      "content": "Hiện tại lãi suất tiết kiệm 12 tháng...",
      "created_at": "2025-02-07T10:00:03Z",
      "tool_calls": []
    }
  ]
}
```

**Lỗi**

- `404 Not Found`: Không tìm thấy session (hoặc chưa có tin nhắn).

---

### 2.3 Tạo session mới (tùy chọn)

Nếu không tạo session ngầm trong `/chat`, có thể dùng:

**POST** `/api/sessions`

**Body**: `{}` hoặc không gửi body.

**Response 201**

```json
{
  "session_id": "sess_xyz789",
  "created_at": "2025-02-07T10:00:00Z"
}
```

---

## 3. Tools API (Nội bộ / Chatbot gọi)

Tools được Chatbot gọi khi cần tính toán. Có thể triển khai dưới dạng microservice riêng (mỗi tool một endpoint) hoặc một service với nhiều path.

### 3.1 Tính lãi (đơn / ghép)

**POST** `/tools/interest` hoặc `/interest`

**Body**

```json
{
  "principal": 100000000,
  "rate_percent": 6,
  "months": 12,
  "compound": false
}
```

| Field          | Kiểu    | Bắt buộc | Mô tả |
|----------------|---------|----------|--------|
| `principal`    | number  | Có       | Số tiền gốc (VNĐ hoặc đơn vị). |
| `rate_percent` | number  | Có       | Lãi suất %/năm. |
| `months`       | number  | Có       | Kỳ hạn (tháng). |
| `compound`     | boolean | Không   | `true` = lãi kép, mặc định `false` = lãi đơn. |

**Response 200**

```json
{
  "principal": 100000000,
  "interest": 6000000,
  "total": 106000000,
  "rate_percent": 6,
  "months": 12,
  "compound": false
}
```

---

### 3.2 Tính tỷ lệ tiết kiệm so với thu nhập

**POST** `/tools/savings-rate` hoặc `/savings-rate`

**Body**

```json
{
  "income": 20000000,
  "savings": 4000000
}
```

| Field     | Kiểu   | Bắt buộc | Mô tả |
|-----------|--------|----------|--------|
| `income`  | number | Có       | Thu nhập (đơn vị). |
| `savings` | number | Có       | Số tiền tiết kiệm. |

**Response 200**

```json
{
  "income": 20000000,
  "savings": 4000000,
  "savings_rate_percent": 20,
  "suggestion": "Tỷ lệ tiết kiệm 20% thu nhập là mức tốt, thường khuyến nghị 10–20%."
}
```

---

## 4. Quy ước chung

### 4.1 Định dạng lỗi

Mọi response lỗi (4xx, 5xx) nên có body JSON thống nhất:

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "session_id is required"
  }
}
```

### 4.2 Mã trạng thái HTTP

| Mã   | Ý nghĩa |
|------|---------|
| 200  | Thành công. |
| 201  | Tạo mới thành công (ví dụ session). |
| 400  | Request không hợp lệ. |
| 404  | Không tìm thấy tài nguyên. |
| 500  | Lỗi phía server. |

### 4.3 Health check (tùy chọn)

**GET** `/health` hoặc `/ready`

- **200**: Service sẵn sàng nhận request.
- Dùng cho Cloud Run health check.

---

## 5. Luồng gọi API (Demo)

1. **Frontend (Web)** → **POST /chat** với `session_id` + `message` tới Backend (Chatbot).
2. **Backend (Chatbot)** đọc/ghi session (GCS hoặc Firestore), gọi LLM.
3. Nếu LLM quyết định dùng tool → **Chatbot** gọi **POST /tools/interest** hoặc **/tools/savings-rate** (Backend/Tools).
4. **Chatbot** gộp kết quả tool vào câu trả lời, lưu message, trả **response** cho Frontend.
5. **Frontend** gọi **GET /sessions/{id}/messages** khi cần load lại lịch sử.

---

*Tài liệu thiết kế API đơn giản cho demo – có thể bổ sung auth (API key, CORS) khi triển khai thật.*
