# Service account cho Chatbot: đọc Secret Manager (OPENAI_API_KEY), đọc/ghi GCS bucket sessions
resource "google_service_account" "chatbot" {
  account_id   = "chatbot-sa"
  display_name = "Chatbot Cloud Run SA"
  project      = var.project_id
}

# Secret Manager: Chatbot SA được phép access secret openai-api-key
resource "google_secret_manager_secret_iam_member" "chatbot_secret" {
  secret_id = google_secret_manager_secret.openai_api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.chatbot.email}"
}

# GCS: Chatbot SA đọc/ghi bucket sessions
resource "google_storage_bucket_iam_member" "chatbot_bucket" {
  bucket = google_storage_bucket.sessions.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.chatbot.email}"
}
