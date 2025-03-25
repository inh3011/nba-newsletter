import boto3
import os

REGION = os.getenv("AWS_REGION", "ap-northeast-2")

dynamodb = boto3.resource("dynamodb", region_name=REGION)

def get_table(name: str):
    return dynamodb.Table(name)