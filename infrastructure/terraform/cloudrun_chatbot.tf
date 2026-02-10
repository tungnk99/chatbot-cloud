# Cloud Run: Chatbot service - điều phối LLM, Tools, Storage
# Cần: OPENAI_API_KEY (Secret), TOOLS_BASE_URL (Tools service), GCS bucket
resource "google_cloud_run_v2_service" "chatbot" {
  name     = "chatbot-api"
  location = var.region
  project  = var.project_id

  template {
    service_account = google_service_account.chatbot.email

    containers {
      image = local.image_chatbot

      env {
        name  = "OPENAI_MODEL"
        value = var.openai_model
      }
      env {
        name  = "TOOLS_BASE_URL"
        value = google_cloud_run_v2_service.tools.uri
      }
      env {
        name  = "STORAGE_BACKEND"
        value = "gcs"
      }
      env {
        name  = "GCS_BUCKET"
        value = google_storage_bucket.sessions.name
      }
      dynamic "env" {
        for_each = var.cors_origins != "" ? [1] : []
        content {
          name  = "CORS_ORIGINS"
          value = var.cors_origins
        }
      }
      env {
        name = "OPENAI_API_KEY"
        value_source {
          secret_key_ref {
            secret  = "projects/${var.project_id}/secrets/${google_secret_manager_secret.openai_api_key.secret_id}"
            version = "latest"
          }
        }
      }
      dynamic "env" {
        for_each = var.enable_pubsub_async ? [1] : []
        content {
          name  = "PUBSUB_TOPIC"
          value = "projects/${var.project_id}/topics/${google_pubsub_topic.chat_requests[0].name}"
        }
      }
      dynamic "env" {
        for_each = var.enable_pubsub_async ? [1] : []
        content {
          name  = "USE_PUBSUB_ASYNC"
          value = "true"
        }
      }

      resources {
        limits = {
          cpu    = var.chatbot_cpu
          memory = var.chatbot_memory_mi
        }
      }
    }
    scaling {
      min_instance_count = var.chatbot_min_instances
      max_instance_count = var.chatbot_max_instances
    }
    timeout = "300s" # Đủ lớn cho xử lý LLM khi nhận push từ Pub/Sub
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [
    google_project_service.run,
    google_secret_manager_secret_iam_member.chatbot_secret,
    google_storage_bucket_iam_member.chatbot_bucket,
    google_cloud_run_v2_service.tools,
  ]
}

resource "google_cloud_run_v2_service_iam_member" "chatbot_invoker" {
  count = var.allow_unauthenticated ? 1 : 0

  project   = google_cloud_run_v2_service.chatbot.project
  location  = google_cloud_run_v2_service.chatbot.location
  name      = google_cloud_run_v2_service.chatbot.name
  role      = "roles/run.invoker"
  member    = "allUsers"
}
