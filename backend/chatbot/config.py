"""Cấu hình từ biến môi trường."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings từ env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # API
    api_prefix: str = "/api"

    # LLM
    openai_api_key: str = ""
    openai_model: str = "gpt-5-nano"

    # Tools service URL (Backend/tools)
    tools_base_url: str = "http://localhost:8081"

    # Storage: "local" | "gcs"
    storage_backend: str = "local"
    gcs_bucket: str = ""
    local_storage_path: str = "./data/sessions"

    # App
    port: int = 8080

    # CORS (AGENT: allow_origins cụ thể, không "*" production)
    cors_origins: str = "http://localhost:8501,http://127.0.0.1:8501"

    # Rate limit: số request / phút cho /api/chat (0 = tắt)
    rate_limit_per_minute: int = 60

    # Pub/Sub: xử lý chat bất đồng bộ (tránh treo kết nối khi gọi LLM nặng)
    use_pubsub_async: bool = False
    pubsub_topic: str = ""  # format: projects/PROJECT_ID/topics/chat-requests


settings = Settings()
