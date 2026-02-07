# Cloud Run: Frontend (Streamlit) - gọi Chatbot API
resource "google_cloud_run_v2_service" "frontend" {
  name     = "chatbot-frontend"
  location = var.region
  project  = var.project_id

  template {
    containers {
      image = local.image_frontend

      env {
        name  = "CHATBOT_API_URL"
        value = google_cloud_run_v2_service.chatbot.uri
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }
    scaling {
      min_instance_count = var.frontend_min_instances
      max_instance_count = var.frontend_max_instances
    }
    timeout = "60s"
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [
    google_project_service.run,
    google_cloud_run_v2_service.chatbot,
  ]
}

resource "google_cloud_run_v2_service_iam_member" "frontend_invoker" {
  count = var.allow_unauthenticated ? 1 : 0

  project   = google_cloud_run_v2_service.frontend.project
  location  = google_cloud_run_v2_service.frontend.location
  name      = google_cloud_run_v2_service.frontend.name
  role      = "roles/run.invoker"
  member    = "allUsers"
}
