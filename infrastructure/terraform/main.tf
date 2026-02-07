provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

locals {
  # Tự build image URI nếu không truyền
  artifact_registry = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_registry_repo}"
  image_tools       = var.image_tools != "" ? var.image_tools : "${local.artifact_registry}/tools:latest"
  image_chatbot    = var.image_chatbot != "" ? var.image_chatbot : "${local.artifact_registry}/chatbot:latest"
  image_frontend   = var.image_frontend != "" ? var.image_frontend : "${local.artifact_registry}/frontend:latest"
  gcs_bucket_name  = "${var.project_id}-chatbot-sessions"
  secret_name      = "openai-api-key"
}
