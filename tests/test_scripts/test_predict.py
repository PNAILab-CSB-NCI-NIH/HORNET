import sys
import unittest
from unittest.mock import patch
import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../scripts")
from predict import args, predict

class TestPredict(unittest.TestCase):

    def setUp(self):
        origin = os.path.dirname(os.path.realpath(__file__)) + "/../test_data"
        self.predictions = os.path.dirname(os.path.realpath(__file__)) + "/../test_data/Final_Cohort_prediction.csv"
        self.top10 = os.path.dirname(os.path.realpath(__file__)) + "/../test_data/Final_Cohort_Top10.csv"
        self.input_path = ".test_data"
    
        # Create temporary dir
        if not os.path.exists(self.input_path):
            os.makedirs(self.input_path)

        # Copy file
        os.system(f"cp {origin}/Final_Cohort.csv {self.input_path}")
        os.system(f"cp -r {os.path.dirname(os.path.realpath(__file__))}/../../models/hornet {self.input_path}")

    def tearDown(self):
        os.system(f"rm -r {self.input_path}")

    # Test help option
    @patch('predict.help')
    def test_help_option(self, mock_help):
        argslist = ['predict.py', '-h']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 0)
        mock_help.assert_called()
        
    # Test long help option
    @patch('predict.help')
    def test_long_help_option(self, mock_help):
        argslist = ['predict.py', '--help']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 0)
        mock_help.assert_called()
        
    # Test inputs provided
    def test_inputs_provided(self):
        argslist = ['predict.py', '-o', 'output_folder', '-m', 'model_location', '-d', 'dataset', '-n', '5', '-k', '3', '-f', '2']
        output_folder, model_location, dataset, n_residues, max_kappa, min_frame = args(argslist)
        self.assertTrue(output_folder.endswith('output_folder'))
        self.assertTrue(model_location.endswith('model_location'))
        self.assertEqual(dataset, 'dataset')
        self.assertEqual(n_residues, 5)
        self.assertEqual(max_kappa, 3)
        self.assertEqual(min_frame, 2)

    # Test missing model location
    def test_missing_model(self):
        argslist = ['predict.py', '-o', 'output_folder', '-d', 'dataset', '-n', '5', '-k', '3', '-f', '2']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 1)

    # Test missing dataset
    def test_missing_dataset(self):
        argslist = ['predict.py', '-o', 'output_folder', '-m', 'model_location', '-n', '5', '-k', '3', '-f', '2']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 1)

    # Test missing residues
    def test_missing_residues(self):
        argslist = ['predict.py', '-o', 'output_folder', '-m', 'model_location', '-d', 'dataset', '-k', '3', '-f', '2']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 1)

    # Test default
    def test_default(self):
        argslist = ['predict.py', '-d', 'dataset', '-m', 'model_location', '-n', '5',]
        output_folder, model_location, dataset, n_residues, max_kappa, min_frame = args(argslist)
        self.assertTrue(dataset.endswith('dataset'))
        self.assertTrue(model_location.endswith('model_location'))
        self.assertEqual(n_residues, 5)

    # Test input issue residues
    def test_input_issue_residues(self):
        argslist = ['predict.py', '-d', 'dataset', '-m', 'model_location', '-n', 'a']
        with self.assertRaises(ValueError):
            args(argslist)

    # Test input issue kappa
    def test_input_issue_kappa(self):
        argslist = ['predict.py', '-d', 'dataset', '-m', 'model_location', '-n', '5', '-k', 'a']
        with self.assertRaises(ValueError):
            args(argslist)

    # Test input issue frame
    def test_input_issue_frame(self):
        argslist = ['predict.py', '-d', 'dataset', '-m', 'model_location', '-n', '5', '-f', 'a']
        with self.assertRaises(ValueError):
            args(argslist)
        
    def test_predict(self):
        argslist = ['predict.py', '-o', self.input_path, '-d', f"{self.input_path}/Final_Cohort.csv", '-m', f"{self.input_path}/hornet", '-n', '268', '-k', '50', '-f', '2000']
        output_folder, model_location, dataset, n_residues, max_kappa, min_frame = args(argslist)

        self.assertTrue(output_folder.endswith(f"{self.input_path}"))
        self.assertTrue(model_location.endswith(f"{self.input_path}/hornet"))
        self.assertTrue(dataset.endswith(f"{self.input_path}/Final_Cohort.csv"))
        self.assertEqual(n_residues, 268)
        self.assertEqual(max_kappa, 50)
        self.assertEqual(min_frame, 2000)

        predict(output_folder, model_location, dataset, n_residues, max_kappa, min_frame)

        # Assert files were created and have expected length
        self.assertTrue(os.path.exists(f"{self.input_path}/Final_Cohort_prediction.csv"))
        self.assertTrue(os.path.exists(f"{self.input_path}/Final_Cohort_Top10.csv"))
        self.assertTrue(len(pd.read_csv(f"{self.input_path}/Final_Cohort_Top10.csv")) == len(pd.read_csv(self.top10)))
        self.assertTrue(len(pd.read_csv(f"{self.input_path}/Final_Cohort_prediction.csv")) == len(pd.read_csv(self.predictions)))

        # Assert predictions are exactly the same
        self.assertTrue(set(pd.read_csv(self.top10)['prediction'])) == set(pd.read_csv(f"{self.input_path}/Final_Cohort_Top10.csv")['prediction'])

        
if __name__ == '__main__':
    unittest.main()