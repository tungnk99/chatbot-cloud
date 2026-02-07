output "region" {
  value = var.region
}

output "gcs_bucket_sessions" {
  description = "GCS bucket lưu session (chat/sessions/)"
  value       = google_storage_bucket.sessions.name
}

output "artifact_registry_repository" {
  description = "Artifact Registry repo cho Docker images"
  value       = google_artifact_registry_repository.chatbot.id
}

output "cloud_run_tools_url" {
  description = "URL Cloud Run Tools service"
  value       = google_cloud_run_v2_service.tools.uri
}

output "cloud_run_chatbot_url" {
  description = "URL Cloud Run Chatbot service"
  value       = google_cloud_run_v2_service.chatbot.uri
}

output "cloud_run_frontend_url" {
  description = "URL Cloud Run Frontend (mở trình duyệt vào đây)"
  value       = google_cloud_run_v2_service.frontend.uri
}

output "openai_secret_name" {
  description = "Secret Manager secret chứa OPENAI_API_KEY (thêm version thủ công nếu không dùng var)"
  value       = google_secret_manager_secret.openai_api_key.name
}

output "pubsub_topic_chat_requests" {
  description = "Pub/Sub topic cho chat bất đồng bộ (khi enable_pubsub_async = true)"
  value       = var.enable_pubsub_async ? google_pubsub_topic.chat_requests[0].id : null
}
