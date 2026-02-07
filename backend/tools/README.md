# Tools Service (Backend/tools)

Microservice tính toán tài chính, triển khai **riêng** trên Cloud Run (Serverless-first).

## API

- **POST** `/tools/interest` – Tính lãi đơn/ghép (principal, rate_percent, months, compound)
- **POST** `/tools/savings-rate` – Tỷ lệ tiết kiệm so với thu nhập (income, savings)
- **GET** `/health`, `/ready` – Health check

## Chạy local

```bash
cd Backend/tools
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8081
```

## Docker

```bash
docker build -t chatbot-tools .
docker run -p 8081:8080 chatbot-tools
```

## Biến môi trường

Không bắt buộc. Có thể dùng `PORT` (mặc định 8080) cho Cloud Run.

## Triển khai Cloud Run

Deploy độc lập; Chatbot gọi qua `TOOLS_BASE_URL`.
