# tests/test_utils.py

import unittest
from src.utils import load_data, preprocess_data
import pandas as pd

class TestUtils(unittest.TestCase):

    def test_load_data(self):
        # Assuming a test CSV file exists
        data = load_data('../data/raw/storedata_total.csv')
        self.assertEqual(len(data), expected_length)

    def test_preprocess_data(self):
        data = pd.DataFrame({'A': [1, 2, None], 'B': [4, None, 6]})
        processed_data = preprocess_data(data)
        self.assertFalse(processed_data.isnull().values.any())

if __name__ == '__main__':
    unittest.main()
