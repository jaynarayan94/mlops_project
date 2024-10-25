# src/utils.py

import os
import tempfile
import numpy as np
import pandas as pd
import datetime as dt

def preprocess_data(base_dir="/opt/ml/processing"):
    """Preprocess the store data and save train, validation, and test datasets."""

    # Read Data
    df = pd.read_csv(f"{base_dir}/input/storedata_total.csv")

    # Convert created column to datetime
    df["created"] = pd.to_datetime(df["created"])

    # Convert firstorder and lastorder to datetime datatype
    df["firstorder"] = pd.to_datetime(df["firstorder"], errors='coerce')
    df["lastorder"] = pd.to_datetime(df["lastorder"], errors='coerce')

    # Drop Rows with Null Values
    df = df.dropna()

    # Create column for days between the last order and the first order
    df['first_last_days_diff'] = (df['lastorder'] - df['firstorder']).dt.days

    # Create column for days between customer record creation and the first order
    df['created_first_days_diff'] = (df['created'] - df['firstorder']).dt.days

    # Drop unnecessary columns
    df.drop(['custid', 'created', 'firstorder', 'lastorder'], axis=1, inplace=True)

    # Apply one hot encoding on favday and city columns
    df = pd.get_dummies(df, prefix=['favday', 'city'], columns=['favday', 'city'])

    # Split features and target variable
    y = df.pop("retained")
    X_pre = df
    y_pre = y.to_numpy().reshape(len(y), 1)
    X = np.concatenate((y_pre, X_pre), axis=1)
    np.random.shuffle(X)

    # Split into Train, Validation, and Test datasets
    train, validation, test = np.split(X, [int(.7 * len(X)), int(.85 * len(X))])

    # Convert to DataFrames
    train_df = pd.DataFrame(train)
    validation_df = pd.DataFrame(validation)
    test_df = pd.DataFrame(test)

    # Convert the label column to integer
    train_df[0] = train_df[0].astype(int)
    validation_df[0] = validation_df[0].astype(int)
    test_df[0] = test_df[0].astype(int)

    # Save the DataFrames as CSV files
    train_df.to_csv(f"{base_dir}/train/train.csv", header=False, index=False)
    validation_df.to_csv(f"{base_dir}/validation/validation.csv", header=False, index=False)
    test_df.to_csv(f"{base_dir}/test/test.csv", header=False, index=False)

if __name__ == "__main__":
    preprocess_data()
