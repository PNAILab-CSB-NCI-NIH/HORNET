import os
import pandas as pd
import numpy as np
import unittest
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.model import standardize

class TestStandardize(unittest.TestCase):
    
    def setUp(self):
        self.df = pd.DataFrame({
            'etot': [1, 2, 3], 'local': [4, 5, 6], 'go': [7, 8, 9], 'repul': [10, 11, 12],
            'stack': [13, 14, 15], 'hbond': [16, 17, 18], 'elect': [19, 20, 21],
            'afmfit': [22, 23, 24], 'afmcc': [25, 26, 27], 'cc7xEtot': [28, 29, 30]})
        self.mean = {'etot': 2, 'local': 5, 'go': 8, 'repul': 11, 'stack': 14, 'hbond': 17, 'elect': 20, 'afmfit': 23, 'afmcc': 26, 'cc7xEtot': 29}
        self.sigma = {'etot': 1, 'local': 1, 'go': 1, 'repul': 1, 'stack': 1, 'hbond': 1, 'elect': 1, 'afmfit': 1, 'afmcc': 1, 'cc7xEtot': 1}
    
    def test_standardize(self):
        expected_df = pd.DataFrame({
            'etot': [-1., 0., 1.], 'local': [-1., 0., 1.], 'go': [-1., 0., 1.], 'repul': [-1., 0., 1.],
            'stack': [-1., 0., 1.], 'hbond': [-1., 0., 1.], 'elect': [-1., 0., 1.],
            'afmfit': [-1., 0., 1.], 'afmcc': [-1., 0., 1.], 'cc7xEtot': [-1., 0., 1.]})
        df_result = standardize(self.df, self.mean, self.sigma)
        self.assertTrue(expected_df.equals(df_result))

    def test_standardize_mean_none(self):
        with self.assertRaises(ValueError):
            standardize(self.df, None, self.sigma)

    def test_standardize_sigma_none(self):
        with self.assertRaises(ValueError):
            standardize(self.df, self.mean, None)

    def test_standardize_missing_key_mean(self):
        mean = {'etot': 2, 'local': 5, 'go': 8, 'repul': 11, 'stack': 14, 'hbond': 17, 'elect': 20, 'afmfit': 23, 'afmcc': 26}
        with self.assertRaises(KeyError):
            standardize(self.df, mean, self.sigma)

    def test_standardize_missing_key_sigma(self):
        sigma = {'etot': 1, 'local': 1, 'go': 1, 'repul': 1, 'stack': 1, 'hbond': 1, 'elect': 1, 'afmfit': 1, 'afmcc': 1}
        with self.assertRaises(KeyError):
            standardize(self.df, self.mean, sigma)

if __name__ == '__main__':
    unittest.main()