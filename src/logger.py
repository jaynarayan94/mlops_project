# src/logger.py
import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    """Function to set up a logger."""
    # Create a directory for logs if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

# Example of setting up a logger
training_logger = setup_logger('training_logger', 'logs/training_logs.log')
