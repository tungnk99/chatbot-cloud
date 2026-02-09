# Cloud Run: Tools service (Backend/tools) - Serverless-first, deploy riêng
resource "google_cloud_run_v2_service" "tools" {
  name     = "chatbot-tools"
  location = var.region
  project  = var.project_id

  template {
    containers {
      image = local.image_tools

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
    }
    scaling {
      min_instance_count = var.tools_min_instances
      max_instance_count = var.tools_max_instances
    }
    timeout = "60s"
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [
    google_project_service.run,
  ]
}

resource "google_cloud_run_v2_service_iam_member" "tools_invoker" {
  count = var.allow_unauthenticated ? 1 : 0

  project   = google_cloud_run_v2_service.tools.project
  location  = google_cloud_run_v2_service.tools.location
  name      = google_cloud_run_v2_service.tools.name
  role      = "roles/run.invoker"
  member    = "allUsers"
}
