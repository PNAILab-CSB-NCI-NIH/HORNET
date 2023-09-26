import unittest
from unittest import mock
import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.uml import uml_analysis

class TestUMLAnalysis(unittest.TestCase):

    def setUp(self):
        import warnings
        warnings.filterwarnings(action='ignore', category=FutureWarning)

        data_path = os.path.dirname(os.path.realpath(__file__)) + "/../test_data"
        original_file = f"{data_path}/Full_Trajectory.csv"
        self.folder = ".data_test"
        self.input_file = f"{self.folder}/Full_Trajectory.csv"
        self.expected_filtered = pd.read_csv(f"{data_path}/Filtered_Data.csv")
        self.expected_cluster = pd.read_csv(f"{data_path}/Select_Cluster.csv")
        self.expected_cohort = pd.read_csv(f"{data_path}/Final_Cohort.csv")

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        os.system(f"cp {original_file} {self.folder}")
    
    def tearDown(self):
        os.system(f"rm -r {self.folder}")

    @mock.patch('hornet.uml.input', create=True)
    def test_read_data(self, mocked_input):
        n_components_mock = '8'
        n_clusters_mock = '3'
        mocked_input.side_effect = [n_components_mock, n_clusters_mock]

        # Test that the input file is read correctly
        with mock.patch("hornet.uml.plt.show") as show_patch:
            uml_analysis(self.input_file)
            self.assertTrue(show_patch.called)
        
        df_filtered = pd.read_csv(f"{self.folder}/Filtered_Data.csv")
        df_cluster = pd.read_csv(f"{self.folder}/Select_Cluster.csv")
        df_cohort = pd.read_csv(f"{self.folder}/Final_Cohort.csv")

        self.assertEqual(len(df_filtered), len(self.expected_filtered))
        self.assertEqual(len(df_cluster), len(self.expected_cluster))
        self.assertEqual(len(df_cohort), len(self.expected_cohort))

if __name__ == '__main__':
    unittest.main()