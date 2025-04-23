variable "region" {
  default = "ap-northeast-2"
}

variable "gmail_address" {
  description = "Gmail address for sending newsletters"
  type        = string
}

variable "gmail_app_password" {
  description = "Gmail application password for authentication"
  type        = string
  sensitive   = true
}

variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "nba-newsletter"
}

# Environment-specific naming
locals {
  environment_prefix = var.environment == "prod" ? "" : "${var.environment}-"
  resource_prefix    = "${local.environment_prefix}${var.project_name}"
}