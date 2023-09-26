import unittest
from unittest import mock
import os
import pandas as pd
from sklearn.decomposition import PCA
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.uml import create_pca_dataset

class TestCreatePcaDataset(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'etot': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
                                'local': [4, 5, 6, 4, 5, 6, 4, 5, 6, 4, 5, 6],
                                'go': [7, 8, 9, 7, 8, 9, 7, 8, 9, 7, 8, 9], 
                                'repul': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                                'stack': [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
                                'hbond': [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], 
                                'elect': [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                                'afmcc': [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33],
                                'afmfit': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36], 
                                'kapa': [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
                                'stage': [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]})
        self.output_dir = '.data_test'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def tearDown(self):
        os.system(f"rm -rf {self.output_dir}")

    @mock.patch('hornet.uml.input', create=True)
    def test_create_pca_dataset(self, mocked_input):
        n_components_mock = '8'
        mocked_input.side_effect = [n_components_mock]
        with mock.patch("hornet.uml.plt.show") as show_patch:
            pca_ana, pca_std, pca, scores_pca, PCA_variance, n_components = create_pca_dataset(self.df, self.output_dir)
            self.assertTrue(show_patch.called)
        n_components_mock = int(n_components_mock)

        # Testing if the returned dataframes have the correct shape
        self.assertEqual(pca_ana.shape, (12, 11))
        self.assertEqual(pca_std.shape, (12, 11))
        self.assertEqual(scores_pca.shape, (12, n_components_mock))
        self.assertEqual(PCA_variance.shape, (n_components_mock, 1))

        # Testing if the returned PCA model is of the correct type
        self.assertIsInstance(pca, PCA)

        # Testing if the returned number of components is correct
        self.assertEqual(n_components, n_components_mock)

    @mock.patch('hornet.uml.input', create=True)
    def test_create_pca_dataset_deafault(self, mocked_input):
        n_components_mock = ' '
        mocked_input.side_effect = [n_components_mock]
        with mock.patch("hornet.uml.plt.show") as show_patch:
            pca_ana, pca_std, pca, scores_pca, PCA_variance, n_components = create_pca_dataset(self.df, self.output_dir)
            self.assertTrue(show_patch.called)
        n_components_mock = 8 # Goes back to default

        # Testing if the returned dataframes have the correct shape
        self.assertEqual(pca_ana.shape, (12, 11))
        self.assertEqual(pca_std.shape, (12, 11))
        self.assertEqual(scores_pca.shape, (12, n_components_mock))
        self.assertEqual(PCA_variance.shape, (n_components_mock, 1))

        # Testing if the returned PCA model is of the correct type
        self.assertIsInstance(pca, PCA)

        # Testing if the returned number of components is correct
        self.assertEqual(n_components, n_components_mock)

    @mock.patch('hornet.uml.input', create=True)
    def test_create_pca_dataset_custom(self, mocked_input):
        n_components_mock = '3'
        mocked_input.side_effect = [n_components_mock]
        with mock.patch("hornet.uml.plt.show") as show_patch:
            pca_ana, pca_std, pca, scores_pca, PCA_variance, n_components = create_pca_dataset(self.df, self.output_dir)
            self.assertTrue(show_patch.called)
        n_components_mock = int(n_components_mock)

        # Testing if the returned dataframes have the correct shape
        self.assertEqual(pca_ana.shape, (12, 11))
        self.assertEqual(pca_std.shape, (12, 11))
        self.assertEqual(scores_pca.shape, (12, n_components_mock))
        self.assertEqual(PCA_variance.shape, (n_components_mock, 1))

        # Testing if the returned PCA model is of the correct type
        self.assertIsInstance(pca, PCA)

        # Testing if the returned number of components is correct
        self.assertEqual(n_components, n_components_mock)


    @mock.patch('hornet.uml.input', create=True)
    def test_create_pca_dataset_issue(self, mocked_input):
        n_components_mock = '-1'
        mocked_input.side_effect = [n_components_mock]
        with mock.patch("hornet.uml.plt.show") as show_patch:
            pca_ana, pca_std, pca, scores_pca, PCA_variance, n_components = create_pca_dataset(self.df, self.output_dir)
            self.assertTrue(show_patch.called)
        n_components_mock = 8 # Goes back to default

        # Testing if the returned dataframes have the correct shape
        self.assertEqual(pca_ana.shape, (12, 11))
        self.assertEqual(pca_std.shape, (12, 11))
        self.assertEqual(scores_pca.shape, (12, n_components_mock))
        self.assertEqual(PCA_variance.shape, (n_components_mock, 1))

        # Testing if the returned PCA model is of the correct type
        self.assertIsInstance(pca, PCA)

        # Testing if the returned number of components is correct
        self.assertEqual(n_components, n_components_mock)

if __name__ == '__main__':
    unittest.main()