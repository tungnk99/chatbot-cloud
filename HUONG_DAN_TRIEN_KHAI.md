# Hướng dẫn triển khai Chatbot Cloud

Tài liệu này hướng dẫn triển khai hệ thống Chatbot Cloud lên Google Cloud Platform từ đầu đến cuối, dựa trên kinh nghiệm thực tế.

---

## Mục lục

- [Quick Start (10-15 phút)](#quick-start-10-15-phút)
- [Hướng dẫn chi tiết](#hướng-dẫn-chi-tiết)
  - [1. Chuẩn bị](#1-chuẩn-bị)
  - [2. Triển khai (6 bước)](#2-triển-khai-6-bước)
  - [3. Kiểm tra triển khai](#3-kiểm-tra-triển-khai)
  - [4. Lỗi thường gặp](#4-lỗi-thường-gặp)
  - [5. Checklist sau triển khai](#5-checklist-sau-triển-khai)
  - [6. Lệnh hữu ích](#6-lệnh-hữu-ích)
  - [7. Tips và lưu ý](#7-tips-và-lưu-ý)
- [Troubleshooting nhanh](#troubleshooting-nhanh)

---

## Quick Start (10-15 phút)

### Yêu cầu

- [x] Đã cài: `git`, `gcloud`, `terraform` (>= 1.0)
- [x] Có GCP project với Billing đã bật
- [x] Có OpenAI API key (dạng `sk-proj-...`)

### Triển khai (6 lệnh)

```bash
# 1. Clone repo
git clone <URL_REPO>
cd chatbot-cloud

# 2. Đăng nhập GCP
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud auth application-default login  # ⚠️ QUAN TRỌNG - dùng tài khoản Owner/Editor

# 3. Cấu hình Terraform
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars
# Sửa trong terraform.tfvars:
#   - project_id = "your-project-id"
#   - openai_api_key_secret = "sk-proj-..."

# 4. Tạo hạ tầng
terraform init
terraform apply  # Gõ yes

# 5. Build Docker images (đợi 3-5 phút)
cd ../../
gcloud builds submit --config=cloudbuild.yaml .

# 6. Apply lại Terraform (nếu bước 4 báo thiếu image)
cd infrastructure/terraform
terraform apply  # Gõ yes
```

### Lấy URL và truy cập

```bash
cd infrastructure/terraform
terraform output cloud_run_frontend_url
```

Mở URL trên trình duyệt để sử dụng chatbot.

**Thời gian**: ~10-15 phút  
**Chi phí ước tính**: ~$5-20/tháng (demo/dev)

---

## Hướng dẫn chi tiết

### 1. Chuẩn bị

#### 1.1 Công cụ cần cài

Kiểm tra các công cụ:

```bash
git --version        # Cần: 2.x trở lên
gcloud --version     # Cần: mới nhất
terraform --version  # Cần: >= 1.0
```

Nếu chưa có, cài đặt:
- **Git**: https://git-scm.com/
- **gcloud CLI**: https://cloud.google.com/sdk/docs/install
- **Terraform**: https://www.terraform.io/downloads

#### 1.2 Tài khoản GCP

- Tài khoản Google Cloud với **Billing đã bật**
- Project GCP (tạo mới hoặc dùng có sẵn)
- Tài khoản cần có quyền **Owner** hoặc **Editor** trên project

Kiểm tra billing:
- Vào [Console GCP](https://console.cloud.google.com) → **Billing** → đảm bảo project đã link với tài khoản thanh toán

#### 1.3 OpenAI API Key

- Key dạng `sk-proj-...` hoặc `sk-...`
- Lấy từ: https://platform.openai.com/api-keys
- Giữ bí mật, không commit vào Git

---

### 2. Triển khai (6 bước)

#### Bước 1: Clone repo

```bash
git clone <URL_REPO>
cd chatbot-cloud
```

#### Bước 2: Đăng nhập GCP

```bash
# Đăng nhập tài khoản có quyền Owner/Editor
gcloud auth login

# Chọn project
gcloud config set project YOUR_PROJECT_ID

# ⚠️ QUAN TRỌNG: Đăng nhập Application Default Credentials
gcloud auth application-default login
```

**Lưu ý quan trọng**: Bước `gcloud auth application-default login` rất quan trọng để Terraform có đủ quyền tạo tài nguyên. Phải đăng nhập bằng tài khoản có quyền **Owner** hoặc **Editor**.

#### Bước 3: Cấu hình Terraform

```bash
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars
```

Mở file `terraform.tfvars` và chỉnh sửa:

```hcl
project_id = "your-project-id"  # Thay bằng Project ID thật
region     = "asia-southeast1"   # Có thể đổi region khác

# Điền OpenAI key (hoặc bỏ trống, thêm thủ công sau)
openai_api_key_secret = "sk-proj-..."
```

**Lưu ý**: File `terraform.tfvars` không được commit vào Git (đã có trong `.gitignore`).

#### Bước 4: Chạy Terraform

```bash
terraform init
terraform plan    # Xem trước thay đổi (tùy chọn)
terraform apply   # Tạo hạ tầng
```

Gõ `yes` khi được hỏi. Terraform sẽ tạo:

- **APIs**: Cloud Run, Storage, Secret Manager, Artifact Registry, Pub/Sub, IAM, Cloud Build
- **GCS bucket**: Lưu lịch sử chat
- **Secret Manager**: Lưu OpenAI key
- **Artifact Registry**: Lưu Docker images
- **Service Account**: IAM cho Cloud Run
- **Pub/Sub**: Topic và subscription cho xử lý bất đồng bộ

**⚠️ Lưu ý**: Lần đầu `terraform apply` có thể báo lỗi thiếu Docker image → bình thường, chuyển sang Bước 5.

#### Bước 5: Build và push Docker images

Quay lại **thư mục gốc** repo:

```bash
cd ../../
# Hoặc: cd /path/to/chatbot-cloud

gcloud builds submit --config=cloudbuild.yaml .
```

Lệnh này sẽ:
- Build 3 Docker images: `tools`, `chatbot`, `frontend`
- Push lên Artifact Registry
- Đợi khoảng **3-5 phút**

Theo dõi tiến trình trên terminal hoặc [Cloud Build Console](https://console.cloud.google.com/cloud-build/builds).

#### Bước 6: Apply lại Terraform (nếu cần)

Nếu Bước 4 báo lỗi thiếu image, sau khi build xong chạy:

```bash
cd infrastructure/terraform
terraform apply
```

Lần này Terraform sẽ tạo thành công 3 Cloud Run services: `chatbot-tools`, `chatbot-api`, `chatbot-frontend`.

---

### 3. Kiểm tra triển khai

#### 3.1 Lấy URL

```bash
cd infrastructure/terraform
terraform output cloud_run_frontend_url
terraform output cloud_run_chatbot_url
terraform output cloud_run_tools_url
```

Kết quả sẽ giống:
```
cloud_run_frontend_url = "https://chatbot-frontend-xxxxx-as.a.run.app"
cloud_run_chatbot_url = "https://chatbot-api-xxxxx-as.a.run.app"
cloud_run_tools_url = "https://chatbot-tools-xxxxx-as.a.run.app"
```

#### 3.2 Kiểm tra health APIs

```bash
# Tools API
curl $(terraform output -raw cloud_run_tools_url)/health

# Chatbot API
curl $(terraform output -raw cloud_run_chatbot_url)/health
```

Kết quả mong đợi: `{"status":"ok"}`

#### 3.3 Mở giao diện web

Mở URL từ `cloud_run_frontend_url` trên trình duyệt:

```
https://chatbot-frontend-xxxxx-as.a.run.app
```

Thử gửi tin nhắn để test chatbot:
- "Xin chào"
- "Tính lãi kép cho 10 triệu đồng, lãi suất 5%/năm, kỳ hạn 3 năm"
- "So sánh tỷ lệ tiết kiệm giữa tiết kiệm 2 triệu/tháng và 5 triệu/tháng"

---

### 4. Lỗi thường gặp

#### Lỗi 1: Permission denied (403) khi `terraform apply`

**Triệu chứng:**
```
Error 403: Permission denied to list services for consumer container
Error 403: Permission 'iam.serviceAccounts.create' denied
```

**Nguyên nhân**: Tài khoản không đủ quyền trên project.

**Cách xử lý:**

1. Đảm bảo dùng tài khoản có quyền **Owner** hoặc **Editor**
2. Chạy lại:
   ```bash
   gcloud auth application-default login
   ```
   Đăng nhập bằng tài khoản có quyền
3. Chạy lại:
   ```bash
   terraform apply
   ```

**Nếu project do trường/tổ chức quản lý**: Nhờ admin:
- Cấp quyền **Owner** hoặc **Editor** cho tài khoản của bạn, hoặc
- Chạy Terraform giúp bằng tài khoản có quyền

---

#### Lỗi 2: Memory 256Mi không đủ cho Cloud Run

**Triệu chứng:**
```
Error 400: Invalid value specified for memory. 
Total memory < 512 Mi is not supported with cpu always allocated (unthrottled).
```

**Nguyên nhân**: Cloud Run yêu cầu tối thiểu 512Mi memory.

**Cách xử lý**: Đã fix sẵn trong code. Nếu vẫn gặp, kiểm tra file `infrastructure/terraform/cloudrun_*.tf`:

```hcl
resources {
  limits = {
    cpu    = "1"
    memory = "512Mi"  # Phải >= 512Mi
  }
}
```

---

#### Lỗi 3: Image not found khi tạo Cloud Run

**Triệu chứng:**
```
Error: Image 'asia-southeast1-docker.pkg.dev/.../tools:latest' not found
Error waiting to create Service: Image not found
```

**Nguyên nhân**: Chưa build và push Docker images lên Artifact Registry.

**Cách xử lý:**

1. Build images:
   ```bash
   cd /path/to/chatbot-cloud
   gcloud builds submit --config=cloudbuild.yaml .
   ```
2. Đợi build hoàn thành (3-5 phút)
3. Apply lại Terraform:
   ```bash
   cd infrastructure/terraform
   terraform apply
   ```

---

#### Lỗi 4: OpenAI API Key không hoạt động

**Triệu chứng**: Chatbot không trả lời, báo lỗi 401/403, hoặc log có lỗi OpenAI authentication.

**Cách xử lý:**

1. Kiểm tra Secret Manager có secret `openai-api-key`:
   ```bash
   gcloud secrets versions list openai-api-key
   ```

2. Nếu chưa có hoặc sai, thêm/cập nhật:
   ```bash
   echo -n "sk-proj-..." | gcloud secrets versions add openai-api-key --data-file=-
   ```

3. Redeploy Cloud Run để load key mới:
   ```bash
   cd infrastructure/terraform
   terraform apply -replace=google_cloud_run_v2_service.chatbot
   ```

4. Kiểm tra Service Account có quyền đọc secret:
   ```bash
   gcloud secrets get-iam-policy openai-api-key
   ```
   Phải có: `serviceAccount:chatbot-sa@PROJECT_ID.iam.gserviceaccount.com` với role `secretmanager.secretAccessor`

---

#### Lỗi 5: Cloud Build bị timeout hoặc treo

**Triệu chứng**: `gcloud builds submit` chạy quá lâu (>10 phút) hoặc không có output mới.

**Cách xử lý:**

1. Kiểm tra log trên Console:
   ```
   https://console.cloud.google.com/cloud-build/builds?project=YOUR_PROJECT_ID
   ```

2. Xem build ID trong terminal output, click vào để xem chi tiết

3. Nếu build fail:
   - Kiểm tra Dockerfile có lỗi syntax không
   - Kiểm tra `requirements.txt` có dependency không tồn tại không
   - Xem log lỗi cụ thể

4. Thử build lại:
   ```bash
   gcloud builds submit --config=cloudbuild.yaml .
   ```

5. Nếu vẫn bị treo, cancel và build lại:
   ```bash
   # Lấy build ID từ output
   gcloud builds cancel BUILD_ID
   gcloud builds submit --config=cloudbuild.yaml .
   ```

---

#### Lỗi 6: Frontend không kết nối được Chatbot

**Triệu chứng**: Mở frontend, gửi tin nhắn nhưng không có phản hồi, hoặc báo lỗi connection.

**Cách xử lý:**

1. Kiểm tra biến môi trường `CHATBOT_API_URL` trong Cloud Run Frontend:
   ```bash
   gcloud run services describe chatbot-frontend --region=asia-southeast1 --format="value(spec.template.spec.containers[0].env)"
   ```

2. Đảm bảo `CHATBOT_API_URL` trỏ đúng URL Chatbot API

3. Kiểm tra Cloud Run Chatbot đang chạy:
   ```bash
   gcloud run services describe chatbot-api --region=asia-southeast1
   ```

4. Redeploy Frontend:
   ```bash
   cd infrastructure/terraform
   terraform apply -replace=google_cloud_run_v2_service.frontend
   ```

---

### 5. Checklist sau triển khai

Đảm bảo tất cả các mục sau đã hoàn thành:

- [ ] `terraform apply` thành công, không có lỗi
- [ ] Cloud Build hoàn thành, 3 images được push lên Artifact Registry
- [ ] 3 Cloud Run services đã tạo: `chatbot-tools`, `chatbot-api`, `chatbot-frontend`
- [ ] Health check Tools API: `curl <tools_url>/health` → `{"status":"ok"}`
- [ ] Health check Chatbot API: `curl <chatbot_url>/health` → `{"status":"ok"}`
- [ ] Mở Frontend URL trên trình duyệt, thấy giao diện chat Streamlit
- [ ] Gửi tin nhắn test, chatbot phản hồi bình thường
- [ ] OpenAI key đã lưu trong Secret Manager (không commit vào Git)
- [ ] File `terraform.tfvars` không bị commit (kiểm tra `.gitignore`)
- [ ] Ghi lại các URL: Frontend, Chatbot API, Tools API
- [ ] (Tùy chọn) Thêm Cloud Logging filter để monitor errors

---

### 6. Lệnh hữu ích

#### Xem log Cloud Run

```bash
# Log Chatbot (50 dòng gần nhất)
gcloud run services logs read chatbot-api --region=asia-southeast1 --limit=50

# Log Frontend
gcloud run services logs read chatbot-frontend --region=asia-southeast1 --limit=50

# Log Tools
gcloud run services logs read chatbot-tools --region=asia-southeast1 --limit=50

# Theo dõi log real-time (stream)
gcloud run services logs tail chatbot-api --region=asia-southeast1
```

#### Xem thông tin service

```bash
# Chatbot API
gcloud run services describe chatbot-api --region=asia-southeast1

# Frontend
gcloud run services describe chatbot-frontend --region=asia-southeast1

# Tools
gcloud run services describe chatbot-tools --region=asia-southeast1
```

#### Xem danh sách images trong Artifact Registry

```bash
gcloud artifacts docker images list asia-southeast1-docker.pkg.dev/PROJECT_ID/chatbot-cloud
```

#### Redeploy service (sau khi thay đổi code)

```bash
# 1. Build image mới
cd /path/to/chatbot-cloud
gcloud builds submit --config=cloudbuild.yaml .

# 2. Update Cloud Run bằng Terraform
cd infrastructure/terraform
terraform apply

# Hoặc force replace một service cụ thể
terraform apply -replace=google_cloud_run_v2_service.chatbot
```

#### Xem thông tin Terraform outputs

```bash
cd infrastructure/terraform

# Tất cả outputs
terraform output

# Output cụ thể (không có quotes)
terraform output -raw cloud_run_frontend_url
terraform output -raw cloud_run_chatbot_url
terraform output -raw cloud_run_tools_url
```

#### Kiểm tra Secret Manager

```bash
# List secrets
gcloud secrets list

# Xem versions của secret
gcloud secrets versions list openai-api-key

# Xem IAM policy của secret
gcloud secrets get-iam-policy openai-api-key
```

#### Xóa toàn bộ hạ tầng

```bash
cd infrastructure/terraform
terraform destroy
```

**⚠️ Cảnh báo**: Lệnh này sẽ xóa tất cả:
- Cloud Run services
- GCS bucket và data bên trong
- Secret Manager secrets
- Artifact Registry repo và images
- Service Account
- Pub/Sub topic và subscription

Dữ liệu sẽ **KHÔNG THỂ** khôi phục được.

---

### 7. Tips và lưu ý

#### 7.1 Chi phí

Cloud Run pricing:
- **Request**: $0.40 / triệu requests
- **CPU time**: $0.00002400 / vCPU-giây
- **Memory**: $0.00000250 / GiB-giây
- **Networking**: $0.12 / GB (egress)

GCS pricing:
- **Storage**: ~$0.020 / GB / tháng (Standard class, asia-southeast1)

Artifact Registry:
- **Storage**: $0.10 / GB / tháng

**Ước tính cho demo/dev** (tải thấp):
- Cloud Run: ~$2-5/tháng
- GCS: ~$0.10-0.50/tháng (tùy số session)
- Artifact Registry: ~$0.20/tháng
- **Tổng**: ~$5-20/tháng

**Tiết kiệm chi phí**:
- Scale to zero khi không dùng (mặc định `min_instances = 0`)
- Xóa old images trong Artifact Registry
- Dọn dẹp old sessions trong GCS bucket

#### 7.2 Bảo mật

**Không được**:
- Commit `terraform.tfvars` vào Git (đã có trong `.gitignore`)
- Để OpenAI key trong code hoặc log
- Share OpenAI key qua email/Slack/chat

**Nên làm**:
- Dùng Secret Manager để lưu tất cả secrets
- Tắt `allow_unauthenticated = true` nếu không muốn public:
  ```hcl
  # Trong terraform.tfvars
  allow_unauthenticated = false
  ```
- Dùng Cloud Armor cho DDoS protection (nâng cao)
- Enable Cloud Audit Logs để track access

#### 7.3 Scale

Mặc định:
- **Chatbot**: min 0, max 10 instances
- **Tools**: min 0, max 10 instances
- **Frontend**: min 0, max 5 instances

Thay đổi trong `terraform.tfvars`:

```hcl
# Luôn có 1 instance (tránh cold start, tăng chi phí)
chatbot_min_instances = 1
chatbot_max_instances = 20  # Scale lên tối đa 20 khi có tải cao

tools_min_instances = 1
tools_max_instances = 10

frontend_min_instances = 1
frontend_max_instances = 10
```

Sau khi chỉnh sửa:
```bash
cd infrastructure/terraform
terraform apply
```

#### 7.4 Region

Mặc định: `asia-southeast1` (Singapore)

Các region phổ biến khác:
- `asia-east1` (Đài Loan)
- `us-central1` (Iowa, Mỹ)
- `europe-west1` (Bỉ)

Thay đổi trong `terraform.tfvars`:

```hcl
region = "asia-east1"  # Gần Việt Nam hơn Singapore
```

**Lưu ý**: 
- Đổi region cần destroy và tạo lại hạ tầng
- Chi phí có thể khác nhau giữa các region

#### 7.5 Monitoring và Logging

**Cloud Logging**: Tất cả logs từ Cloud Run tự động gửi vào Cloud Logging.

Xem log trên Console:
```
https://console.cloud.google.com/logs/query?project=YOUR_PROJECT_ID
```

Filter hữu ích:
```
# Lỗi từ Chatbot
resource.type="cloud_run_revision"
resource.labels.service_name="chatbot-api"
severity>=ERROR

# Request tới Frontend
resource.type="cloud_run_revision"
resource.labels.service_name="chatbot-frontend"
httpRequest.status>=400
```

**Cloud Monitoring**: Tạo dashboard để theo dõi:
- Request count
- Response time
- Error rate
- Instance count (scaling)

#### 7.6 Backup và Recovery

**GCS Bucket** (lưu sessions):
- Bật versioning (tùy chọn):
  ```bash
  gcloud storage buckets update gs://BUCKET_NAME --versioning
  ```
- Export định kỳ sang bucket khác (backup)

**Artifact Registry** (images):
- Images tự động được giữ
- Xóa old tags thủ công để tiết kiệm chi phí

**Terraform State**:
- Mặc định lưu local (`terraform.tfstate`)
- **Nên** dùng remote backend (GCS) cho team:
  ```hcl
  # Thêm vào infrastructure/terraform/main.tf
  terraform {
    backend "gcs" {
      bucket = "your-terraform-state-bucket"
      prefix = "chatbot-cloud"
    }
  }
  ```

---

## Troubleshooting nhanh

| Vấn đề | Kiểm tra | Xử lý |
|--------|----------|-------|
| Terraform lỗi 403 Permission denied | Quyền tài khoản | `gcloud auth application-default login` với tài khoản Owner/Editor |
| Cloud Run thiếu image | Cloud Build status | `gcloud builds submit --config=cloudbuild.yaml .` |
| Chatbot không trả lời | OpenAI key | `gcloud secrets versions list openai-api-key` + kiểm tra key đúng chưa |
| Frontend không load | Cloud Run status | `gcloud run services describe chatbot-frontend --region=asia-southeast1` |
| Frontend không kết nối Chatbot | Biến môi trường `CHATBOT_API_URL` | Kiểm tra env var, redeploy frontend |
| Cloud Build timeout | Build log | Xem log trên Console, cancel và build lại |
| Chi phí cao bất thường | Monitoring | Kiểm tra request count, instance count, xem có bị spam không |
| Cold start lâu | Min instances | Tăng `min_instances = 1` trong terraform.tfvars |
| Memory hết | Cloud Run metrics | Tăng `memory = "1Gi"` trong cloudrun_*.tf |
| CPU throttle | Cloud Run metrics | Tăng `cpu = "2"` trong cloudrun_*.tf |

---

## Tổng kết

**Những điều quan trọng nhất**:

1. ✅ **Quyền**: Phải dùng tài khoản có quyền Owner/Editor, chạy `gcloud auth application-default login`
2. ✅ **Build images trước**: `gcloud builds submit` trước khi `terraform apply` tạo Cloud Run
3. ✅ **OpenAI key**: Lưu trong Secret Manager, không commit vào Git
4. ✅ **Memory**: Cloud Run cần tối thiểu 512Mi
5. ✅ **Check health**: Luôn test `/health` endpoint sau khi deploy

**Thời gian triển khai**: ~10-15 phút (bao gồm chờ Cloud Build)

**Khi gặp vấn đề**:
1. Đọc lỗi cụ thể trong terminal
2. Tra bảng "Troubleshooting nhanh" ở trên
3. Xem log: `gcloud run services logs read SERVICE_NAME --region=asia-southeast1 --limit=50`
4. Tham khảo thêm: [docs/DEPLOY_GUIDELINE.md](docs/DEPLOY_GUIDELINE.md)

---

*Tài liệu được cập nhật dựa trên triển khai thực tế ngày 09/02/2026 - Project: `chatbot-cloud-n9`*
