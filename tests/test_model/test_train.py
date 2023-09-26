import unittest
import os
import pandas as pd
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.model import train

class TestTrainFunction(unittest.TestCase):

    def setUp(self):
        self.path = ".output_test_train"
        self.input_path = ".input_test_train"

        # Create temporary dir
        if not os.path.exists(self.input_path):
            os.makedirs(self.input_path)

        # Delete output dir if already exists
        if os.path.exists(self.path):
            os.system(f"rm -r {self.path}")

        # Create mock files
        original = os.path.dirname(os.path.realpath(__file__)) + "/../test_data"
        files = ["train_sample1.csv", "train_sample2.csv", "validation_sample.csv"]
        for file in files:
            os.system(f"cp {original}/{file} {self.input_path}")
        
        assert(len(os.listdir(self.input_path)) in [3,4])

    def tearDown(self):
        os.system(f"rm -r {self.path}")
        os.system(f"rm -r {self.input_path}")

    def test_output_folder_creation(self):
        with self.assertRaises(ValueError):
            train(self.path)
        self.assertTrue(os.path.exists(self.path))

    def test_no_training_data(self):
        dataset = [f"nonexisting.csv"]
        n_residues = [268]
        epochs = 1
        with self.assertRaises(FileNotFoundError):
            train(output_folder=self.path, dataset=dataset, n_residues=n_residues, max_epochs=epochs)
    
    def test_no_validation_data(self):
        dataset = [f"{self.input_path}/train_sample1.csv"]
        validation = f"nonexisting.csv"
        n_residues = [268]
        n_residues_validation = 268
        epochs = 1
        with self.assertRaises(FileNotFoundError):
            train(output_folder=self.path, dataset=dataset, n_residues=n_residues, max_epochs=epochs, validation=validation, validation_residues=n_residues_validation)

    def test_invalid_epochs(self):
        dataset = [f"{self.input_path}/train_sample1.csv"]
        n_residues = [268]
        min_frame = 2000
        max_kappa = 50
        epochs = -1
        with self.assertRaises(ValueError):
            train(output_folder=self.path, dataset=dataset, n_residues=n_residues, min_frame=min_frame, max_kappa=max_kappa, max_epochs=epochs)

    def test_invalid_epochs_string(self):
        dataset = [f"{self.input_path}/train_sample1.csv"]
        n_residues = [268]
        min_frame = 2000
        max_kappa = 50
        epochs = "a"
        with self.assertRaises(TypeError):
            train(output_folder=self.path, dataset=dataset, n_residues=n_residues, min_frame=min_frame, max_kappa=max_kappa, max_epochs=epochs)

    def test_invalid_frame_cut(self):
        dataset = [f"{self.input_path}/train_sample1.csv"]
        n_residues = [268]
        min_frame = "a"
        max_kappa = 50
        with self.assertRaises(TypeError):
            train(output_folder=self.path, dataset=dataset, n_residues=n_residues, min_frame=min_frame, max_kappa=max_kappa)

    def test_invalid_kappa_cut(self):
        dataset = [f"{self.input_path}/train_sample1.csv"]
        n_residues = [268]
        min_frame = 2000
        max_kappa = "a"
        with self.assertRaises(TypeError):
            train(output_folder=self.path, dataset=dataset, n_residues=n_residues, min_frame=min_frame, max_kappa=max_kappa)

    def test_invalid_folder(self):
        dataset = [f"{self.input_path}/train_sample1.csv"]
        n_residues = [268]
        folder = "existing_folder"
        os.makedirs(folder)
        with self.assertRaises(AssertionError):
            train(output_folder=folder, dataset=dataset, n_residues=n_residues)
        os.system(f"rm -r {folder}")

    def test_no_residues(self):
        dataset = [f"{self.input_path}/train_sample1.csv"]
        n_residues = []
        with self.assertRaises(ValueError):
            train(output_folder=self.path, dataset=dataset, n_residues=n_residues)

    def test_no_data(self):
        dataset = []
        n_residues = [268]
        with self.assertRaises(ValueError):
            train(output_folder=self.path, dataset=dataset, n_residues=n_residues)

    def test_wrong_number_residues_and_data(self):
        dataset = [f"{self.input_path}/train_sample1.csv"]
        n_residues = [268, 268]
        with self.assertRaises(ValueError):
            train(output_folder=self.path, dataset=dataset, n_residues=n_residues)

    def test_wrong_data_type(self):
        dataset = f"{self.input_path}/train_sample1.csv"
        n_residues = [268]
        with self.assertRaises(TypeError):
            train(output_folder=self.path, dataset=dataset, n_residues=n_residues)

    def test_wrong_residue_type(self):
        dataset = [f"{self.input_path}/train_sample1.csv"]
        n_residues = 268
        with self.assertRaises(TypeError):
            train(output_folder=self.path, dataset=dataset, n_residues=n_residues)
    
    def test_one_training_data_huber(self):
        dataset = [f"{self.input_path}/train_sample1.csv"]
        n_residues = [268]
        min_frame = 2000
        max_kappa = 50
        epochs = 1
        loss_function = 'huber'
        train(output_folder=self.path, dataset=dataset, n_residues=n_residues, min_frame=min_frame, max_kappa=max_kappa, max_epochs=epochs, loss_function=loss_function)
        self.assertTrue(os.path.exists(f"{self.path}/model"))
        self.assertTrue(os.path.exists(f"{self.path}/model_1e"))
    
    def test_one_training_data_mse(self):
        dataset = [f"{self.input_path}/train_sample1.csv"]
        n_residues = [268]
        min_frame = 2000
        max_kappa = 50
        epochs = 1
        loss_function = 'mse'
        train(output_folder=self.path, dataset=dataset, n_residues=n_residues, min_frame=min_frame, max_kappa=max_kappa, max_epochs=epochs, loss_function=loss_function)
        self.assertTrue(os.path.exists(f"{self.path}/model"))
        self.assertTrue(os.path.exists(f"{self.path}/model_1e"))
    
    def test_training_and_validation_data(self):
        dataset = [f"{self.input_path}/train_sample1.csv", f"{self.input_path}/train_sample2.csv"]
        validation = f"{self.input_path}/validation_sample.csv"
        n_residues = [268, 268]
        n_residues_validation = 298
        min_frame = 2000
        max_kappa = 15
        epochs = 1
        train(output_folder=self.path, dataset=dataset, n_residues=n_residues, min_frame=min_frame, max_kappa=max_kappa, max_epochs=epochs, validation=validation, validation_residues=n_residues_validation)
        self.assertTrue(os.path.exists(f"{self.path}/model"))
        self.assertTrue(os.path.exists(f"{self.path}/model_1e"))
    
    def test_all_filtered(self):
        dataset = [f"{self.input_path}/train_sample1.csv", f"{self.input_path}/train_sample2.csv"]
        validation = f"{self.input_path}/validation_sample.csv"
        n_residues = [268, 268]
        n_residues_validation = 298
        min_frame = 50000
        max_kappa = 0
        epochs = 1
        with self.assertRaises(ValueError):
            train(output_folder=self.path, dataset=dataset, n_residues=n_residues, min_frame=min_frame, max_kappa=max_kappa, max_epochs=epochs, validation=validation, validation_residues=n_residues_validation)

    
    def test_longer_training(self):
        dataset = [f"{self.input_path}/train_sample1.csv", f"{self.input_path}/train_sample2.csv"]
        validation = f"{self.input_path}/validation_sample.csv"
        n_residues = [268, 268]
        n_residues_validation = 298
        min_frame = 3000
        max_kappa = 4
        epochs = 10
        train(output_folder=self.path, dataset=dataset, n_residues=n_residues, min_frame=min_frame, max_kappa=max_kappa, max_epochs=epochs, validation=validation, validation_residues=n_residues_validation)
        self.assertTrue(os.path.exists(f"{self.path}/model"))
        self.assertTrue(os.path.exists(f"{self.path}/model_10e"))


if __name__ == '__main__':
    unittest.main()