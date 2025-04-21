#!/bin/bash

set -e

LOG_DIR="logs/lambda"

mkdir -p "$LOG_DIR"

PRODUCER_DIR=lambda/producer
PRODUCER_BUILD=$PRODUCER_DIR/build
PRODUCER_ZIP=$PRODUCER_DIR/producer_lambda.zip

rm -rf "$PRODUCER_BUILD"
mkdir -p "$PRODUCER_BUILD"

pip3 install -r "$PRODUCER_DIR/requirements.txt" -t "$PRODUCER_BUILD"
cp "$PRODUCER_DIR/producer_lambda.py" "$PRODUCER_BUILD"
cp "$PRODUCER_DIR/newsletter_template.html" "$PRODUCER_BUILD/"

(cd "$PRODUCER_BUILD" && zip -r "../$(basename "$PRODUCER_ZIP")" . > /dev/null)

CONSUMER_DIR=lambda/consumer
CONSUMER_BUILD=$CONSUMER_DIR/build
CONSUMER_ZIP=$CONSUMER_DIR/consumer_lambda.zip

rm -rf "$CONSUMER_BUILD"
mkdir -p "$CONSUMER_BUILD"

pip3 install -r "$CONSUMER_DIR/requirements.txt" -t "$CONSUMER_BUILD"
cp "$CONSUMER_DIR/consumer_lambda.py" "$CONSUMER_BUILD"

(cd "$CONSUMER_BUILD" && zip -r "../$(basename "$CONSUMER_ZIP")" . > /dev/null)

