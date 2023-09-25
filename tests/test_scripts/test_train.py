import sys
import unittest
from unittest.mock import patch
import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../scripts")
from train import args, train

class TestTrain(unittest.TestCase):

    def setUp(self):
        origin = os.path.dirname(os.path.realpath(__file__)) + "/../test_data"
        self.input_path = ".test_data"
        self.output_path = ".model_test"
    
        # Create temporary dir
        if not os.path.exists(self.input_path):
            os.makedirs(self.input_path)

        # Copy file
        os.system(f"cp {origin}/train_sample1.csv {self.input_path}")
        os.system(f"cp {origin}/train_sample2.csv {self.input_path}")
        os.system(f"cp {origin}/validation_sample.csv {self.input_path}")

    def tearDown(self):
        os.system(f"rm -r {self.input_path}")
        os.system(f"rm -r {self.output_path}")

    # Test help option
    @patch('train.help')
    def test_help_option(self, mock_help):
        argslist = ['train.py', '-h']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 0)
        mock_help.assert_called()

    # Test long help option
    @patch('train.help')
    def test_long_help_option(self, mock_help):
        argslist = ['train.py', '--help']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 0)
        mock_help.assert_called()

    # Test inputs provided
    def test_inputs_provided(self):
        argslist = ['train.py', '-o', 'output_folder', '-d', 'dataset', '-n', '5', '-k', '3', '-f', '2', '-v', 'validation', '-vn', '268', '-e', '300', '-l', 'mse', '-s', '101']
        output_folder, dataset, n_residues, validation, validation_residues, max_epochs, max_kappa, min_frame, loss_function, seed = args(argslist)
        self.assertTrue(output_folder.endswith('output_folder'))
        self.assertEqual(dataset, ['dataset'])
        self.assertEqual(n_residues, [5])
        self.assertEqual(max_kappa, 3)
        self.assertEqual(min_frame, 2)
        self.assertEqual(validation, 'validation')
        self.assertEqual(validation_residues, 268)
        self.assertEqual(max_epochs, 300)
        self.assertEqual(loss_function, 'mse')
        self.assertEqual(seed, 101)

    # Test missing output location
    def test_missing_output(self):
        argslist = ['train.py', '-d', 'dataset', '-n', '5']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 1)

    # Test missing dataset
    def test_missing_dataset(self):
        argslist = ['train.py', '-o', 'output_folder', '-n', '5']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 1)

    # Test missing residues
    def test_missing_residues(self):
        argslist = ['train.py', '-o', 'output_folder', '-d', 'dataset']
        with self.assertRaises(SystemExit) as cm:
            args(argslist)
        self.assertEqual(cm.exception.code, 1)

    # Test minimum input
    def test_minimum_input(self):
        argslist = ['train.py', '-o', 'output_folder', '-d', 'dataset', '-n', '5']
        output_folder, dataset, n_residues, validation, validation_residues, max_epochs, max_kappa, min_frame, loss_function, seed = args(argslist)
        self.assertTrue(output_folder.endswith('output_folder'))
        self.assertEqual(dataset, ['dataset'])
        self.assertEqual(n_residues, [5])

    # Test issue loss
    def test_issue_loss(self):
        argslist = ['train.py', '-o', 'output_folder', '-d', 'dataset', '-n', '5', '-l', 'a']
        with self.assertRaises(ValueError):
            args(argslist)

    # Test issue number of residues
    def test_issue_residues(self):
        argslist = ['train.py', '-o', 'output_folder', '-d', 'dataset', '-n', 'a']
        with self.assertRaises(ValueError):
            args(argslist)

    # Test issue number of kappa
    def test_issue_kappa(self):
        argslist = ['train.py', '-o', 'output_folder', '-d', 'dataset', '-n', '5', '-k', 'a']
        with self.assertRaises(ValueError):
            args(argslist)

    # Test issue number of frames
    def test_issue_frame(self):
        argslist = ['train.py', '-o', 'output_folder', '-d', 'dataset', '-n', '5', '-f', 'a']
        with self.assertRaises(ValueError):
            args(argslist)

    # Test issue seed
    def test_issue_seed(self):
        argslist = ['train.py', '-o', 'output_folder', '-d', 'dataset', '-n', '5', '-s', 'a']
        with self.assertRaises(ValueError):
            args(argslist)

    # Test issue epochs
    def test_issue_epochs(self):
        argslist = ['train.py', '-o', 'output_folder', '-d', 'dataset', '-n', '5', '-e', 'a']
        with self.assertRaises(ValueError):
            args(argslist)

    # Test issue validation residues
    def test_issue_residues_validation(self):
        argslist = ['train.py', '-o', 'output_folder', '-d', 'dataset', '-n', '5', '-vn', 'a']
        with self.assertRaises(ValueError):
            args(argslist)

    # Test train mse
    def test_train_complete_mse(self):
        argslist = ['train.py', '-o', self.output_path, '-d', f"{self.input_path}/train_sample1.csv,{self.input_path}/train_sample2.csv", '-n', '268,268', '-k', '5', '-f', '2000', '-v', f"{self.input_path}/validation_sample.csv", '-vn', '298', '-e', '1', '-l', 'mse', '-s', '101']
        output_folder, dataset, n_residues, validation, validation_residues, max_epochs, max_kappa, min_frame, loss_function, seed = args(argslist)
        self.assertTrue(output_folder.endswith(self.output_path))
        self.assertEqual(dataset, [f"{self.input_path}/train_sample1.csv", f"{self.input_path}/train_sample2.csv"])
        self.assertEqual(n_residues, [268, 268])
        self.assertEqual(max_kappa, 5)
        self.assertEqual(min_frame, 2000)
        self.assertEqual(validation, f"{self.input_path}/validation_sample.csv")
        self.assertEqual(validation_residues, 298)
        self.assertEqual(max_epochs, 1)
        self.assertEqual(loss_function, 'mse')
        self.assertEqual(seed, 101)

        train(output_folder, dataset, n_residues, validation, validation_residues, max_epochs, max_kappa, min_frame, loss_function, seed)
        self.assertTrue(os.path.exists(f"{output_folder}/model"))
        self.assertTrue(os.path.exists(f"{output_folder}/model_1e"))
        self.assertTrue(os.path.exists(f"{output_folder}/mean.json"))
        self.assertTrue(os.path.exists(f"{output_folder}/sigma.json"))

    # Test train huber
    def test_train_complete_huber(self):
        argslist = ['train.py', '-o', self.output_path, '-d', f"{self.input_path}/train_sample1.csv", '-n', '268', '-k', '5', '-f', '2000', '-v', f"{self.input_path}/validation_sample.csv", '-vn', '298', '-e', '1', '-l', 'huber', '-s', '101']
        output_folder, dataset, n_residues, validation, validation_residues, max_epochs, max_kappa, min_frame, loss_function, seed = args(argslist)
        self.assertTrue(output_folder.endswith(self.output_path))
        self.assertEqual(dataset, [f"{self.input_path}/train_sample1.csv"])
        self.assertEqual(n_residues, [268])
        self.assertEqual(max_kappa, 5)
        self.assertEqual(min_frame, 2000)
        self.assertEqual(validation, f"{self.input_path}/validation_sample.csv")
        self.assertEqual(validation_residues, 298)
        self.assertEqual(max_epochs, 1)
        self.assertEqual(loss_function, 'huber')
        self.assertEqual(seed, 101)

        train(output_folder, dataset, n_residues, validation, validation_residues, max_epochs, max_kappa, min_frame, loss_function, seed)
        self.assertTrue(os.path.exists(f"{output_folder}/model"))
        self.assertTrue(os.path.exists(f"{output_folder}/model_1e"))
        self.assertTrue(os.path.exists(f"{output_folder}/mean.json"))
        self.assertTrue(os.path.exists(f"{output_folder}/sigma.json"))

    # Test train huber
    def test_train_no_validation(self):
        argslist = ['train.py', '-o', self.output_path, '-d', f"{self.input_path}/train_sample1.csv", '-n', '268', '-k', '5', '-f', '2000', '-e', '10', '-l', 'huber', '-s', '101']
        output_folder, dataset, n_residues, validation, validation_residues, max_epochs, max_kappa, min_frame, loss_function, seed = args(argslist)
        self.assertTrue(output_folder.endswith(self.output_path))
        self.assertEqual(dataset, [f"{self.input_path}/train_sample1.csv"])
        self.assertEqual(n_residues, [268])
        self.assertEqual(max_kappa, 5)
        self.assertEqual(min_frame, 2000)
        self.assertEqual(max_epochs, 10)
        self.assertEqual(loss_function, 'huber')
        self.assertEqual(seed, 101)

        train(output_folder, dataset, n_residues, validation, validation_residues, max_epochs, max_kappa, min_frame, loss_function, seed)
        self.assertTrue(os.path.exists(f"{output_folder}/model"))
        self.assertTrue(os.path.exists(f"{output_folder}/model_10e"))
        self.assertTrue(os.path.exists(f"{output_folder}/mean.json"))
        self.assertTrue(os.path.exists(f"{output_folder}/sigma.json"))
        
        
if __name__ == '__main__':
    unittest.main()