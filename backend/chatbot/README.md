# Chatbot Service (Backend/chatbot)

Dịch vụ chatbot cốt lõi: điều phối LLM, gọi Tools, lưu session (Storage).

## API

- **POST** `/api/chat` – Gửi tin nhắn, nhận phản hồi (session_id, message)
- **GET** `/api/sessions/{session_id}/messages` – Lịch sử hội thoại
- **POST** `/api/sessions` – Tạo session mới
- **GET** `/health`, `/ready` – Health check

## Chạy local

1. Chạy **Tools** trước (port 8081).
2. Tạo file `.env` (xem `.env.example` ở root), đặt `OPENAI_API_KEY`, `TOOLS_BASE_URL=http://localhost:8081`.
3. Chạy:

```bash
cd Backend/chatbot
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080
```

## Biến môi trường

| Biến | Mô tả |
|------|--------|
| `OPENAI_API_KEY` | API key OpenAI (bắt buộc cho LLM) |
| `OPENAI_MODEL` | Model (mặc định gpt-4o-mini) |
| `TOOLS_BASE_URL` | URL dịch vụ Tools (ví dụ http://localhost:8081) |
| `STORAGE_BACKEND` | local hoặc gcs |
| `LOCAL_STORAGE_PATH` | Thư mục lưu session khi dùng local |

## Docker

```bash
docker build -t chatbot-api .
docker run -p 8080:8080 -e OPENAI_API_KEY=xxx -e TOOLS_BASE_URL=http://host.docker.internal:8081 chatbot-api
```

## Triển khai Cloud Run

Deploy sau khi Tools đã có URL; cấu hình `TOOLS_BASE_URL` trỏ tới service Tools.
