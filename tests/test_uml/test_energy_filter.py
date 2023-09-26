import os
import pandas as pd
import numpy as np
import unittest
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.uml import energy_filter

class TestEnergyFilter(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.df = pd.DataFrame({
            'repul': [1, 2, 3, 4, 5],
            'hbond': [1, 2, 3, 4, 5],
            'stage': [1, 2, 3, 4, 5],
            'stack': [1, 2, 3, 4, 5],
            'local': [1, 2, 3, 4, 5],
            'afmcc': [1, 2, 3, 4, 5],
            'etot': [1, 2, 3, 4, 5]
        })
        self.expected_output = pd.DataFrame({
            'repul': [1, 2, 3, 4],
            'hbond': [1, 2, 3, 4],
            'stage': [1, 2, 3, 4],
            'stack': [1, 2, 3, 4],
            'local': [1, 2, 3, 4],
            'afmcc': [1, 2, 3, 4],
            'etot': [1, 2, 3, 4]
        })

    def test_energy_filter_step1(self):
        # Test the filtering logic of step 1
        filtered_df = energy_filter(self.df)
        self.assertTrue(filtered_df.reset_index(drop=True).equals(self.expected_output))

if __name__ == '__main__':
    unittest.main()