#!/bin/bash

LAMBDA_DIR=lambda
BUILD_DIR=lambda/build

LAMBDA_NAME=nbaNewsletter
REGION=ap-northeast-2
ZIP_PATH=$LAMBDA_DIR/nba_lambda_deploy.zip
LOG_DIR=logs/lambda

rm -rf $BUILD_DIR
mkdir $BUILD_DIR

pip install -r $LAMBDA_DIR/requirements-lambda.txt -t $BUILD_DIR

cp $LAMBDA_DIR/lambda_function.py $BUILD_DIR/
cp $LAMBDA_DIR/template/newsletter_template.html $BUILD_DIR/

rm -f $ZIP_PATH
zip -r $ZIP_PATH $BUILD_DIR/*

mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
OUTPUT_FILE="$LOG_DIR/lambda_$TIMESTAMP.json"

aws lambda update-function-code \
  --function-name "$LAMBDA_NAME" \
  --zip-file "fileb://$ZIP_PATH" \
  --region "$REGION" |  tee "$OUTPUT_FILE"