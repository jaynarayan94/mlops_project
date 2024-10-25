#!/bin/bash
# Script to create IAM roles for SageMaker

# Create IAM Role for SageMaker
aws iam create-role --role-name SageMakerExecutionRole --assume-role-policy-document file://trust-policy.json

# Attach policies
aws iam attach-role-policy --role-name SageMakerExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonSageMakerFullAccess
