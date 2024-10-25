import os
import shutil

# Define the base directory for the project
base_dir = "mlops_project"

# Define the project structure
project_structure = {
    "data": {
        "raw": {
            "storedata_total.csv": "",  # Raw data file
            "__init__.py": "# This package contains raw data files.\n"
        },
        "processed": {
            "processed_data.csv": "",  # Processed data file
            "__init__.py": "# This package contains processed data files.\n"
        },
    },
    "notebooks": {
        "eda.ipynb": "",  # Jupyter notebook for exploratory data analysis
    },
    "src": {
        "train.py": "",  # Training script for SageMaker
        "utils.py": "",  # Utility functions
        "Dockerfile": "",  # Dockerfile for SageMaker container
        "requirements.txt": "",  # Python dependencies
        "__init__.py": "# This package contains source code for the project.\n"
    },
    "infrastructure": {
        "pipeline.yaml": "",  # AWS CodePipeline YAML configuration
        "trust-policy.json": "",  # IAM trust policy for SageMaker role
        "create-roles.sh": "#!/bin/bash\n# Script to create IAM roles for SageMaker\n",
    },
    "scripts": {
        "upload_to_s3.py": "",  # Script to upload data to S3
        "start_pipeline.py": "",  # Script to start the pipeline
        "__init__.py": "# This package contains automation scripts.\n"
    },
    "logs": {
        "training_logs.log": "",  # Logs from training jobs
        "__init__.py": "# This package contains log files.\n"
    },
    "tests": {
        "test_train.py": "",  # Tests for the training script
        "test_utils.py": "",  # Tests for utility functions
        "__init__.py": "# This package contains unit tests for the project.\n"
    },
    ".gitignore": "",  # Git ignore file
    "README.md": "# MLOps Project\nThis project uses AWS services to implement an end-to-end machine learning pipeline.\n",
    "requirements.txt": ""  # List of Python packages needed for the project
}

# Create the project structure
def create_structure(base_dir, structure):
    for name, content in structure.items():
        path = os.path.join(base_dir, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)  # Recursively create subdirectories
        else:
            with open(path, 'w') as file:
                file.write(content)  # Create files with specified content
            print(f"Created file: {path}")

# Check if the base directory already exists
if os.path.exists(base_dir):
    shutil.rmtree(base_dir)  # Remove the existing directory and all its contents

# Create a new base directory
os.makedirs(base_dir)
create_structure(base_dir, project_structure)
print("Project structure created successfully!")
