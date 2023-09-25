import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.model import retrieve_mean_and_sigma

class TestRetrieveMeanAndSigma(unittest.TestCase):

    def setUp(self):
        self.path = ".model_test_rms"
        self.empty_path = ".model_test_empty_rms"

        # Create temporary dir
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if not os.path.exists(self.empty_path):
            os.makedirs(self.empty_path)
        
        # Create mock files
        with open(f"{self.path}/mean.json", "w") as f:
            f.write('{"feat1": 1.5, "feat2": 0.7}')
        with open(f"{self.path}/sigma.json", "w") as f:
            f.write('{"feat1": 1, "feat2": 2}')

    def tearDown(self):
        os.system(f"rm -rf {self.path}")
        os.system(f"rm -rf {self.empty_path}")

    def test_retrieve_mean_and_sigma(self):
        mean, sigma = retrieve_mean_and_sigma(self.path)

        self.assertEqual(mean, {"feat1": 1.5, "feat2": 0.7})
        self.assertEqual(sigma, {"feat1": 1, "feat2": 2})

    def test_retrieve_mean_and_sigma_empty(self):
        with self.assertRaises(FileNotFoundError):
            retrieve_mean_and_sigma(self.empty_path)

if __name__ == '__main__':
    unittest.main()