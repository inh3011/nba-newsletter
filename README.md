# 🏀 NBA Newsletter Project

## Overview

NBA Newsletter is a service that sends users daily emails with the results of their favorite NBA teams' games.  
It is built using a **serverless architecture** with various AWS services.

---

## Architecture

```mermaid
flowchart TD
  A(EventBridge (Every day at 15:00 KST)) --> B(nbaNewsletterProducer (Lambda))
  B --> C(Fetch subscribers from DynamoDB)
  B --> D(Push email tasks to SQS (nbaNewsletterQueue))
  D --> E(nbaNewsletterConsumer (Lambda, triggered by SQS))
  E --> F(Send emails using Gmail SMTP)
```

---

## Components

### Backend

- **FastAPI**  
  Provides APIs to register user emails and update favorite teams
- **DynamoDB**  
  Stores user information and team preferences
- **nba_api**  
  Fetches real-time NBA game data
- **Jinja2**  
  Renders the HTML newsletter template

### AWS Serverless

- **AWS Lambda**
  - `nbaNewsletterProducer`: Fetches users and sends tasks to SQS
  - `nbaNewsletterConsumer`: Listens to SQS and sends emails
- **AWS SQS**
  - A queue for managing email tasks asynchronously
- **AWS EventBridge**
  - Triggers the Producer Lambda every day
- **Amazon CloudWatch**
  - Monitors and logs Lambda function executions

### Email Delivery

- **Gmail SMTP**
  - Sends emails using `smtplib` and `email.message`
  - Managed with environment variables: `GMAIL_ADDRESS`, `GMAIL_APP_PASSWORD`

### Dev & Infra

- **Python 3.11+**
- **Terraform**
  - Infrastructure as Code for AWS services
- **Vite + React**
  - A simple web UI for subscribing and selecting favorite teams
- **Git + GitHub**
  - Version control and project documentation

---

## Deployment

### Create AWS Resources using Terraform

```bash
terraform init
terraform plan
terraform apply
```

- Creates the Lambda execution role
- Creates the SQS queue
- Deploys the Producer and Consumer Lambdas
- Sets up the SQS trigger for the Consumer

### Deploy Lambda Functions (with Shell Script)

```bash
./deploy-lambdas.sh
```

- Packages and updates `producer_lambda.zip` and `consumer_lambda.zip`

---

## Environment Variables (.env)

- `GMAIL_ADDRESS`
- `GMAIL_APP_PASSWORD`
- `SQS_QUEUE_URL`

> (Must be set in Lambda console environment variables)

---

## Summary

This system efficiently delivers NBA game results using serverless technology.  
It ensures scalability and cost-efficiency by separating user querying and email delivery into different Lambdas via SQS.

**More detailed documents are available in the `/docs` folder.**
