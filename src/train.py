# Imports and Constants
import boto3
import pandas as pd
import sagemaker
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.workflow.parameters import ParameterInteger, ParameterString, ParameterFloat
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.workflow.steps import ProcessingStep
from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput
from sagemaker.tuner import HyperparameterTuner, ContinuousParameter, IntegerParameter

# Initialize AWS clients and parameters
s3_client = boto3.resource('s3') 
pipeline_session = PipelineSession() 
sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role() 
default_bucket = sagemaker_session.default_bucket() 

# Parameters
processing_instance_count = ParameterInteger(name="ProcessingInstanceCount", default_value=1)
processing_instance_type = ParameterString(name="ProcessingInstanceType", default_value="ml.m5.xlarge")
training_instance_type = ParameterString(name="TrainingInstanceType", default_value="ml.m5.xlarge")
input_data = "s3://your-bucket/path/to/storedata_total.csv"  # Update with actual path
model_path = f"s3://{default_bucket}/output"

# Define Processing Step
sklearn_processor = SKLearnProcessor(
    framework_version="1.0-1",
    instance_type=processing_instance_type,
    instance_count=processing_instance_count,
    base_job_name="sklearn-churn-process",
    role=role,
    sagemaker_session=pipeline_session,
)

processor_args = sklearn_processor.run(
    inputs=[ProcessingInput(source=input_data, destination="/opt/ml/processing/input")],
    outputs=[
        ProcessingOutput(output_name="train", source="/opt/ml/processing/train",
                         destination=f"s3://{default_bucket}/output/train"),
        ProcessingOutput(output_name="validation", source="/opt/ml/processing/validation",
                         destination=f"s3://{default_bucket}/output/validation"),
        ProcessingOutput(output_name="test", source="/opt/ml/processing/test",
                         destination=f"s3://{default_bucket}/output/test")
    ],
    code="src/preprocess_churn.py",
)
step_process = ProcessingStep(name="ChurnModelProcess", step_args=processor_args)

# Hyperparameter Tuning
image_uri = sagemaker.image_uris.retrieve(
    framework="xgboost",
    region=sagemaker_session.boto_region_name,
    version="1.0-1",
    py_version="py3",
    instance_type=training_instance_type,
)

fixed_hyperparameters = {
    "eval_metric": "auc",
    "objective": "binary:logistic",
    "num_round": "100",
    "rate_drop": "0.3",
    "tweedie_variance_power": "1.4"
}

xgb_train = Estimator(
    image_uri=image_uri,
    instance_type=training_instance_type,
    instance_count=1,
    hyperparameters=fixed_hyperparameters,
    output_path=model_path,
    base_job_name="churn-train",
    sagemaker_session=pipeline_session,
    role=role,
)

hyperparameter_ranges = {
    "eta": ContinuousParameter(0, 1),
    "min_child_weight": IntegerParameter(1, 10),
    "alpha": ContinuousParameter(0, 2),
    "max_depth": IntegerParameter(1, 10),
}

objective_metric_name = "validation:auc"

tuner = HyperparameterTuner(
    xgb_train,
    objective_metric_name,
    hyperparameter_ranges,
    max_jobs=2,
    max_parallel_jobs=2,
)

hpo_args = tuner.fit(
    inputs={
        "train": TrainingInput(
            s3_data=step_process.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri,
            content_type="text/csv",
        ),
        "validation": TrainingInput(
            s3_data=step_process.properties.ProcessingOutputConfig.Outputs["validation"].S3Output.S3Uri,
            content_type="text/csv",
        ),
    }
)

# Add more steps for evaluation and model registration as needed
