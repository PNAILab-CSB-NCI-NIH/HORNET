import os
import pandas as pd
import numpy as np
import unittest
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.uml import filter_data

class TestFilterData(unittest.TestCase):
    
    def test_filter_data_frame(self):
        # Test case 1: df['kapa'] 10 - 40, df['frame'] 1000 - 5000, df['etot'] < 0, df['go'] < 0
        df = pd.DataFrame({'kapa': [10, 20, 30, 40],
                           'frame': [1000, 2000, 3000, 4000],
                           'etot': [-1, -2, -3, -4],
                           'go': [-1, -2, -3, -4]})
        expected_output = pd.DataFrame({'kapa': [30, 40],
                                        'frame': [3000, 4000],
                                        'etot': [-3, -4],
                                        'go': [-3, -4]})
        self.assertTrue(filter_data(df).reset_index(drop=True).equals(expected_output))

    def test_filter_data_kappa(self):   
        # Test case 2: df['kapa'] 10 - 55, df['frame'] > 2000, df['etot'] < 0, df['go'] < 0
        df = pd.DataFrame({'kapa': [10, 20, 30, 55],
                           'frame': [3000, 4000, 5000, 6000],
                           'etot': [-1, -2, -3, -4],
                           'go': [-1, -2, -3, -4]})
        expected_output = pd.DataFrame({'kapa': [10, 20, 30],
                                        'frame': [3000, 4000, 5000],
                                        'etot': [-1, -2, -3],
                                        'go': [-1, -2, -3]})
        self.assertTrue(filter_data(df).reset_index(drop=True).equals(expected_output))
    
    def test_filter_data_etot(self):
        # Test case 3: df['kapa'] 10 - 40, df['frame'] > 3000 - 6000, -5 < df['etot'] < 5, df['go'] < 0
        df = pd.DataFrame({'kapa': [10, 20, 30, 40],
                           'frame': [3000, 4000, 5000, 6000],
                           'etot': [-5, -2, 2, 5],
                           'go': [-1, -2, -3, -4]})
        expected_output = pd.DataFrame({'kapa': [10, 20],
                                        'frame': [3000, 4000],
                                        'etot': [-5, -2],
                                        'go': [-1, -2]})
        self.assertTrue(filter_data(df).reset_index(drop=True).equals(expected_output))
    
    def test_filter_data_go(self):
        # Test case 4: df['kapa'] 10 - 40, df['frame'] > 3000 - 6000, df['etot'] < 0, -5 < df['go'] < 5
        df = pd.DataFrame({'kapa': [10, 20, 30, 40],
                           'frame': [3000, 4000, 5000, 6000],
                           'etot': [-1, -2, -3, -4],
                           'go': [-5, -2, 2, 5]})
        expected_output = pd.DataFrame({'kapa': [10, 20],
                                        'frame': [3000, 4000],
                                        'etot': [-1, -2],
                                        'go': [-5, -2]})
        self.assertTrue(filter_data(df).reset_index(drop=True).equals(expected_output))

    def test_filter_data_empty(self):   
        # Test case 5: df is empty
        df = pd.DataFrame(columns=['kapa', 'frame', 'etot', 'go'])
        expected_output = pd.DataFrame(columns=['kapa', 'frame', 'etot', 'go'])
        self.assertTrue(filter_data(df).reset_index(drop=True).equals(expected_output))

if __name__ == '__main__':
    unittest.main()