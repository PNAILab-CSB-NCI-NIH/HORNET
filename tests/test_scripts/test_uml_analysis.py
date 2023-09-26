import sys
import unittest
from unittest.mock import patch
import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../scripts")
from uml_analysis import args, uml_analysis

class TestUmlAnalysis(unittest.TestCase):

    def setUp(self):
        import warnings
        warnings.filterwarnings(action='ignore', category=FutureWarning)
        
        self.full_trajectory = os.path.dirname(os.path.realpath(__file__)) + "/../test_data/Full_Trajectory.csv"
        self.filtered_data = os.path.dirname(os.path.realpath(__file__)) + "/../test_data/Filtered_Data.csv"
        self.select_cluster = os.path.dirname(os.path.realpath(__file__)) + "/../test_data/Select_Cluster.csv"
        self.final_cohort = os.path.dirname(os.path.realpath(__file__)) + "/../test_data/Final_Cohort.csv"
        self.input_path = ".test_data"
        self.file_path = f"{self.input_path}/Full_Trajectory.csv"
    
        # Create temporary dir
        if not os.path.exists(self.input_path):
            os.makedirs(self.input_path)

        # Copy file
        os.system(f"cp {self.full_trajectory} {self.file_path}")

    def tearDown(self):
        os.system(f"rm -r {self.input_path}")

    # Test help option
    @patch('uml_analysis.help')
    def test_help_option(self, mock_help):
        argslist = ['uml_analysis.py', '-h']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 0)
        mock_help.assert_called()
        
    # Test long help option
    @patch('uml_analysis.help')
    def test_long_help_option(self, mock_help):
        argslist = ['uml_analysis.py', '--help']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 0)
        mock_help.assert_called()
        
    # Test input file provided
    def test_input_file_provided(self):
        argslist = ['uml_analysis.py', 'file.txt']
        input_file = args(argslist)
        self.assertEqual(input_file, 'file.txt')
        
    # Test no input file provided
    @patch('uml_analysis.help')
    def test_no_input_file_provided(self, mock_help):
        argslist = ['uml_analysis.py']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 1)
        mock_help.assert_called()

    @patch('hornet.uml.input', create=True)
    def test_uml_analysis(self, mocked_input):
        argslist = ['uml_analysis.py', self.file_path]
        input_file = args(argslist)

        n_components_mock = '8'
        n_clusters_mock = '3'
        mocked_input.side_effect = [n_components_mock, n_clusters_mock]

        with patch("hornet.uml.plt.show") as show_patch:
            uml_analysis(input_file)

        self.assertTrue(os.path.exists(f"{self.input_path}/Filtered_Data.csv"))
        self.assertTrue(os.path.exists(f"{self.input_path}/Select_Cluster.csv"))
        self.assertTrue(os.path.exists(f"{self.input_path}/Final_Cohort.csv"))

        self.assertTrue(len(pd.read_csv(f"{self.input_path}/Filtered_Data.csv")) == len(pd.read_csv(self.filtered_data)))
        self.assertTrue(len(pd.read_csv(f"{self.input_path}/Select_Cluster.csv")) == len(pd.read_csv(self.select_cluster)))
        self.assertTrue(len(pd.read_csv(f"{self.input_path}/Final_Cohort.csv")) == len(pd.read_csv(self.final_cohort)))
        
if __name__ == '__main__':
    unittest.main()