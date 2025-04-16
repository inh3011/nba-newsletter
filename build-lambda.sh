#!/bin/bash

set -e

REGION="ap-northeast-2"
LOG_DIR="logs/lambda"
ROLE_ARN="arn:aws:iam::915650020635:role/LambdaRole"
TIMESTAMP=$(date "+%Y-%m-%d_%H-%M-%S")
PRODUCER_OUTPUT_FILE="$LOG_DIR/producer_${TIMESTAMP}.json"
CONSUMER_OUTPUT_FILE="$LOG_DIR/consumer_${TIMESTAMP}.json"

mkdir -p "$LOG_DIR"

# ========================
# Producer Lambda
# ========================
PRODUCER_DIR=lambda/producer
PRODUCER_BUILD=$PRODUCER_DIR/build
PRODUCER_ZIP=$PRODUCER_DIR/producer_lambda.zip
PRODUCER_FUNC=nbaNewsletterProducer

rm -rf "$PRODUCER_BUILD"
mkdir -p "$PRODUCER_BUILD"

pip3 install -r "$PRODUCER_DIR/requirements.txt" -t "$PRODUCER_BUILD"
cp "$PRODUCER_DIR/producer_lambda.py" "$PRODUCER_BUILD"
cp "$PRODUCER_DIR/newsletter_template.html" "$PRODUCER_BUILD/"

(cd "$PRODUCER_BUILD" && zip -r "../$(basename "$PRODUCER_ZIP")" . > /dev/null)

if aws lambda get-function --function-name "$PRODUCER_FUNC" --region "$REGION" > /dev/null 2>&1; then
  aws lambda update-function-code \
    --function-name "$PRODUCER_FUNC" \
    --zip-file "fileb://$PRODUCER_ZIP" \
    --region "$REGION" | tee "$PRODUCER_OUTPUT_FILE"
else
  aws lambda create-function \
    --function-name "$PRODUCER_FUNC" \
    --runtime python3.13 \
    --role $ROLE_ARN \
    --handler producer_lambda.lambda_handler \
    --zip-file "fileb://$PRODUCER_ZIP" \
    --region "$REGION" | tee "$PRODUCER_OUTPUT_FILE"
fi

# ========================
# Consumer Lambda
# ========================
CONSUMER_DIR=lambda/consumer
CONSUMER_BUILD=$CONSUMER_DIR/build
CONSUMER_ZIP=$CONSUMER_DIR/consumer_lambda.zip
CONSUMER_FUNC=nbaNewsletterConsumer

rm -rf "$CONSUMER_BUILD"
mkdir -p "$CONSUMER_BUILD"

pip3 install -r "$CONSUMER_DIR/requirements.txt" -t "$CONSUMER_BUILD"
cp "$CONSUMER_DIR/consumer_lambda.py" "$CONSUMER_BUILD"

(cd "$CONSUMER_BUILD" && zip -r "../$(basename "$CONSUMER_ZIP")" . > /dev/null)

if aws lambda get-function --function-name "$CONSUMER_FUNC" --region "$REGION" > /dev/null 2>&1; then
  aws lambda update-function-code \
    --function-name "$CONSUMER_FUNC" \
    --zip-file "fileb://$CONSUMER_ZIP" \
    --region "$REGION" | tee "$CONSUMER_OUTPUT_FILE"
else
  aws lambda create-function \
    --function-name "$CONSUMER_FUNC" \
    --runtime python3.13 \
    --role $ROLE_ARN \
    --handler producer_lambda.lambda_handler \
    --zip-file "fileb://$CONSUMER_ZIP" \
    --region "$REGION" | tee "$CONSUMER_OUTPUT_FILE"
fi

