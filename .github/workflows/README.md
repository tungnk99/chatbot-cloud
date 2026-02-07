# GitHub Actions

## deploy.yml – Tự động triển khai khi push lên main

Khi push code lên nhánh `main`, workflow sẽ:

1. **Build** 3 Docker images (Tools, Chatbot, Frontend) bằng Cloud Build và push lên Artifact Registry.
2. **Deploy** từng service lên Cloud Run: `chatbot-tools`, `chatbot-api`, `chatbot-frontend`.

### Cấu hình GitHub Secrets

Vào **Settings → Secrets and variables → Actions**, tạo 2 secrets:

| Secret | Mô tả |
|--------|--------|
| `GCP_PROJECT_ID` | GCP Project ID (ví dụ: `my-project-123`) |
| `GCP_SA_KEY` | Nội dung JSON của Service Account key (file `.json` khi tạo key trong GCP Console) |

### Quyền cần có cho Service Account

Service Account dùng trong `GCP_SA_KEY` cần ít nhất:

- **Cloud Build Editor** – để chạy `gcloud builds submit`
- **Artifact Registry Writer** – (hoặc Cloud Build dùng SA mặc định có sẵn quyền push)
- **Cloud Run Admin** – để deploy lên Cloud Run
- **Service Account User** – để Cloud Run chạy với SA đã cấu hình

Hoặc gán các role: `roles/cloudbuild.builds.builder`, `roles/run.admin`, `roles/iam.serviceAccountUser`, và quyền ghi Artifact Registry cho project/repo tương ứng.

### Lưu ý

- Hạ tầng (Terraform) cần được tạo trước (bucket, Artifact Registry, Cloud Run services, IAM). Workflow chỉ build image và deploy revision mới.
- Region mặc định: `asia-southeast1`. Đổi trong `env.GCP_REGION` trong `deploy.yml` nếu dùng region khác.
