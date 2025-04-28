# Technology Documentation Template

## 1. Overview
Terraform is an Infrastructure as Code (IaC) tool developed by HashiCorp.  
It allows you to define and manage cloud resources like AWS, Azure, and GCP using code.

---

## 2. Why We Chose Terraform
We selected Terraform to build consistent and repeatable infrastructure.  
Compared to tools like AWS CloudFormation, Terraform offers strong multi-cloud support and a simpler, more readable syntax.

---

## 3. Role in the Project
- All infrastructure code is located in the `/terraform/` directory:
  - `main.tf`: Defines resources
  - `variables.tf`: Manages input variables
  - `terraform.tfstate`: Tracks the current infrastructure state
- We use Terraform to create and manage AWS services such as Lambda functions, SQS queues, and IAM roles.

---

## 4. Key Configurations and Code Example
In this project, we manage Lambda deployments using Terraform.  
Below is an example of deploying the `nbaNewsletterProducer` Lambda function:

```hcl
provider "aws" {
  region = "ap-northeast-2"
}

resource "aws_iam_role" "lambda_exec" {
  name = "nbaLambdaRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = { Service = "lambda.amazonaws.com" },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "basic_execution" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "producer" {
  function_name = "nbaNewsletterProducer"
  handler       = "producer_lambda.lambda_handler"
  runtime       = "python3.11"
  role          = aws_iam_role.lambda_exec.arn

  filename         = "${path.module}/../lambda/producer/producer_lambda.zip"
  source_code_hash = filebase64sha256("${path.module}/../lambda/producer/producer_lambda.zip")

  environment {
    variables = {
      SQS_QUEUE_URL = "https://sqs.ap-northeast-2.amazonaws.com/123456789012/nbaNewsletterQueue"
    }
  }

  timeout = 15
}
```
### Explanation  
- IAM Role Creation: Grants the Lambda function the permissions it needs to run.
- Lambda Deployment: Uploads the local zip file to AWS to create the nbaNewsletterProducer function.
- Environment Variables: Passes necessary values like the SQS queue URL to the Lambda function.
- Important: Make sure filename and source_code_hash paths are set relative to the Terraform module directory.

### Terraform Commands

To initialize and apply Terraform configurations:
```
terraform init
terraform plan
terraform apply
```

---

## 5. Things to Watch Out For
- Securely manage your terraform.tfstate file. It’s recommended to store it in a remote backend like AWS S3.
- Always review the output of terraform plan carefully before applying changes.
- Handle sensitive data (like passwords and keys) separately or encrypt them.

---

## 6. 참고 링크
[Terraform Official Documentation](https://www.terraform.io/docs)  
[HashiCorp Learn - Terraform](https://learn.hashicorp.com/terraform)  
[Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)  

---