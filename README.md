# Chatbot Cloud – Hệ Thống Chatbot Thông Minh Tự Động Dãn Nở

[![Cloud Platform](https://img.shields.io/badge/Cloud-Google%20Cloud-4285F4?logo=google-cloud)](https://cloud.google.com/)
[![Architecture](https://img.shields.io/badge/Architecture-Serverless-brightgreen)]()
[![Scalability](https://img.shields.io/badge/Scalability-Auto%20Scaling-orange)]()

**Chatbot Cloud** là hệ thống chatbot thông minh chạy trên **Google Cloud Platform (GCP)**, kiến trúc **serverless**, tích hợp **LLM** và **auto-scaling** theo tải.

---

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Tính năng](#tính-năng)
- [Kiến trúc](#kiến-trúc)
- [Công nghệ](#công-nghệ)
- [Bắt đầu nhanh](#bắt-đầu-nhanh)
- [Cấu trúc repo](#cấu-trúc-repo)
- [Tài liệu](#tài-liệu)
- [Đóng góp & Liên hệ](#đóng-góp--liên-hệ)

---

## Giới thiệu

- **Tự động dãn nở**: Scale up/down theo nhu cầu, scale to zero khi không dùng.
- **Chi phí**: Pay-as-you-go, chỉ trả cho tài nguyên thực sử dụng.
- **Hiệu năng**: Độ trễ thấp, xử lý đồng thời nhiều request.
- **Mở rộng**: Thêm chức năng qua **Tools** (microservice).

Chi tiết kiến trúc: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## Tính năng

| Nhóm | Nội dung |
|------|----------|
| **Cốt lõi** | Chatbot LLM, auto-scaling, Cloud Run, lịch sử hội thoại (GCS), Tools mở rộng, giao diện web, CI/CD |
| **Hàng đợi** | **Google Pub/Sub**: xử lý chat bất đồng bộ, tránh treo kết nối khi gọi LLM nặng |
| **Nâng cao** | Context-aware, tích hợp công cụ ngoài, monitoring/logging, IAM & mã hóa |

---

## Kiến trúc

```
┌─────────┐     ┌─────────────────┐     ┌────────────────────────────────┐
│  User   │ ──► │ Web (Frontend)   │ ──► │   Chatbot (Cloud Run)           │
└─────────┘     └─────────────────┘     │   LLM ↔ Tools ↔ Storage (GCS)  │
                                         │   ↔ Pub/Sub (hàng đợi async)   │
                                         └────────────────────────────────┘
```

- **Frontend** → giao diện chat (Streamlit); tùy chọn “Xử lý bất đồng bộ” dùng Pub/Sub.
- **Chatbot** → điều phối: nhận tin nhắn, gọi LLM, gọi Tools, lưu session; có thể đẩy tin nhắn vào **Pub/Sub** để xử lý bất đồng bộ (tránh treo kết nối khi LLM nặng).
- **Pub/Sub** → hàng đợi: tin nhắn được push tới Chatbot để gọi LLM, client poll GET messages để lấy kết quả.
- **Tools** → microservice mở rộng (tính lãi, tỷ lệ tiết kiệm, …).
- **Storage** → Cloud Storage lưu lịch sử hội thoại.

Chi tiết: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## Công nghệ

| Thành phần | Công nghệ |
|------------|------------|
| Cloud | GCP, Cloud Run, Cloud Storage, **Pub/Sub**, Secret Manager, Artifact Registry |
| Backend | Python, FastAPI, Docker |
| Frontend | Streamlit |
| LLM | OpenAI API (hoặc tương thích) |
| IaC / CI | Terraform, Cloud Build, GitHub Actions |

---

## Bắt đầu nhanh

### Yêu cầu

- GCP project (billing bật), [gcloud](https://cloud.google.com/sdk) và [Terraform](https://www.terraform.io/downloads) ≥ 1.0.
- OpenAI API key (dạng `sk-...`).

### Triển khai lên GCP (khuyến nghị)

1. Clone repo và vào thư mục Terraform:
   ```bash
   git clone <URL_REPO> && cd chatbot-cloud
   cd infrastructure/terraform
   ```
2. Cấu hình: `cp terraform.tfvars.example terraform.tfvars`, sửa `project_id` (và tùy chọn `openai_api_key_secret`).
3. Tạo hạ tầng: `terraform init && terraform apply`.
4. (Nếu chưa dùng tfvars) Thêm OpenAI key vào Secret Manager:  
   `echo -n "sk-..." | gcloud secrets versions add openai-api-key --data-file=-`
5. Từ **root repo**: build và push image:  
   `gcloud builds submit --config=cloudbuild.yaml .`
6. Nếu Cloud Run chưa có image: chạy lại `terraform apply` hoặc redeploy từ Console.
7. Lấy URL: `terraform output cloud_run_frontend_url` → mở trình duyệt.

**Triển khai tự động:** Push code lên nhánh `main` → GitHub Actions build và deploy lên Cloud Run. Cấu hình secrets `GCP_PROJECT_ID`, `GCP_SA_KEY` theo [.github/workflows/README.md](.github/workflows/README.md).

**Hướng dẫn đầy đủ (cho người triển khai / khách hàng):** [docs/DEPLOY_GUIDELINE.md](docs/DEPLOY_GUIDELINE.md).  
**Terraform chi tiết:** [infrastructure/terraform/README.md](infrastructure/terraform/README.md).

### Chạy local & test

- **Biến môi trường**: Copy `.env.example` → `.env`, điền `OPENAI_API_KEY`, URL (localhost) cho Chatbot/Tools.
- **Cấu hình**: [docs/CONFIG.md](docs/CONFIG.md).
- **Test / lint**: [docs/PROJECT_CHECKLIST.md](docs/PROJECT_CHECKLIST.md).
- **Load test**: [tests/load/README.md](tests/load/README.md).

---

## Cấu trúc repo

```
chatbot-cloud/
├── backend/           # Backend
│   ├── chatbot/      # Dịch vụ Chatbot (Cloud Run)
│   └── tools/        # Microservice Tools (Cloud Run)
├── frontend/         # Giao diện web (Streamlit)
├── infrastructure/
│   └── terraform/    # IaC (APIs, GCS, Secret, Artifact Registry, Cloud Run)
├── docs/             # Tài liệu (architecture, deploy, config, operations, api, …)
├── tests/            # Unit test, load test
├── cloudbuild.yaml   # Cloud Build: build & push 3 images
├── .env.example
└── README.md
```

---

## Tài liệu

| Tài liệu | Nội dung |
|----------|----------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Kiến trúc hệ thống chi tiết |
| [docs/DEPLOY_GUIDELINE.md](docs/DEPLOY_GUIDELINE.md) | Hướng dẫn triển khai (cho người mới / khách hàng) |
| [docs/CONFIG.md](docs/CONFIG.md) | Biến môi trường, cấu hình Cloud Run (Terraform) |
| [docs/OPERATIONS.md](docs/OPERATIONS.md) | Scaling, giám sát, logging, bảo mật |
| [docs/API.md](docs/API.md) | Thiết kế API |
| [docs/DATABASE.md](docs/DATABASE.md) | Schema, thiết kế dữ liệu |
| [docs/PRD.md](docs/PRD.md) | Product Requirements Document |
| [docs/PROJECT_CHECKLIST.md](docs/PROJECT_CHECKLIST.md) | Checklist phát triển & CI |
| [infrastructure/terraform/README.md](infrastructure/terraform/README.md) | Terraform: biến, thứ tự deploy, backend state |

---

## Đóng góp & Liên hệ

- Đóng góp: xem [CONTRIBUTING.md](CONTRIBUTING.md).
- Dự án phát triển cho mục đích học tập – Bài Tập Lớn môn Cloud Computing, HUST (2026).

*For questions or support, please open an issue or contact the team.*
