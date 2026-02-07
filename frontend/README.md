# Frontend (Streamlit)

Giao diện chat, gọi Backend Chatbot API.

## Chạy local

1. Chạy **Chatbot** (Backend/chatbot) trước, ví dụ port 8080.
2. Đặt biến môi trường `CHATBOT_API_URL=http://localhost:8080` (hoặc tạo `.env`).
3. Chạy:

```bash
cd Frontend
pip install -r requirements.txt
streamlit run app.py
```

Mở http://localhost:8501 (hoặc port Streamlit báo).

## Biến môi trường

| Biến | Mô tả |
|------|--------|
| `CHATBOT_API_URL` | URL Chatbot API (mặc định http://localhost:8080) |

## Docker

```bash
docker build -t chatbot-frontend .
docker run -p 8080:8080 -e CHATBOT_API_URL=http://host.docker.internal:8080 chatbot-frontend
```

Truy cập http://localhost:8080.

## Triển khai Cloud Run

Deploy riêng; cấu hình `CHATBOT_API_URL` trỏ tới URL Chatbot service.
