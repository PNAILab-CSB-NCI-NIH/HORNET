import os
import pandas as pd
import numpy as np
import unittest
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.uml import get_min_cluster_index

class TestGetMinClusterIndex(unittest.TestCase):

    def setUp(self):
        # create a sample DataFrame
        self.df = pd.DataFrame({
            'Segment': [1, 1, 2, 2, 3, 3],
            'Feature': [10, 20, 30, 40, 50, 60]
        })

    def test_get_min_cluster_feature(self):
        # Test case 1: testing with column 'Feature'
        means, index = get_min_cluster_index(self.df, 'Feature')
        self.assertEqual(means, {1: 15.0, 2: 35.0, 3: 55.0})
        self.assertEqual(index, 1)

    def test_get_min_cluster_segment(self):
        # Test case 2: testing with column 'Segment'
        means, index = get_min_cluster_index(self.df, 'Segment')
        self.assertEqual(means, {1: 1.0, 2: 2.0, 3: 3.0})
        self.assertEqual(index, 1)

    def test_get_min_cluster_nonexistent(self):
        # Test case 3: testing with column 'Nonexistent'
        with self.assertRaises(ValueError):
            get_min_cluster_index(self.df, 'Nonexistent')

if __name__ == '__main__':
    unittest.main()