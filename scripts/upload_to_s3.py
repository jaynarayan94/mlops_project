# src/upload_to_s3.py

import logging
import boto3
import os
from src.logger import setup_logger

# Set up logger
logger = setup_logger('upload_logger', 'logs/upload_logs.log')

def upload_to_s3(file_path, bucket_name, object_name=None):
    """Upload a file to an S3 bucket."""
    if object_name is None:
        object_name = os.path.basename(file_path)

    logger.info(f'Starting upload of {file_path} to bucket {bucket_name} as {object_name}.')
    
    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(file_path, bucket_name, object_name)
        logger.info('Upload completed successfully.')
    except FileNotFoundError:
        logger.error(f'The file {file_path} was not found.')
    except Exception as e:
        logger.error(f'An error occurred: {str(e)}')

if __name__ == "__main__":
    upload_to_s3('../data/processed/processed_data.csv', 'mlops-project-jay')
