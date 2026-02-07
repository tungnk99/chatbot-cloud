# Terraform – Triển khai Chatbot Cloud lên GCP

Triển khai theo kiến trúc [docs/architecture.md](../../docs/architecture.md):

- **Frontend** (Streamlit) → **Chatbot** (Cloud Run) → **LLM** + **Tools** (Cloud Run) + **Storage** (GCS)

## Tạo tài nguyên

| Thành phần | Tài nguyên |
|------------|------------|
| Compute | Cloud Run: `chatbot-tools`, `chatbot-api`, `chatbot-frontend` |
| Storage | GCS bucket: `{project_id}-chatbot-sessions` (chat/sessions/) |
| Pub/Sub | Topic `chat-requests`, subscription push tới Chatbot (khi `enable_pubsub_async = true`) |
| Secret | Secret Manager: `openai-api-key` (OPENAI_API_KEY) |
| Images | Artifact Registry repo: `chatbot-cloud` (tools, chatbot, frontend) |
| IAM | SA `chatbot-sa`: Secret accessor, GCS objectAdmin, Pub/Sub publisher, Run invoker (cho push) |

## Yêu cầu

- [Terraform](https://www.terraform.io/downloads) >= 1.0
- [gcloud](https://cloud.google.com/sdk) đã login và chọn project
- GCP project với Billing bật

## Cách dùng

### 1. Khởi tạo

```bash
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars
# Sửa terraform.tfvars: project_id, (optional) openai_api_key_secret
```

### 2. Tạo OPENAI_API_KEY trong Secret Manager

**Cách A – Truyền qua Terraform (sensitive):**

Trong `terraform.tfvars`:

```hcl
openai_api_key_secret = "sk-your-openai-key"
```

**Cách B – Thêm thủ công sau lần apply đầu:**

```bash
# Sau khi terraform apply xong
echo -n "sk-your-openai-key" | gcloud secrets versions add openai-api-key --data-file=-
```

### 3. Build và push Docker images

Từ **root repo** (có `cloudbuild.yaml`):

```bash
export PROJECT_ID=$(gcloud config get-value project)
export REGION=asia-southeast1

# Build và push 3 images lên Artifact Registry
gcloud builds submit --config=cloudbuild.yaml .
```

Lần đầu cần tạo Artifact Registry repo (Terraform đã tạo). Nếu chưa chạy Terraform thì tạo tay:

```bash
gcloud artifacts repositories create chatbot-cloud \
  --repository-format=docker \
  --location=$REGION
```

### 4. Apply Terraform

```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

Nếu chưa có image (chưa chạy Cloud Build), Cloud Run vẫn tạo service nhưng revision có thể fail. Sau khi push image xong, deploy lại revision mới hoặc chạy `terraform apply` lại.

### 5. Output

Sau `terraform apply`:

```bash
terraform output cloud_run_frontend_url   # URL mở trình duyệt
terraform output cloud_run_chatbot_url
terraform output cloud_run_tools_url
terraform output gcs_bucket_sessions
terraform output pubsub_topic_chat_requests   # (khi enable_pubsub_async = true)
```

## Thứ tự triển khai gợi ý

1. `terraform apply` (tạo APIs, bucket, secret, Artifact Registry, IAM, Cloud Run với image :latest).
2. Thêm version cho secret `openai-api-key` nếu chưa truyền qua tfvars.
3. `gcloud builds submit --config=cloudbuild.yaml .` (build + push 3 images).
4. Nếu Cloud Run báo image chưa tồn tại: đợi build xong rồi `terraform apply` lại hoặc cập nhật revision (redeploy) từ Console.

## Biến (variables)

| Biến | Mô tả | Mặc định |
|------|--------|----------|
| `project_id` | GCP Project ID | (bắt buộc) |
| `region` | Region (Cloud Run, GCS, Artifact Registry) | asia-southeast1 |
| `openai_api_key_secret` | Giá trị OPENAI_API_KEY (Secret Manager) | "" |
| `artifact_registry_repo` | Tên Artifact Registry repo | chatbot-cloud |
| `image_tools`, `image_chatbot`, `image_frontend` | URI image (để trống = dùng :latest từ repo) | "" |
| `allow_unauthenticated` | Cho phép gọi Cloud Run không auth | true |
| `enable_pubsub_async` | Bật Pub/Sub (topic + subscription) cho chat bất đồng bộ | true |
| `api_prefix` | API prefix dùng trong push endpoint Pub/Sub | /api |
| `cors_origins` | CORS allow_origins cho Chatbot (URL Frontend) | "" |

## Backend state (tùy chọn)

Để lưu state trên GCS (tránh mất state, dùng chung team):

1. Tạo bucket: `gsutil mb gs://your-terraform-state-bucket`
2. Trong `versions.tf` bỏ comment block `backend "gcs"` và sửa `bucket`, `prefix`.
3. `terraform init -reconfigure`

## Xóa

```bash
terraform destroy
```

(Lưu ý: xóa Secret Manager secret và GCS bucket có thể cần force.)
