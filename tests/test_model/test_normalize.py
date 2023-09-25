import os
import pandas as pd
import numpy as np
import unittest
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.model import normalize

class TestNormalize(unittest.TestCase):
    
    def setUp(self):
        self.df = pd.DataFrame({
            'etot': [1., 2., 3.], 'local': [1., 2., 3.], 'go': [1., 2., 3.], 'repul': [1., 2., 3.],
            'stack': [1., 2., 3.], 'hbond': [1., 2., 3.], 'elect': [1., 2., 3.],
            'afmfit': [1., 2., 3.], 'afmcc': [1., 2., 3.], 'cc7xEtot': [1., 2., 3.],
            'baseP': [2., 2., 3.], 'baseS': [1., 2., 3.], 'kapa': [2., 2., 2.]})
    
    def test_normalize(self):
        n_residues = 1/3
        expected_df = pd.DataFrame({
            'etot': [1., 2., 3.], 'local': [1., 2., 3.], 'go': [1., 2., 3.], 'repul': [1., 2., 3.],
            'stack': [1., 1., 1.], 'hbond': [0.5, 1., 1.,], 'elect': [1., 2., 3.],
            'afmfit': [0.5, 1, 1.5], 'afmcc': [1., 2., 3.], 'cc7xEtot': [1., 2., 3.],
            'baseP': [2., 2., 3.], 'baseS': [1., 2., 3.], 'kapa': [2., 2., 2.]})
        df_result = normalize(self.df, n_residues)
        self.assertTrue(expected_df.equals(df_result))

    def test_normalize_custom(self):
        n_residues = 1/6
        expected_df = pd.DataFrame({
            'etot': [1., 2., 3.], 'local': [2., 4., 6.], 'go': [2., 4., 6.], 'repul': [2., 4., 6.],
            'stack': [1., 1., 1.], 'hbond': [0.5, 1., 1.,], 'elect': [2., 4., 6.],
            'afmfit': [1., 2., 3.], 'afmcc': [1., 2., 3.], 'cc7xEtot': [1., 2., 3.],
            'baseP': [2., 2., 3.], 'baseS': [1., 2., 3.], 'kapa': [2., 2., 2.]})
        df_result = normalize(self.df, n_residues)
        self.assertTrue(expected_df.equals(df_result))

if __name__ == '__main__':
    unittest.main()