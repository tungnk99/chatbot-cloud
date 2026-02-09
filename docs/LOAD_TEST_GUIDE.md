# HƯỚNG DẪN CHẠY LOAD TEST VÀ THU THẬP SỐ LIỆU

Tài liệu này hướng dẫn cách chạy load test và thu thập số liệu để cập nhật vào báo cáo.

---

## 1. CHUẨN BỊ

### 1.1. Cài đặt dependencies

```bash
# Cài đặt load test dependencies
pip install -r tests/load/requirements.txt
```

### 1.2. Khởi động services

**Option 1: Local (để test)**
```bash
# Terminal 1: Tools service
cd backend/tools
uvicorn main:app --port 8081

# Terminal 2: Chatbot service  
cd backend/chatbot
uvicorn main:app --port 8080

# Terminal 3: Frontend (optional)
cd frontend
streamlit run app.py
```

**Option 2: GCP (production)**
```bash
# Lấy URLs từ Terraform
cd infrastructure/terraform
terraform output cloud_run_chatbot_url
terraform output cloud_run_tools_url
```

---

## 2. CHẠY LOAD TESTS

### 2.1. Test Tools Service

```bash
# Test với pytest (nhanh, CLI)
TOOLS_URL=http://localhost:8081 \
LOAD_NUM_REQUESTS=100 \
LOAD_NUM_WORKERS=20 \
pytest tests/load/test_load_tools.py -v -s

# Ghi chú kết quả:
# - [Chatbot /health] requests=..., ok=..., avg_ms=..., rps=...
# - [Tools /tools/interest] requests=..., ok=..., avg_ms=..., rps=...
# - [Tools /tools/savings-rate] requests=..., ok=..., avg_ms=..., rps=...
```

**Cập nhật vào REPORT.md, Section 7.2.3.A:**
- Điền số liệu vào bảng Tools Service Performance

### 2.2. Test Chatbot Service

```bash
# Test với pytest
CHATBOT_URL=http://localhost:8080 \
LOAD_NUM_REQUESTS=50 \
LOAD_NUM_WORKERS=10 \
pytest tests/load/test_load_chatbot.py -v -s

# Ghi chú kết quả:
# - [Chatbot /health] requests=..., ok=..., avg_ms=..., rps=...
# - [Chatbot /api/sessions] requests=..., ok=..., avg_ms=..., rps=...
# - [Chatbot /api/chat] requests=..., ok=..., avg_ms=..., rps=...
```

**Cập nhật vào REPORT.md, Section 7.2.3.B:**
- Điền số liệu vào bảng Chatbot Service Performance

### 2.3. Test với Locust (Interactive)

#### A. Khởi động Locust

```bash
# Test Chatbot
locust -f tests/load/locustfile.py --host=http://localhost:8080

# Hoặc test Tools
locust -f tests/load/locustfile.py --host=http://localhost:8081
```

#### B. Mở Web UI

- Truy cập: http://localhost:8089
- Cấu hình test:
  - **Number of users:** 50
  - **Spawn rate:** 5 users/second
  - **Host:** http://localhost:8080 (hoặc GCP URL)
  - **Run time:** 5 minutes

#### C. Thu thập số liệu

Sau khi test xong, ghi chú các metrics:

**Từ Locust UI:**
- Total Requests
- Failures
- Median Response Time
- 95th Percentile
- Average Response Time
- Requests/s (RPS)
- Min/Max Response Time

**Cập nhật vào REPORT.md:**
- Section 7.2.3.A: Tools Service Performance
- Section 7.2.3.B: Chatbot Service Performance

---

## 3. AUTO-SCALING TEST

### 3.1. Kịch bản: Tăng tải dần

```bash
# Chạy Locust với ramping users
locust -f tests/load/locustfile.py \
  --host=http://localhost:8080 \
  --headless \
  --users 100 \
  --spawn-rate 1 \
  --run-time 5m \
  --csv=results/autoscale_test
```

### 3.2. Theo dõi Cloud Run instances

**Trong GCP Console:**
1. Vào Cloud Run → chọn service (chatbot-api)
2. Tab "Metrics"
3. Xem "Instance count" graph

**Hoặc dùng gcloud:**
```bash
# Xem metrics realtime
gcloud run services describe chatbot-api \
  --region=asia-southeast1 \
  --format="value(status.traffic[0].latestRevision)"

# Hoặc dùng Cloud Monitoring
```

### 3.3. Ghi chú kết quả

Ghi lại theo thời gian:

| Thời điểm | Users | Instances | Avg Response Time | RPS |
|-----------|-------|-----------|-------------------|-----|
| 0s        | 0     | ?         | -                 | 0   |
| 30s       | 25    | ?         | ?ms               | ?   |
| 60s       | 50    | ?         | ?ms               | ?   |
| 90s       | 75    | ?         | ?ms               | ?   |
| 120s      | 100   | ?         | ?ms               | ?   |

**Cập nhật vào REPORT.md, Section 7.2.3.C**

---

## 4. STRESS TEST

### 4.1. Chạy stress test

```bash
# High load: 200 users, 10 phút
locust -f tests/load/locustfile.py \
  --host=http://localhost:8080 \
  --headless \
  --users 200 \
  --spawn-rate 10 \
  --run-time 10m \
  --csv=results/stress_test
```

### 4.2. Thu thập metrics

Sau khi test xong, check file CSV:
- `results/stress_test_stats.csv`
- `results/stress_test_failures.csv`

Tính toán:
- Total Requests = sum of all requests
- Success Rate = (Total - Failures) / Total * 100%
- Failed Requests = count of failures
- Avg Response Time = average từ CSV
- Max Instances = check từ GCP Console

**Cập nhật vào REPORT.md, Section 7.2.3.D**

---

## 5. TEMPLATE GHI CHÚ KẾT QUẢ

### 5.1. Tools Service Performance

```
Endpoint: /health
- Requests: ___
- Success Rate: ___%
- Avg Latency: ___ms
- P95 Latency: ___ms
- RPS: ___

Endpoint: /tools/interest
- Requests: ___
- Success Rate: ___%
- Avg Latency: ___ms
- P95 Latency: ___ms
- RPS: ___

Endpoint: /tools/savings-rate
- Requests: ___
- Success Rate: ___%
- Avg Latency: ___ms
- P95 Latency: ___ms
- RPS: ___
```

### 5.2. Chatbot Service Performance

```
Endpoint: /health
- Requests: ___
- Success Rate: ___%
- Avg Latency: ___ms
- P95 Latency: ___ms
- RPS: ___

Endpoint: /api/sessions
- Requests: ___
- Success Rate: ___%
- Avg Latency: ___ms
- P95 Latency: ___ms
- RPS: ___

Endpoint: /api/chat (sync)
- Requests: ___
- Success Rate: ___%
- Avg Latency: ___s
- P95 Latency: ___s
- RPS: ___

Endpoint: /api/chat (async)
- Requests: ___
- Success Rate: ___%
- Avg Latency: ___ms
- P95 Latency: ___ms
- RPS: ___
```

### 5.3. Auto-scaling Test

```
Thời điểm | Users | Instances | Avg Response Time | RPS
----------|-------|-----------|-------------------|-----
0s        | 0     | ___       | -                 | 0
30s       | 25    | ___       | ___ms             | ___
60s       | 50    | ___       | ___ms             | ___
90s       | 75    | ___       | ___ms             | ___
120s      | 100   | ___       | ___ms             | ___

Scale down:
180s      | 50    | ___       | ___ms             | -
240s      | 10    | ___       | ___ms             | -
300s      | 0     | ___       | -                 | -
```

### 5.4. Stress Test

```
Total Requests: _____
Success Rate: ____%
Failed Requests: ___ (timeout/rate limit)
Avg Response Time: ___s
Max Instances: ___
Error Rate: ____%
```

---

## 6. TIPS & TROUBLESHOOTING

### 6.1. Tips

1. **Chạy test nhiều lần** để lấy số liệu trung bình
2. **Warm up** service trước khi test (gửi vài request)
3. **Test trên GCP** để có số liệu thực tế về auto-scaling
4. **Ghi chú môi trường test:**
   - Local hay GCP?
   - Machine specs (nếu local)
   - Cloud Run config (CPU, memory, max instances)

### 6.2. Troubleshooting

**Lỗi: Connection refused**
```bash
# Check service đang chạy
curl http://localhost:8080/health
curl http://localhost:8081/health
```

**Lỗi: Timeout**
```bash
# Tăng timeout trong test
# Hoặc giảm số concurrent users
```

**Lỗi: Rate limit (429)**
```bash
# Giảm spawn rate
# Hoặc tăng max instances trong Cloud Run config
```

**Lỗi: LLM API timeout**
```bash
# Sử dụng async endpoint
# Hoặc tăng timeout trong chatbot config
```

---

## 7. CHECKLIST

Sau khi chạy xong tất cả tests:

- [ ] Đã chạy pytest load test cho Tools service
- [ ] Đã chạy pytest load test cho Chatbot service
- [ ] Đã chạy Locust interactive test
- [ ] Đã test auto-scaling (nếu trên GCP)
- [ ] Đã chạy stress test
- [ ] Đã ghi chú tất cả số liệu
- [ ] Đã cập nhật vào REPORT.md Section 7.2.3
- [ ] Đã screenshot Locust UI (optional, để báo cáo)
- [ ] Đã screenshot GCP Metrics (optional, để báo cáo)

---

## 8. CẬP NHẬT VÀO REPORT.MD

Sau khi có đủ số liệu, mở file `docs/REPORT.md` và:

1. Tìm **Section 7.2.3** (Kết quả)
2. Thay thế các số liệu mẫu bằng số liệu thực tế
3. Cập nhật **Section 7.1** (Unit Tests) nếu đã chạy unit tests
4. Cập nhật **Section 7.5** (Cost Analysis) nếu có số liệu thực tế từ GCP billing

**Lưu ý:** 
- Các số liệu hiện tại trong REPORT.md là **MẪU** để tham khảo
- Bạn cần thay thế bằng số liệu thực tế từ load tests
- Ghi rõ môi trường test (local/GCP, config, etc.)

---

**Good luck with your load testing!** 🚀
