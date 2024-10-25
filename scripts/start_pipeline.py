import sys
import os
import boto3
import logging

# Add project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.logger import setup_logger

# Set up logger
logger = setup_logger('pipeline_logger', 'logs/pipeline_logs.log')

def start_pipeline(pipeline_name):
    """Start an AWS CodePipeline execution."""
    client = boto3.client('codepipeline')
    
    try:
        response = client.start_pipeline_execution(name=pipeline_name)
        logger.info(f"Started pipeline execution: {response['pipelineExecutionId']}")
        print(f"Started pipeline execution: {response['pipelineExecutionId']}")
    except client.exceptions.InvalidPipelineNameException:
        logger.error(f"Invalid pipeline name: {pipeline_name}")
        print(f"Invalid pipeline name: {pipeline_name}")
    except client.exceptions.PipelineNotFoundException:
        logger.error(f"Pipeline not found: {pipeline_name}")
        print(f"Pipeline not found: {pipeline_name}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    start_pipeline('churn-pipeline')
