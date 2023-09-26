import os
import pandas as pd
import unittest
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.uml import create_features

class TestCreateFeatures(unittest.TestCase):
    
    def test_create_features_creation(self):
        # Test case 1: Check if 'afmccpow' column is created correctly
        df = pd.DataFrame({'afmcc': [1, 0.5], 'etot': [3, 4]})
        df = create_features(df)
        expected_output = pd.DataFrame({'afmcc': [1, 0.5], 'etot': [3, 4], 'afmccpow': [1, 0.0078125], 'etotPower': [3, 0.03125]})
        self.assertTrue(df.equals(expected_output))

    def test_create_features_empty(self):
        # Test case 2: Empty df
        df = pd.DataFrame({'afmcc': [], 'etot': []})
        df = create_features(df)
        expected_output = pd.DataFrame({'afmcc': [], 'etot': [], 'afmccpow': [], 'etotPower': []})
        self.assertTrue(df.equals(expected_output))

if __name__ == '__main__':
    unittest.main()