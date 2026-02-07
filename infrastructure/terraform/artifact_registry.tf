# Artifact Registry repository cho Docker images (Chatbot, Tools, Frontend)
resource "google_artifact_registry_repository" "chatbot" {
  provider = google-beta

  location      = var.region
  repository_id = var.artifact_registry_repo
  description   = "Docker images for Chatbot Cloud (tools, chatbot, frontend)"
  format        = "DOCKER"

  depends_on = [google_project_service.artifactregistry]
}
