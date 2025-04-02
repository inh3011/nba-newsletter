#!/bin/bash

LAMBDA_DIR=lambda
BUILD_DIR=$LAMBDA_DIR/build
ZIP_PATH=$LAMBDA_DIR/nba_lambda_deploy.zip

LAMBDA_NAME=nbaNewsletter
REGION=ap-northeast-2
LOG_DIR=logs/lambda

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$LOG_DIR"

echo "Installing dependencies..."
pip install -r "$LAMBDA_DIR/requirements-lambda.txt" -t "$BUILD_DIR"

echo "Copying source files..."
cp "$LAMBDA_DIR/lambda_function.py" "$BUILD_DIR/"
cp "$LAMBDA_DIR/template/newsletter_template.html" "$BUILD_DIR/"

echo "Zipping deployment package..."
rm -f "$ZIP_PATH"
(cd "$BUILD_DIR" && zip -r "../$(basename "$ZIP_PATH")" . > /dev/null)

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
OUTPUT_FILE="$LOG_DIR/lambda_$TIMESTAMP.json"

echo "Deploying to Lambda..."
aws lambda update-function-code \
  --function-name "$LAMBDA_NAME" \
  --zip-file "fileb://$ZIP_PATH" \
  --region "$REGION" | tee "$OUTPUT_FILE"