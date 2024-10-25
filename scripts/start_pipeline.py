# scripts/start_pipeline.py

import boto3

def start_pipeline(pipeline_name):
    """Start an AWS CodePipeline execution."""
    client = boto3.client('codepipeline')
    response = client.start_pipeline_execution(name=pipeline_name)
    print(f"Started pipeline execution: {response['pipelineExecutionId']}")

if __name__ == "__main__":
    start_pipeline('your-pipeline-name')
