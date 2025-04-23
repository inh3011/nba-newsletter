provider "aws" {
  region = "ap-northeast-2"
}

# IAM Policy Document
data "aws_iam_policy_document" "lambda_sqs_policy" {
  statement {
    effect = "Allow"
    actions = [
      "sqs:SendMessage",
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes"
    ]
    resources = [aws_sqs_queue.newsletter_queue.arn]
  }
}

# IAM Policy
resource "aws_iam_policy" "lambda_sqs_policy" {
  name        = "${local.resource_prefix}-lambda-sqs-policy"
  description = "Policy for Lambda to access SQS"
  policy      = data.aws_iam_policy_document.lambda_sqs_policy.json
}

resource "aws_iam_role" "lambda_exec" {
  name = "${local.resource_prefix}-lambda-execution-role"

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
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_sqs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_sqs_policy.arn
}

# CloudWatch Log Group with Free Tier optimization
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${local.resource_prefix}"
  retention_in_days = 30  # Free Tier: 5GB storage

  tags = {
    Environment = var.environment
    Project     = var.project_name
    FreeTier    = "true"
  }
}

# SQS Queue with Free Tier optimization
resource "aws_sqs_queue" "newsletter_queue" {
  name                      = "${local.resource_prefix}-queue"
  delay_seconds             = 0
  message_retention_seconds = 86400  # 1 day (Free Tier: 1M requests/month)
  visibility_timeout_seconds = 30
  max_message_size          = 262144  # 256KB (Free Tier limit)

  tags = {
    Environment = var.environment
    Project     = var.project_name
    FreeTier    = "true"
  }
}

# Lambda Function with Free Tier optimization
resource "aws_lambda_function" "producer" {
  function_name = "${local.resource_prefix}-producer"
  handler       = "producer_lambda.lambda_handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn
  memory_size   = 128  # Reduced from 256MB to stay within Free Tier
  timeout       = 15   # Reduced from 30s to minimize execution time

  filename         = "${path.module}/../lambda/producer/producer_lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/../lambda/producer/producer_lambda.zip")

  environment {
    variables = {
      SQS_QUEUE_URL = aws_sqs_queue.newsletter_queue.url
    }
  }

  tracing_config {
    mode = "Active"
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda_logs,
    aws_sqs_queue.newsletter_queue
  ]

  lifecycle {
    ignore_changes = [filename, source_code_hash]
  }
}

resource "aws_lambda_function" "consumer" {
  function_name = "${local.resource_prefix}-consumer"
  handler       = "consumer_lambda.lambda_handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn
  memory_size   = 128  # Reduced from 256MB to stay within Free Tier
  timeout       = 15   # Reduced from 30s to minimize execution time

  filename         = "${path.module}/../lambda/consumer/consumer_lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/../lambda/consumer/consumer_lambda.zip")

  environment {
    variables = {
      GMAIL_ADDRESS      = var.gmail_address
      GMAIL_APP_PASSWORD = var.gmail_app_password
    }
  }

  tracing_config {
    mode = "Active"
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda_logs,
    aws_sqs_queue.newsletter_queue
  ]

  lifecycle {
    ignore_changes = [filename, source_code_hash]
  }
}

resource "aws_lambda_event_source_mapping" "consumer_sqs_trigger" {
  event_source_arn = aws_sqs_queue.newsletter_queue.arn
  function_name    = aws_lambda_function.consumer.arn
  batch_size       = 1  # Free Tier: 1M requests/month
  enabled          = true

  depends_on = [
    aws_lambda_function.consumer,
    aws_sqs_queue.newsletter_queue
  ]
}

# CloudWatch Alarms with Free Tier optimization
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  for_each = {
    producer = aws_lambda_function.producer.function_name
    consumer = aws_lambda_function.consumer.function_name
  }

  alarm_name          = "${each.value}-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period             = "300"  # 5 minutes (Free Tier: 10 custom metrics)
  statistic          = "Sum"
  threshold          = "0"
  alarm_description  = "This metric monitors Lambda function errors"
  alarm_actions      = []  # Remove SNS topic dependency
  ok_actions         = []  # Remove SNS topic dependency

  dimensions = {
    FunctionName = each.value
  }

  tags = {
    Environment = var.environment
    Project     = var.project_name
    FreeTier    = "true"
  }
}