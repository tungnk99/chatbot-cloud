# Hướng Dẫn Triển Khai – Chatbot Cloud

Tài liệu này dành cho **người triển khai mới** (chưa tham gia dự án) khi mang sản phẩm đến khách hàng. Mục tiêu: triển khai hệ thống Chatbot Cloud lên Google Cloud Platform (GCP) từ đầu với các bước rõ ràng, có thể kiểm tra và bàn giao.

---

## Mục lục

1. [Tổng quan dự án](#1-tổng-quan-dự-an)
2. [Yêu cầu trước khi triển khai](#2-yêu-cầu-trước-khi-triển-khai)
3. [Chuẩn bị môi trường](#3-chuẩn-bị-môi-trường)
4. [Triển khai lên GCP (khuyến nghị)](#4-triển-khai-lên-gcp-khuyến-nghị)
5. [Kiểm tra và bàn giao](#5-kiểm-tra-và-bàn-giao)
6. [Triển khai thủ công (không dùng Terraform)](#6-triển-khai-thủ-công-không-dùng-terraform)
7. [Xử lý sự cố](#7-xử-lý-sự-cố)
8. [Tài liệu tham khảo](#8-tài-liệu-tham-khảo)

---

## 1. Tổng quan dự án

**Chatbot Cloud** là hệ thống chatbot thông minh chạy trên GCP, gồm:

| Thành phần | Mô tả |
|------------|--------|
| **Frontend** | Giao diện web (Streamlit) – người dùng chat tại đây |
| **Chatbot** | Dịch vụ điều phối: nhận tin nhắn, gọi LLM, gọi Tools, lưu session |
| **Tools** | Microservice mở rộng (tính lãi suất, tỷ lệ tiết kiệm, v.v.) |
| **Storage** | Cloud Storage (GCS) lưu lịch sử hội thoại |
| **LLM** | OpenAI API (hoặc tương thích) – cần API key |

**Luồng**: User → Frontend → Chatbot → (LLM + Tools + GCS) → trả lời.

Triển khai mặc định dùng **Terraform** (hạ tầng) + **Cloud Build** (build/push Docker image) + **Cloud Run** (chạy 3 service: frontend, chatbot, tools).

---

## 2. Yêu cầu trước khi triển khai

### 2.1 Tài khoản và quyền

- **Google Cloud Platform**: Tài khoản GCP với **Billing** đã bật.
- **Quyền**: Có quyền tạo project hoặc dùng project có sẵn; quyền **Owner** hoặc **Editor** + **Security Admin** (để bật API, tạo Service Account, Secret Manager).

### 2.2 Công cụ cài trên máy triển khai

| Công cụ | Phiên bản tối thiểu | Ghi chú |
|--------|----------------------|--------|
| **Git** | 2.x | Clone repo |
| **Google Cloud SDK (gcloud)** | Mới nhất | [Cài đặt](https://cloud.google.com/sdk/docs/install) |
| **Terraform** | >= 1.0 | [Cài đặt](https://www.terraform.io/downloads) |

### 2.3 Thông tin cần có trước khi bắt đầu

- **GCP Project ID** (đã tạo hoặc sẽ tạo).
- **OpenAI API Key** (dạng `sk-...`) – dùng cho Chatbot gọi LLM.
- (Tùy chọn) **Region** – mặc định `asia-southeast1`.

---

## 3. Chuẩn bị môi trường

### 3.1 Clone repository

```bash
git clone <URL_REPO_CHATBOT_CLOUD>
cd chatbot-cloud
```

*(Thay `<URL_REPO_CHATBOT_CLOUD>` bằng URL thực tế mà khách/team cung cấp.)*

### 3.2 Đăng nhập và chọn project GCP

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 3.3 Bật Billing (nếu chưa)

Vào [Console GCP](https://console.cloud.google.com) → **Billing** → gắn project với tài khoản thanh toán.

### 3.4 Kiểm tra công cụ

```bash
gcloud --version
terraform --version
```

---

## 4. Triển khai lên GCP (khuyến nghị)

Cách này dùng **Terraform** để tạo toàn bộ hạ tầng (API, GCS, Secret Manager, Artifact Registry, IAM, Cloud Run), sau đó **Cloud Build** để build và push Docker image.

### Bước 4.1 – Cấu hình Terraform

```bash
cd infrastructure/terraform
cp terraform.tfvars.example terraform.tfvars
```

Mở `terraform.tfvars` và chỉnh:

```hcl
project_id = "your-gcp-project-id"   # Thay bằng Project ID thực
region     = "asia-southeast1"       # Có thể đổi region khác
```

*(Tùy chọn)* Nếu muốn Terraform tự tạo secret OpenAI key (sensitive):

```hcl
openai_api_key_secret = "sk-your-openai-api-key"
```

Nếu **không** điền `openai_api_key_secret`, bạn sẽ thêm key thủ công ở Bước 4.4.

### Bước 4.2 – Khởi tạo và tạo hạ tầng

```bash
cd infrastructure/terraform
terraform init
terraform plan    # Xem trước thay đổi
terraform apply   # Gõ yes khi được hỏi
```

Sau bước này sẽ có: APIs đã bật, GCS bucket, Secret Manager secret `openai-api-key`, Artifact Registry repo, IAM, 3 Cloud Run service (có thể chưa chạy được nếu chưa có image).

### Bước 4.3 – Thêm OPENAI_API_KEY vào Secret Manager (nếu chưa dùng tfvars)

Nếu bạn **không** điền `openai_api_key_secret` trong `terraform.tfvars`:

```bash
echo -n "sk-your-openai-api-key" | gcloud secrets versions add openai-api-key --data-file=-
```

*(Thay `sk-your-openai-api-key` bằng key thật; giữ nguyên tên secret `openai-api-key`.)*

### Bước 4.4 – Build và push Docker images

Từ **thư mục gốc repo** (nơi có file `cloudbuild.yaml`):

```bash
cd /path/to/chatbot-cloud
gcloud builds submit --config=cloudbuild.yaml .
```

Lệnh này build 3 image (tools, chatbot, frontend) và push lên Artifact Registry. Lần đầu có thể mất vài phút.

### Bước 4.5 – Cập nhật Cloud Run (nếu cần)

Nếu khi `terraform apply` chưa có image, Cloud Run có thể báo lỗi thiếu image. Sau khi `gcloud builds submit` xong:

```bash
cd infrastructure/terraform
terraform apply
```

Hoặc từ GCP Console: Cloud Run → chọn từng service → **Edit & Deploy New Revision** → chọn image `:latest` tương ứng.

### Bước 4.6 – Lấy URL triển khai

```bash
cd infrastructure/terraform
terraform output cloud_run_frontend_url   # URL cho người dùng mở trình duyệt
terraform output cloud_run_chatbot_url
terraform output cloud_run_tools_url
```

**URL chính để bàn giao cho khách**: `cloud_run_frontend_url` – mở link này để dùng chatbot.

---

## 5. Kiểm tra và bàn giao

### 5.1 Kiểm tra nhanh

1. Mở `cloud_run_frontend_url` trên trình duyệt → thấy giao diện chat.
2. Gửi một tin nhắn → có phản hồi từ chatbot (LLM).
3. (Tùy chọn) Gọi trực tiếp health:
   - `curl <cloud_run_chatbot_url>/health`
   - `curl <cloud_run_tools_url>/health`

### 5.2 Checklist bàn giao cho khách hàng

| Nội dung | Trạng thái |
|----------|------------|
| GCP Project ID đã ghi lại | ☐ |
| Frontend URL (để truy cập chatbot) | ☐ |
| Đã kiểm tra chat thử trên Frontend | ☐ |
| OPENAI_API_KEY đã lưu trong Secret Manager (không gửi key qua email/slack) | ☐ |
| Tài liệu: README.md, docs/architecture.md | ☐ |
| Hướng dẫn thay đổi region/scale (terraform.tfvars) nếu khách cần | ☐ |

### 5.3 Thông tin nên giao cho khách (ví dụ)

- **URL ứng dụng**: `<cloud_run_frontend_url>`
- **Project GCP**: `<project_id>`
- **Tài liệu trong repo**: `README.md`, `docs/architecture.md`, `infrastructure/terraform/README.md`
- **Cách thêm/chỉnh OPENAI key**: Bước 4.3 hoặc dùng Secret Manager trong Console.

---

## 6. Triển khai thủ công (không dùng Terraform)

Nếu khách không dùng Terraform, có thể triển khai theo README.md gốc:

1. Bật API: Cloud Run, Cloud Storage, Cloud Build, Secret Manager.
2. Tạo GCS bucket, Secret Manager secret `openai-api-key`, Artifact Registry repo.
3. Build/push image bằng `gcloud builds submit --config=cloudbuild.yaml .`
4. Deploy từng service lên Cloud Run bằng `gcloud run deploy` (xem README.md phần "Manual Deploy với Docker").

Chi tiết từng lệnh nằm trong **README.md** tại thư mục gốc repo.

---

## 7. Xử lý sự cố

### 7.1 Lỗi 403 Permission denied khi `terraform apply`

Nếu gặp **Permission denied to list services** (serviceusage) hoặc **Permission 'iam.serviceAccounts.create' denied**:

- **Nguyên nhân**: Tài khoản dùng cho Terraform (Application Default Credentials) không đủ quyền trên project.
- **Cách xử lý**:
  1. Dùng tài khoản có quyền **Owner** hoặc **Editor** trên project, chạy:  
     `gcloud auth application-default login`  
     Đăng nhập bằng tài khoản đó rồi chạy lại `terraform apply`.
  2. Hoặc nhờ **Owner** của project cấp cho tài khoản của bạn ít nhất: **Service Usage Admin** (bật API), **Service Account Admin** (tạo SA), và quyền tạo Cloud Run, Storage, Secret Manager, Pub/Sub, Artifact Registry (hoặc gán role **Editor**).
  3. Nếu project do trường/tổ chức quản lý: liên hệ admin project để họ chạy Terraform hoặc cấp quyền đủ cho tài khoản của bạn.

| Triệu chứng | Gợi ý xử lý |
|-------------|--------------|
| **403 Permission denied** (list services / create service account) | Xem [§7.1](#71-lỗi-403-permission-denied-khi-terraform-apply): dùng tài khoản Owner/Editor hoặc được cấp đủ quyền. |
| `terraform apply` báo lỗi API chưa bật | Bật thủ công: `gcloud services enable run.googleapis.com storage.googleapis.com secretmanager.googleapis.com cloudbuild.googleapis.com` rồi `terraform apply` lại. |
| Cloud Run báo "Image not found" | Chạy `gcloud builds submit --config=cloudbuild.yaml .` từ root repo; sau đó `terraform apply` lại hoặc redeploy revision trên Console. |
| Chatbot trả lời lỗi hoặc không gọi được LLM | Kiểm tra Secret Manager: secret `openai-api-key` đã có version và đúng key; Service Account Cloud Run Chatbot có quyền `secretmanager.secretAccessor`. |
| Frontend không kết nối được Chatbot | Kiểm tra biến môi trường Frontend: `CHATBOT_API_URL` trỏ đúng URL Cloud Run Chatbot (Terraform đã inject; nếu deploy tay cần set đúng). |
| CORS lỗi khi gọi API từ domain khác | Trong `terraform.tfvars` set `cors_origins = "https://your-frontend-domain.com"` rồi `terraform apply`. |

---

## 8. Tài liệu tham khảo

- **Kiến trúc**: [docs/architecture.md](architecture.md)
- **Terraform chi tiết**: [infrastructure/terraform/README.md](../infrastructure/terraform/README.md)
- **API**: [docs/api.md](api.md)
- **Checklist dự án**: [docs/PROJECT_CHECKLIST.md](PROJECT_CHECKLIST.md)
- **README tổng quan**: [README.md](../README.md) (từ thư mục gốc repo)

---

*Tài liệu này phục vụ triển khai và bàn giao cho khách hàng; cập nhật theo từng phiên bản repo.*
