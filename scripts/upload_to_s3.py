# scripts/upload_to_s3.py

import boto3
import os

def upload_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket."""
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response

if __name__ == "__main__":
    upload_to_s3('../data/processed/processed_data.csv', 'your-s3-bucket-name')
