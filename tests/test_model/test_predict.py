import unittest
import os
import pandas as pd
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.model import predict

class TestPredictFunction(unittest.TestCase):

    def setUp(self):
        self.path = ".output_test_pred"
        self.input_path = ".input_test_pred"
        origin = os.path.dirname(os.path.realpath(__file__)) + "/../../models/hornet"
        self.model_path = f"{self.input_path}/hornet"

        # Create temporary dir
        if not os.path.exists(self.input_path):
            os.makedirs(self.input_path)
        
        # Copy model
        os.system(f"cp -r {origin} {self.input_path}")

        # Delete output dir if already exists
        if os.path.exists(self.path):
            os.system(f"rm -r {self.path}")

        # Create mock files
        original = os.path.dirname(os.path.realpath(__file__)) + "/../test_data"
        files = ["train_sample1.csv", "train_sample2.csv", "validation_sample.csv"]
        for file in files:
            os.system(f"cp {original}/{file} {self.input_path}")
        
        assert(len(os.listdir(self.input_path)) in [3, 4])

    def tearDown(self):
        os.system(f"rm -r {self.path}")
        os.system(f"rm -r {self.input_path}")

    def test_non_existent_dataset(self):
        with self.assertRaises(FileNotFoundError):
            predict(output_folder=self.path)

    def test_non_existent_model(self):
        with self.assertRaises(FileNotFoundError):
            predict(output_folder=self.path, model_location='nonexistent_folder')

    def test_data_prediction(self):
        dataset = f"{self.input_path}/train_sample1.csv"
        n_residues = 268
        max_kappa = 4
        predict(output_folder=self.path, model_location=self.model_path, dataset=dataset, n_residues=n_residues, max_kappa=max_kappa)
        self.assertTrue(os.path.exists(f"{self.path}/train_sample1_prediction.csv"))
        self.assertTrue(os.path.exists(f"{self.path}/train_sample1_Top10.csv"))

    def test_data_prediction2(self):
        dataset = f"{self.input_path}/train_sample2.csv"
        n_residues = 268
        max_kappa = 4
        predict(output_folder=self.path, model_location=self.model_path, dataset=dataset, n_residues=n_residues, max_kappa=max_kappa)
        self.assertTrue(os.path.exists(f"{self.path}/train_sample2_prediction.csv"))
        self.assertTrue(os.path.exists(f"{self.path}/train_sample2_Top10.csv"))

    def test_filtered_data(self):
        dataset = f"{self.input_path}/train_sample1.csv"
        n_residues = 268
        max_kappa = 0
        with self.assertRaises(ValueError):
            predict(output_folder=self.path, model_location=self.model_path, dataset=dataset, n_residues=n_residues, max_kappa=max_kappa)


if __name__ == '__main__':
    unittest.main()