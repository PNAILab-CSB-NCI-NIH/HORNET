import sys
import unittest
from unittest.mock import patch
import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../scripts")
from prepare_inputs import args, prepare_inputs

class TestPrepareInputs(unittest.TestCase):

    def setUp(self):
        origin = os.path.dirname(os.path.realpath(__file__)) + "/../test_data"
        self.full_trajectory = os.path.dirname(os.path.realpath(__file__)) + "/../test_data/Full_Trajectory.csv"
        self.input_path = ".test_data"
    
        # Create temporary dir
        if not os.path.exists(self.input_path):
            os.makedirs(self.input_path)

        # Copy file
        os.system(f"cp {origin}/en_allk*.txt {self.input_path}")
        os.system(f"cp {origin}/bases_k*.csv {self.input_path}")

    def tearDown(self):
        os.system(f"rm -r {self.input_path}")
        if os.path.exists(".tmp"):
            os.system(f"rm -r .tmp")

    # Test help option
    @patch('prepare_inputs.help')
    def test_help_option(self, mock_help):
        argslist = ['prepare_inputs.py', '-h']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 0)
        mock_help.assert_called()
        
    # Test long help option
    @patch('prepare_inputs.help')
    def test_long_help_option(self, mock_help):
        argslist = ['prepare_inputs.py', '--help']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 0)
        mock_help.assert_called()
        
    # Test input file provided
    def test_input_file_provided(self):
        argslist = ['prepare_inputs.py', 'file.txt']
        input_file, bp, bs = args(argslist)
        self.assertTrue(input_file.split("/")[-1], 'file.txt')
        self.assertEqual(bp, -1)
        self.assertEqual(bs, -1)
        
    # Test no input file provided
    @patch('prepare_inputs.help')
    def test_no_input_file_provided(self, mock_help):
        argslist = ['prepare_inputs.py']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 1)
        mock_help.assert_called()
        
    # Test bp and bs provided
    @patch('prepare_inputs.help')
    def test_bp_and_bs_input_provided(self, mock_help):
        argslist = ['prepare_inputs.py', 'file.txt', '1', '2']
        input_file, bp, bs = args(argslist)
        self.assertEqual(input_file.split("/")[-1], 'file.txt')
        self.assertEqual(bp, 1)
        self.assertEqual(bs, 2)
        
    # Test bp and bs provided
    @patch('prepare_inputs.help')
    def test_no_bs_input_provided(self, mock_help):
        argslist = ['prepare_inputs.py', 'file.txt', '1']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 1)
        mock_help.assert_called()
        
    def test_prepare_inputs_averaged(self):
        argslist = ['prepare_inputs.py', self.input_path, '88', '192']
        input_file, bp, bs = args(argslist)

        prepare_inputs(input_file, bp, bs)

        self.assertTrue(os.path.exists(f"{self.input_path}/Full_Trajectory.csv"))
        
    def test_prepare_inputs(self):
        argslist = ['prepare_inputs.py', self.input_path]
        input_file, bp, bs = args(argslist)

        prepare_inputs(input_file, bp, bs)

        self.assertTrue(os.path.exists(f"{self.input_path}/Full_Trajectory.csv"))
        self.assertTrue(len(pd.read_csv(f"{self.input_path}/Full_Trajectory.csv")) == len(pd.read_csv(self.full_trajectory)))
        
if __name__ == '__main__':
    unittest.main()