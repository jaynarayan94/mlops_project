# src/Dockerfile

# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . .

# Command to run when starting the container
CMD ["python", "train.py"]
# src/Dockerfile

# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . .

# Command to run when starting the container
CMD ["python", "train.py"]
