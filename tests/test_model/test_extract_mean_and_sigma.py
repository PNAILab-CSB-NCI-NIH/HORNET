import pandas as pd
import json
import os
import unittest
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.model import extract_mean_and_sigma
import hornet.model as hm

class TestExtractMeanAndSigma(unittest.TestCase):

    def setUp(self):
        self.path = ".data_test_ms"

        # Create temporary dir
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def tearDown(self):
        os.system(f"rm -r {self.path}")

    def test_extract_mean_and_sigma(self):
        # Create test DataFrame
        real_feat = hm.feat.copy()
        hm.feat = ['feat1', 'feat2']
        data = {'feat1': [1, 2, 3, 4, 5],
                'feat2': [2, 4, 6, 8, 10]}
        df = pd.DataFrame(data)

        # Call the function
        mean, sigma = extract_mean_and_sigma(df, self.path)
        hm.feat = real_feat
        
        # Check if mean and sigma are dictionaries
        self.assertIsInstance(mean, dict)
        self.assertIsInstance(sigma, dict)

        # Check if mean and sigma dictionaries have the same keys as the DataFrame columns
        self.assertEqual(set(mean.keys()), set(df.columns))
        self.assertEqual(set(sigma.keys()), set(df.columns))

        # Check if mean and sigma values are correct
        self.assertAlmostEqual(mean['feat1'], 3)
        self.assertAlmostEqual(mean['feat2'], 6)
        self.assertAlmostEqual(sigma['feat1'], 1.5811388300841898)
        self.assertAlmostEqual(sigma['feat2'], 3.1622776601683795)

        # Check if mean and sigma files are saved
        self.assertTrue(os.path.exists(f"{self.path}/mean.json"))
        self.assertTrue(os.path.exists(f"{self.path}/sigma.json"))

if __name__ == '__main__':
    unittest.main()