# Secret Manager: OPENAI_API_KEY cho Chatbot (AGENT.md: dùng Secret Manager, không hardcode)
resource "google_secret_manager_secret" "openai_api_key" {
  secret_id = local.secret_name
  project   = var.project_id

  replication {
    auto {}
  }

  depends_on = [google_project_service.secretmanager]
}

resource "google_secret_manager_secret_version" "openai_api_key" {
  count = var.openai_api_key_secret != "" ? 1 : 0

  secret      = google_secret_manager_secret.openai_api_key.id
  secret_data = var.openai_api_key_secret
}
