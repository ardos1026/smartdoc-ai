
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.0"
    }
  }
}

provider "google" {
  project = "smartdoc-ai-510812"
  region  = "asia-south1"
}



data "google_project" "current" {
  project_id = "smartdoc-ai-510812"
}



output "project_id" {
  description = "Google Cloud project ID"
  value       = data.google_project.current.project_id
}


resource "google_cloud_run_v2_service" "smartdoc_ai" {
  name     = "smartdoc-ai"
  location = "asia-south1"
  project  = data.google_project.current.project_id
  
  client         = "gcloud"
  client_version = "587.0.0"



  template {
    service_account = "722361220782-compute@developer.gserviceaccount.com"

    containers {
      image = "asia-south1-docker.pkg.dev/smartdoc-ai-510812/smartdoc-repo/smartdoc-ai:latest"

      env {
        name = "GEMINI_API_KEY"

        value_source {
          secret_key_ref {
            secret  = "gemini-api-key"
            version = "latest"
          }
        }
      }
    }
  }


  lifecycle {
    prevent_destroy = true
  }
}

