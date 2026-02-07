# GCS bucket lưu session (theo docs/database.md: gs://<bucket>/chat/sessions/<session_id>.json)
resource "google_storage_bucket" "sessions" {
  name     = local.gcs_bucket_name
  project  = var.project_id
  location = var.region

  uniform_bucket_level_access = true

  depends_on = [google_project_service.storage]
}

# Không public list; Chatbot SA sẽ được cấp quyền qua IAM
# (IAM binding cho chatbot SA ở iam.tf)
