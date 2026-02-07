terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.0"
    }
  }

  # Uncomment và cấu hình backend để lưu state trên GCS (khuyến nghị cho team)
  # backend "gcs" {
  #   bucket = "your-terraform-state-bucket"
  #   prefix = "chatbot-cloud/state"
  # }
}
