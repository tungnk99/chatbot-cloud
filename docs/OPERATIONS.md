# Vận Hành – Scaling, Giám Sát, Bảo Mật

Tài liệu vận hành hệ thống Chatbot Cloud: auto-scaling, monitoring, logging, bảo mật.

---

## Khả năng mở rộng (Auto-Scaling)

### Chiến lược

Hệ thống tự động scale dựa trên:

- **Request per second (RPS)** – Số lượng request đến
- **CPU utilization** – Mức sử dụng CPU
- **Memory usage** – Mức sử dụng RAM
- **Concurrent requests** – Số request đồng thời

### Hành vi scale (mặc định)

| Tải | Số instance (gợi ý) |
|-----|----------------------|
| Tải thấp (0–10 users) | 0–1 (scale to zero) |
| Tải trung bình (10–50) | 1–3 |
| Tải cao (50–100) | 3–6 |
| Tải rất cao (>100) | 6–10 (max) |

### Scale to zero

- Không traffic ~15 phút → Cloud Run scale về 0 instances.
- Chi phí = $0 khi không có người dùng.
- Cold start: 1–3 giây khi có request đầu tiên.

### Tối ưu hiệu năng

- **Concurrency**: 80 requests/instance (cấu hình Cloud Run).
- **Keep-alive**: Giảm latency cho LLM calls.
- **Async**: Xử lý non-blocking cho I/O.

Cấu hình min/max instances: xem [CONFIG.md](CONFIG.md).

---

## Giám sát và logging

### Cloud Monitoring

Các metric thường theo dõi:

- **Request count** – Tổng số request
- **Request latency** – P50, P95, P99
- **Error rate** – Tỷ lệ 4xx, 5xx
- **Instance count** – Số instance đang chạy
- **CPU/Memory** – Mức sử dụng tài nguyên
- **Costs** – Chi phí thực tế

### Logging

```bash
# Xem logs gần nhất
gcloud run services logs read chatbot --limit 50 --format json

# Chỉ lỗi
gcloud run services logs read chatbot \
  --filter="severity>=ERROR" \
  --limit 10
```

### Alerting (gợi ý)

- Error rate > 5%
- Latency P95 > 2 giây
- Instance count gần max
- Chi phí vượt ngân sách

---

## Bảo mật

### Authentication & Authorization

- **Cloud IAM** – Quản lý quyền giữa các service
- **Service Accounts** – Mỗi service có SA riêng
- **API Keys** – LLM key lưu trong Secret Manager
- **User Authentication** – OAuth 2.0 / Firebase Auth (tùy chọn)

### Bảo vệ dữ liệu

- **Encryption at rest** – Mã hóa trên Cloud Storage
- **Encryption in transit** – HTTPS/TLS
- **Data retention** – Chính sách xóa dữ liệu (tùy cấu hình)

### Mạng

- **VPC Connector** – Kết nối private (nếu cần)
- **Firewall** – Giới hạn traffic
- **Rate limiting** – Chống DDoS/abuse

### Thực hành

```bash
# Tạo secret (nếu chưa dùng Terraform)
gcloud secrets create openai-api-key --data-file=./key.txt

# Gán quyền cho Service Account
gcloud secrets add-iam-policy-binding openai-api-key \
  --member="serviceAccount:YOUR_SA@YOUR_PROJECT.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

---

## Performance & Chi phí (ước tính)

- **Response time**: 500ms–2s (tùy độ phức tạp)
- **Cold start**: 1–3s
- **Warm requests**: 200–500ms
- **Concurrent users**: 100–1000 (với 10 instances)
- **Throughput**: ~800 requests/phút

**Chi phí ước tính** (vd: 10.000 requests/tháng, 512MB, 1 vCPU, LLM ~$0.002/request):

- Cloud Run: ~$2–5/tháng  
- Cloud Storage: ~$0.5/tháng  
- LLM API: ~$20/tháng  
- Networking: ~$0.5/tháng  
- **Tổng**: ~$25/tháng  
