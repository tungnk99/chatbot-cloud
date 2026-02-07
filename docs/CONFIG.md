# Cấu Hình – Chatbot Cloud

Tài liệu cấu hình biến môi trường và Cloud Run.

## Biến môi trường

Tạo file `.env` (local) hoặc cấu hình trên Cloud Run. Tham khảo [.env.example](../.env.example) ở thư mục gốc repo.

### Chatbot (backend/chatbot)

| Biến | Mô tả |
|------|--------|
| `OPENAI_API_KEY` | API key OpenAI (trên Cloud Run dùng Secret Manager) |
| `OPENAI_MODEL` | Model LLM (vd: gpt-4o-mini) |
| `TOOLS_BASE_URL` | URL dịch vụ Tools (vd: http://localhost:8081) |
| `STORAGE_BACKEND` | `local` hoặc `gcs` |
| `LOCAL_STORAGE_PATH` | Đường dẫn lưu session khi dùng local |
| `GCS_BUCKET` | Tên bucket GCS khi dùng gcs |
| `USE_PUBSUB_ASYNC` | Bật xử lý chat bất đồng bộ qua Pub/Sub (tránh treo khi LLM nặng) | false (local), true (Terraform set) |
| `PUBSUB_TOPIC` | Topic Pub/Sub (vd: projects/PROJECT_ID/topics/chat-requests) | "" |

### Frontend

| Biến | Mô tả |
|------|--------|
| `CHATBOT_API_URL` | URL Chatbot API (vd: http://localhost:8080) |

### Tools (backend/tools)

Không cần biến môi trường đặc biệt cho chạy cơ bản.

---

## Cấu hình Cloud Run (Terraform)

Các biến trong [infrastructure/terraform/terraform.tfvars.example](../infrastructure/terraform/terraform.tfvars.example):

| Biến | Mặc định | Mô tả |
|------|----------|--------|
| `chatbot_min_instances` | 0 | Scale to zero khi không traffic |
| `chatbot_max_instances` | 10 | Số instance tối đa Chatbot |
| `tools_min_instances` | 0 | Min instances Tools |
| `tools_max_instances` | 10 | Max instances Tools |
| `frontend_min_instances` | 0 | Min instances Frontend |
| `frontend_max_instances` | 5 | Max instances Frontend |
| `chatbot_memory_mi` | 512Mi | RAM Chatbot |
| `chatbot_cpu` | 1 | CPU Chatbot |
| `allow_unauthenticated` | true | Cho phép gọi không auth (demo) |
| `cors_origins` | "" | CORS allow_origins cho Chatbot |

Sửa `terraform.tfvars` rồi chạy `terraform apply` để áp dụng.
