# Load tests (Test tải)

Test tải cho **Chatbot API** và **Tools API**: đo throughput (RPS), latency dưới nhiều request đồng thời.

## Cách 1: Locust (giao diện web, ramp-up user)

### Cài đặt

```bash
pip install -r tests/load/requirements.txt
```

### Chạy

1. **Chạy Chatbot và Tools** (localhost hoặc URL deploy):

   ```bash
   # Terminal 1: Tools
   cd backend/tools && uvicorn main:app --port 8081
   # Terminal 2: Chatbot
   cd backend/chatbot && uvicorn main:app --port 8080
   ```

2. **Khởi động Locust** (từ root repo):

   ```bash
   # Test Chatbot
   locust -f tests/load/locustfile.py --host=http://localhost:8080

   # Hoặc test Tools
   locust -f tests/load/locustfile.py --host=http://localhost:8081
   ```

   Mặc định Locust dùng class user đầu tiên (`ChatbotUser`). Để chọn **Tools**:
   dùng web UI (port 8089) chọn "ToolsUser" hoặc chạy headless:

   ```bash
   locust -f tests/load/locustfile.py --host=http://localhost:8081 --user ToolsUser --headless -u 20 -r 5 -t 60s
   ```

3. **Mở giao diện**: http://localhost:8089  
   Nhập số user, spawn rate, Start → xem báo cáo (RPS, latency, lỗi).

### Biến môi trường

| Biến | Mô tả | Mặc định |
|------|--------|----------|
| `CHATBOT_URL` | Base URL Chatbot API | http://localhost:8080 |
| `TOOLS_URL` | Base URL Tools API | http://localhost:8081 |

Ví dụ test môi trường GCP:

```bash
export CHATBOT_URL=https://chatbot-api-xxx.run.app
export TOOLS_URL=https://chatbot-tools-xxx.run.app
locust -f tests/load/locustfile.py --host=$CHATBOT_URL
```

---

## Cách 2: Pytest (script, CI)

Chạy nhanh không cần UI, phù hợp CI hoặc đo nhanh RPS/latency.

### Chạy

```bash
# Cần Tools đang chạy (port 8081)
TOOLS_URL=http://localhost:8081 pytest tests/load/test_load_tools.py -v -s

# Cần Chatbot (+ Tools) đang chạy
CHATBOT_URL=http://localhost:8080 pytest tests/load/test_load_chatbot.py -v -s
```

### Biến môi trường

| Biến | Mô tả | Mặc định |
|------|--------|----------|
| `CHATBOT_URL` | Chatbot API | http://localhost:8080 |
| `TOOLS_URL` | Tools API | http://localhost:8081 |
| `LOAD_NUM_REQUESTS` | Số request mỗi test | 50 (Tools), 20 (Chatbot) |
| `LOAD_NUM_WORKERS` | Số thread đồng thời | 10 (Tools), 5 (Chatbot) |
| `SKIP_LOAD_TEST` | Set `=1` để bỏ qua load test (ví dụ trong CI) | (không set) |

Ví dụ tải nặng hơn:

```bash
LOAD_NUM_REQUESTS=200 LOAD_NUM_WORKERS=20 pytest tests/load/test_load_tools.py -v -s
```

---

## Kịch bản

- **ChatbotUser (Locust)**: health, tạo session, get messages, **chat** (gửi tin nhắn).
- **ToolsUser (Locust)**: health, **/tools/interest**, **/tools/savings-rate**.
- **pytest**: gửi N request đồng thời (health, interest, savings-rate, sessions, chat), in avg latency (ms) và RPS.
