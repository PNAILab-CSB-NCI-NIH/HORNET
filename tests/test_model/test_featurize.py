import os
import pandas as pd
import unittest
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.model import featurize

class TestFeaturize(unittest.TestCase):
    
    def test_featurize_creation(self):
        # Test case 1: Check if 'afmccpow' column is created correctly
        df = pd.DataFrame({'afmcc': [1, 0.5], 'local': [1, 2], 'go': [1, 2], 'repul': [1, 2], 'elect': [1, 2], 'stack': [1, 2], 'hbond': [1, 2]})
        df = featurize(df)
        expected_output = pd.DataFrame({'afmcc': [1, 0.5], 'local': [1, 2], 'go': [1, 2], 'repul': [1, 2], 'elect': [1, 2], 'stack': [1, 2], 'hbond': [1, 2], 'etot': [6.0, 12.0], 'cc7xEtot': [6.0, 0.09375]})
        self.assertTrue(df.equals(expected_output))

    def test_featurize_empty(self):
        # Test case 2: Empty df
        df = pd.DataFrame({'afmcc': [], 'local': [], 'go': [], 'repul': [], 'elect': [], 'stack': [], 'hbond': []})
        df = featurize(df)
        expected_output = pd.DataFrame({'afmcc': [], 'local': [], 'go': [], 'repul': [], 'elect': [], 'stack': [], 'hbond': [], 'etot': [], 'cc7xEtot': []})
        self.assertTrue(df.equals(expected_output))

if __name__ == '__main__':
    unittest.main()