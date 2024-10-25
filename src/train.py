import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import yaml
import joblib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from mlflow.models import infer_signature
from sklearn.model_selection import train_test_split, GridSearchCV
import os
from urllib.parse import urlparse
import mlflow
import boto3
from botocore.exceptions import NoCredentialsError
from src.logger import training_logger  # Import the logger

def save_model_to_s3(model, model_path, s3_bucket):
    try:
        # Create a boto3 S3 client
        s3 = boto3.client('s3')

        # Upload the model to S3
        s3.upload_file(model_path, s3_bucket, model_path)
        training_logger.info(f'Model saved to S3 bucket: {s3_bucket}/{model_path}')
    except FileNotFoundError:
        training_logger.error(f'The file was not found: {model_path}')
    except NoCredentialsError:
        training_logger.error('AWS credentials not available.')

def hyperparameter_tuning(X_train, y_train, param_grid):
    rf = RandomForestClassifier()
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)
    return grid_search

# Load the parameters from params.yaml
params = yaml.safe_load(open("configs/params.yaml"))["train"]

def train(data_path, model_path, random_state, n_estimators, max_depth, s3_bucket):
    training_logger.info('Training started.')
    data = pd.read_csv(data_path)
    X = data.drop(columns=['Outcome'], axis=1)
    y = data["Outcome"]

    mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])

    # Start the MLflow run
    with mlflow.start_run():
        training_logger.info('Started MLflow run.')

        # Split the data into training and test dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=random_state)
        signature = infer_signature(X_train, y_train)

        # Define the hyperparameter grid
        param_grid = {
            'n_estimators': [50, 100],
            'max_depth': [5, 10],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 4],
            'max_features': ['auto', 'sqrt'],
            'bootstrap': [True],
            'criterion': ['gini', 'entropy'],
            'class_weight': ['balanced'],
        }
        
        # Perform Hyperparameter tuning.
        grid_search = hyperparameter_tuning(X_train, y_train, param_grid)

        # Get the best model
        best_model = grid_search.best_estimator_

        # Predict using the best estimator and evaluate the model
        y_pred = best_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        training_logger.info(f"Accuracy: {accuracy}")

        # Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_param("best_n_estimators", best_model.n_estimators)
        mlflow.log_param("best_max_depth", best_model.max_depth)
        mlflow.log_param("best_min_samples_split", best_model.min_samples_split)
        mlflow.log_param("best_min_samples_leaf", best_model.min_samples_leaf)
        mlflow.log_param("best_max_features", best_model.max_features)
        mlflow.log_param("best_bootstrap_condition", best_model.bootstrap)
        mlflow.log_param("best_model_criterion", best_model.criterion)
        mlflow.log_param("best_class_weight", best_model.class_weight)

        # Log confusion matrix and classification report
        cm = confusion_matrix(y_test, y_pred)
        cr = classification_report(y_test, y_pred)

        mlflow.log_text(str(cm), "confusion_matrix.txt")
        mlflow.log_text(cr, "classification_report.txt")

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store != 'file':
            mlflow.sklearn.log_model(best_model, "RFModel", registered_model_name="BestRFModel")
        else:
            mlflow.sklearn.log_model(best_model, "RFModel", signature=signature)

        # Save model locally and to S3
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(best_model, model_path)
        save_model_to_s3(best_model, model_path, s3_bucket)
        training_logger.info('Training completed and model saved.')

if __name__ == "__main__":
    train(params['data'], params['model'], params['random_state'], params['n_estimators'], params['max_depth'], params['s3_bucket'])
