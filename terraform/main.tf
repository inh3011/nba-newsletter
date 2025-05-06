provider "aws" {
  region = "ap-northeast-2"
}

# IAM policy document for allowing Lambda access to SQS
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

# IAM policy document for allowing Lambda to scan DynamoDB users table
data "aws_iam_policy_document" "lambda_dynamodb_policy" {
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:Scan"
    ]
    resources = [
      "arn:aws:dynamodb:ap-northeast-2:915650020635:table/users"
    ]
  }
}

# IAM policy to grant SQS permissions to Lambda
resource "aws_iam_policy" "lambda_sqs_policy" {
  name        = "${local.resource_prefix}-lambda-sqs-policy"
  description = "Policy for Lambda to access SQS"
  policy      = data.aws_iam_policy_document.lambda_sqs_policy.json
}

# IAM role for Lambda execution
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

# Attach AWS-managed policy for CloudWatch Logs to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Attach custom SQS policy to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_sqs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_sqs_policy.arn
}

resource "aws_iam_policy" "lambda_dynamodb_policy" {
  name   = "${local.resource_prefix}-lambda-dynamodb-policy"
  policy = data.aws_iam_policy_document.lambda_dynamodb_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_dynamodb_policy.arn
}

# CloudWatch log group for Lambda functions
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${local.resource_prefix}"
  retention_in_days = 30

  tags = {
    Environment = var.environment
    Project     = var.project_name
    FreeTier    = "true"
  }
}

# SQS queue for newsletter email tasks
resource "aws_sqs_queue" "newsletter_queue" {
  name                      = "${local.resource_prefix}-queue"
  delay_seconds             = 0
  message_retention_seconds = 86400
  visibility_timeout_seconds = 30
  max_message_size          = 262144

  tags = {
    Environment = var.environment
    Project     = var.project_name
    FreeTier    = "true"
  }
}

resource "aws_cloudwatch_event_rule" "producer_trigger" {
  name                = "${local.resource_prefix}-producer-schedule"
  schedule_expression = "cron(0 6 * * ? *)"

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_cloudwatch_event_target" "producer_target" {
  rule      = aws_cloudwatch_event_rule.producer_trigger.name
  target_id = "invoke-producer-lambda"
  arn       = aws_lambda_function.producer.arn
}

resource "aws_lambda_permission" "producer_allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.producer.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.producer_trigger.arn
}


# Lambda function to enqueue email tasks (Producer)
resource "aws_lambda_function" "producer" {
  function_name = "${local.resource_prefix}-producer"
  handler       = "producer_lambda.lambda_handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn
  memory_size   = 128
  timeout       = 15

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

}

# Lambda function to send emails from SQS tasks (Consumer)
resource "aws_lambda_function" "consumer" {
  function_name = "${local.resource_prefix}-consumer"
  handler       = "consumer_lambda.lambda_handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn
  memory_size   = 128
  timeout       = 15

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

}

# Connect the SQS queue to the Consumer Lambda as trigger
resource "aws_lambda_event_source_mapping" "consumer_sqs_trigger" {
  event_source_arn = aws_sqs_queue.newsletter_queue.arn
  function_name    = aws_lambda_function.consumer.arn
  batch_size       = 1
  enabled          = true

  depends_on = [
    aws_lambda_function.consumer,
    aws_sqs_queue.newsletter_queue
  ]
}

# CloudWatch alarms to monitor Lambda errors
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