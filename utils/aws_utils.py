import boto3
from pathlib import Path
import requests
import os

def download_model_from_s3(bucket: str, S3path: str, local_dir: str):
    """
    Download a model from S3 bucket to local directory.
    Args:
        bucket (str): S3 bucket name
        S3path (str): path to the model on S3
        local_dir (str): directory to save the downloaded model
    """
    s3_client = boto3.client('s3') # to connect to S3 (AWS storage)
    paginator = s3_client.get_paginator("list_objects_v2")
    try:
        for page in paginator.paginate(Bucket=bucket, Prefix=S3path):
            keys = [obj["Key"] for obj in page.get("Contents", [])]
            for key in keys:
                relative_path = Path(key).relative_to(S3path)
                target_path = Path(local_dir) / relative_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    s3_client.download_file(bucket, key, str(target_path))
                except Exception as e:
                    print(f"download of {key} failed because of: {e}")
    except Exception as e:
        print(f"Error while downloading model from S3: {e}")


def is_running_on_aws():
    # for ECS Fargate:
    if os.environ.get("AWS_CONTAINER_CREDENTIALS_RELATIVE_URI"):
        return True
    # for EC2:
    try:
        return requests.get("http://169.254.169.254/latest/meta-data/", timeout=0.2).ok
    except requests.exceptions.RequestException:
        return False
    

def download_model_if_on_aws(bucket_name: str, S3_model_path: str, local_model_path: str):
    """loads from S3"""
    if is_running_on_aws():
        try:
            download_model_from_s3(bucket_name, S3_model_path, local_model_path)
        except requests.exceptions.RequestException:
            print("encountered an error while downloading model from S3")
    else:
        print("skipping S3 download, because code is not running on AWS")