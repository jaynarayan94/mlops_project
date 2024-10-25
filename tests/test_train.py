# tests/test_train.py

import unittest
from src.train import train_model
import pandas as pd

class TestTrainModel(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [5, 4, 3, 2, 1],
            'target_column': [0, 1, 0, 1, 0]
        })

    def test_model_training(self):
        model = train_model(self.data)
        self.assertIsNotNone(model)

if __name__ == '__main__':
    unittest.main()
