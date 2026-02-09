# Google Pub/Sub: Hàng đợi xử lý tin nhắn chat bất đồng bộ
# Tin nhắn được đẩy vào topic, subscription push tới Chatbot để gọi LLM, tránh treo kết nối người dùng.
# (Không dùng data.google_project để tránh lỗi permission khi tài khoản chưa có resourcemanager.projects.get)

resource "google_pubsub_topic" "chat_requests" {
  count = var.enable_pubsub_async ? 1 : 0

  name    = "chat-requests"
  project = var.project_id

  depends_on = [google_project_service.pubsub]
}

# Push subscription: gửi message tới Cloud Run Chatbot (endpoint /api/pubsub/chat-handler)
resource "google_pubsub_subscription" "chat_requests_push" {
  count = var.enable_pubsub_async ? 1 : 0

  name    = "chat-requests-push"
  topic   = google_pubsub_topic.chat_requests[0].name
  project = var.project_id

  push_config {
    push_endpoint = "${google_cloud_run_v2_service.chatbot.uri}${var.api_prefix}/pubsub/chat-handler"
    oidc_token {
      service_account_email = google_service_account.chatbot.email
    }
  }

  ack_deadline_seconds = 300
  expiration_policy {
    ttl = "" # không hết hạn
  }

  depends_on = [
    google_project_service.pubsub,
    google_cloud_run_v2_service.chatbot,
  ]
}

# Chatbot SA được phép publish lên topic
resource "google_pubsub_topic_iam_member" "chatbot_publisher" {
  count = var.enable_pubsub_async ? 1 : 0

  project = google_pubsub_topic.chat_requests[0].project
  topic   = google_pubsub_topic.chat_requests[0].name
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.chatbot.email}"
}

# Push subscription dùng OIDC với Chatbot SA → Chatbot SA cần quyền invoke chính Cloud Run Chatbot
resource "google_cloud_run_v2_service_iam_member" "chatbot_self_invoker" {
  count = var.enable_pubsub_async ? 1 : 0

  project   = google_cloud_run_v2_service.chatbot.project
  location  = google_cloud_run_v2_service.chatbot.location
  name      = google_cloud_run_v2_service.chatbot.name
  role      = "roles/run.invoker"
  member    = "serviceAccount:${google_service_account.chatbot.email}"
}
