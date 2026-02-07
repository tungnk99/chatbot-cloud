variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP region (ưu tiên asia-southeast1 theo AGENT.md)"
  type        = string
  default     = "asia-southeast1"
}

variable "openai_api_key_secret" {
  description = "Nội dung OPENAI_API_KEY (sẽ lưu vào Secret Manager). Để trống nếu dùng secret đã tạo thủ công."
  type        = string
  sensitive   = true
  default     = ""
}

variable "artifact_registry_repo" {
  description = "Tên Artifact Registry repository cho Docker images"
  type        = string
  default     = "chatbot-cloud"
}

variable "image_tools" {
  description = "Image URI cho Tools service (ví dụ: asia-southeast1-docker.pkg.dev/PROJECT/chatbot-cloud/tools:latest)"
  type        = string
  default     = ""
}

variable "image_chatbot" {
  description = "Image URI cho Chatbot service"
  type        = string
  default     = ""
}

variable "image_frontend" {
  description = "Image URI cho Frontend service"
  type        = string
  default     = ""
}

variable "chatbot_min_instances" {
  description = "Cloud Run Chatbot: min instances (0 = scale to zero)"
  type        = number
  default     = 0
}

variable "chatbot_max_instances" {
  description = "Cloud Run Chatbot: max instances"
  type        = number
  default     = 10
}

variable "chatbot_memory_mi" {
  description = "Cloud Run Chatbot: memory (Mi)"
  type        = string
  default     = "512Mi"
}

variable "chatbot_cpu" {
  description = "Cloud Run Chatbot: CPU"
  type        = string
  default     = "1"
}

variable "tools_min_instances" {
  type    = number
  default = 0
}

variable "tools_max_instances" {
  type    = number
  default = 10
}

variable "frontend_min_instances" {
  type    = number
  default = 0
}

variable "frontend_max_instances" {
  type    = number
  default = 5
}

variable "allow_unauthenticated" {
  description = "Cho phép gọi Cloud Run không cần auth (demo)"
  type        = bool
  default     = true
}

variable "cors_origins" {
  description = "CORS allow_origins cho Chatbot (ví dụ URL Frontend). Để trống dùng mặc định localhost."
  type        = string
  default     = ""
}

variable "api_prefix" {
  description = "API prefix cho Chatbot (dùng trong push endpoint Pub/Sub)"
  type        = string
  default     = "/api"
}

variable "enable_pubsub_async" {
  description = "Bật Pub/Sub cho xử lý chat bất đồng bộ (topic + subscription + IAM)"
  type        = bool
  default     = true
}
