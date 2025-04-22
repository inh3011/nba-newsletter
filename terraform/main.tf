provider "aws" {
  region = "ap-northeast-2"
}

resource "aws_iam_role" "lambda_exec" {
  name = "nba_lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_sqs" {
  role = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSQSFullAccess"
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

resource "aws_lambda_function" "producer" {
  function_name = "nbaNewsletterProducer"
  handler       = "producer_lambda.lambda_handler"
  runtime       = "python3.13"
  role          = aws_iam_role.lambda_exec.arn

  filename         = "${path.module}/../lambda/producer/producer_lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/../lambda/producer/producer_lambda.zip")

  environment {
    variables = {
      SQS_QUEUE_URL    = var.sqs_queue_url
    }
  }

  timeout = 30

  lifecycle {
    ignore_changes = [filename, source_code_hash]
  }
}

resource "aws_lambda_function" "consumer" {
  function_name = "nbaNewsletterConsumer"
  handler       = "consumer_lambda.lambda_handler"
  runtime       = "python3.13"
  role          = aws_iam_role.lambda_exec.arn

  filename         = "${path.module}/../lambda/consumer/consumer_lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/../lambda/consumer/consumer_lambda.zip")

  environment {
    variables = {
      GMAIL_ADDRESS      = var.gmail_address
      GMAIL_APP_PASSWORD = var.gmail_app_password
    }
  }

  timeout = 30

  lifecycle {
    ignore_changes = [filename, source_code_hash]
  }
}

resource "aws_lambda_event_source_mapping" "consumer_sqs_trigger" {
  event_source_arn = aws_sqs_queue.newsletter_queue.arn
  function_name    = aws_lambda_function.consumer.arn
  batch_size       = 1
  enabled          = true
}