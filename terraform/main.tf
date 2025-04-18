provider "aws" {
  region = "ap-northeast-2"
}

resource "aws_sqs_queue" "newsletter_queue" {
  name                      = "nbaNewsletterQueue"
  delay_seconds             = 0
  message_retention_seconds = 86400
  visibility_timeout_seconds = 30

  tags = {
    Environment = "dev"
    Project     = "nba-newsletter"
    FreeTier    = "true"
  }
}