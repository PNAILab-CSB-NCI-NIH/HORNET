import unittest
from unittest import mock
import os
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.uml import create_pca_kmeans_clustering

class TestCreatePcaKmeansClustering(unittest.TestCase):
    def setUp(self):
        import warnings
        warnings.filterwarnings(action='ignore', category=FutureWarning)
        
        self.df = pd.DataFrame(
            {'frame': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
             'baseP': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
             'baseS': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
             'etot': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
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
        
        self.data = np.array(
            [[-4.85745218e+00, -1.10129500e+00, -1.27885314e-15,
                -1.75718426e-15,  1.13572600e-16, -2.10335816e-16,
                -9.75856746e-17, -1.97615033e-16],
            [-3.60058247e+00,  7.93858612e-01, -5.48108452e-16,
                -1.47571507e-15,  3.32456064e-16, -4.90459809e-17,
                -2.32597922e-16, -1.97543075e-16],
            [-2.34371276e+00,  2.68901222e+00,  1.82636239e-16,
                -1.19424587e-15,  5.17391663e-17, -5.42895994e-17,
                -1.73321141e-16, -5.86932385e-17],
            [-2.45706386e+00, -1.63053407e+00, -9.13447508e-16,
                -7.73374214e-16, -3.46887017e-17, -8.72887936e-17,
                -1.14044359e-16, -5.86212804e-17],
            [-1.20019416e+00,  2.64619537e-01, -1.82702817e-16,
                -4.91905022e-16,  3.94361814e-17,  2.17432157e-17,
                -3.34040210e-17, -1.07937060e-19],
            [ 5.66755531e-02,  2.15977315e+00,  5.48041874e-16,
                -2.10435830e-16,  1.22284593e-17, -2.08509880e-17,
                -3.47058424e-17, -1.31812083e-17],
            [-5.66755531e-02, -2.15977315e+00, -5.48041874e-16,
                2.10435830e-16, -2.16786088e-17, -1.81815246e-19,
                4.21916115e-17,  1.61114424e-17],
            [ 1.20019416e+00, -2.64619537e-01,  1.82702817e-16,
                4.91905022e-16, -5.23557778e-17,  2.31434732e-17,
                5.47675779e-17,  3.07937468e-17],
            [ 2.45706386e+00,  1.63053407e+00,  9.13447508e-16,
                7.73374214e-16,  3.46887017e-17,  8.72887936e-17,
                1.14044359e-16,  5.86212804e-17],
            [ 2.34371276e+00, -2.68901222e+00, -1.82636239e-16,
                1.19424587e-15, -5.17391663e-17,  5.42895994e-17,
                1.73321141e-16,  5.86932385e-17],
            [ 3.60058247e+00, -7.93858612e-01,  5.48108452e-16,
                1.47571507e-15, -3.32456064e-16,  4.90459809e-17,
                2.32597922e-16,  1.97543075e-16],
            [ 4.85745218e+00,  1.10129500e+00,  1.27885314e-15,
                1.75718426e-15, -1.13572600e-16,  2.10335816e-16,
                9.75856746e-17,  1.97615033e-16]])
        
        self.output_dir = '.data_test'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def tearDown(self):
        os.system(f"rm -r {self.output_dir}")

    @mock.patch('hornet.uml.input', create=True)
    def test_create_pca_kmeans_clustering(self, mocked_input):
        n_clusters_mock = '3'
        mocked_input.side_effect = [n_clusters_mock]
        with mock.patch("hornet.uml.plt.show") as show_patch:
            df_result, km = create_pca_kmeans_clustering(self.df, self.data, self.df, self.output_dir)
            self.assertTrue(show_patch.called)
        n_clusters_mock = int(n_clusters_mock)
        
        # Testing if the returned dataframes have the correct shape
        self.assertEqual(df_result.shape, (12, len(self.df.columns)+8+2))
        self.assertTrue(km.n_clusters, n_clusters_mock)

        # Testing if the returned PCA model is of the correct type
        self.assertIsInstance(km, KMeans)
        
        unique_clusters = df_result['Segment k-means PCA'].unique()
        cluster_position = df_result['Segment k-means PCA'].to_list()
        expected_position = [2, 2, 0, 2, 0, 0, 1, 1, 1, 1, 1, 1]
        
        # Testing if the returned data is as expected
        self.assertTrue(len(unique_clusters) == n_clusters_mock)
        #self.assertEqual(cluster_position, expected_position)

    @mock.patch('hornet.uml.input', create=True)
    def test_create_pca_kmeans_clustering_custom(self, mocked_input):
        n_clusters_mock = '5'
        mocked_input.side_effect = [n_clusters_mock]
        with mock.patch("hornet.uml.plt.show") as show_patch:
            df_result, km = create_pca_kmeans_clustering(self.df, self.data, self.df, self.output_dir)
            self.assertTrue(show_patch.called)
        n_clusters_mock = int(n_clusters_mock)
        
        # Testing if the returned dataframes have the correct shape
        self.assertEqual(df_result.shape, (12, len(self.df.columns)+8+2))
        self.assertEqual(km.n_clusters, n_clusters_mock)

        # Testing if the returned PCA model is of the correct type
        self.assertIsInstance(km, KMeans)
        
        unique_clusters = df_result['Segment k-means PCA'].unique()
        cluster_position = df_result['Segment k-means PCA'].to_list()
        expected_position = [2, 2, 1, 2, 1, 1, 3, 4, 4, 3, 0, 0]
        
        # Testing if the returned data is as expected
        self.assertTrue(len(unique_clusters) == n_clusters_mock)
        #self.assertEqual(cluster_position, expected_position)

    @mock.patch('hornet.uml.input', create=True)
    def test_create_pca_kmeans_clustering_issue(self, mocked_input):
        n_clusters_mock = ' '
        mocked_input.side_effect = [n_clusters_mock]
        with mock.patch("hornet.uml.plt.show") as show_patch:
            df_result, km = create_pca_kmeans_clustering(self.df, self.data, self.df, self.output_dir)
            self.assertTrue(show_patch.called)
        n_clusters_mock = 3 # Goes to default
        
        # Testing if the returned dataframes have the correct shape
        self.assertEqual(df_result.shape, (12, len(self.df.columns)+8+2))
        self.assertEqual(km.n_clusters, n_clusters_mock)

        # Testing if the returned PCA model is of the correct type
        self.assertIsInstance(km, KMeans)
        
        unique_clusters = df_result['Segment k-means PCA'].unique()
        cluster_position = df_result['Segment k-means PCA'].to_list()
        expected_position = [2, 2, 0, 2, 0, 0, 1, 1, 1, 1, 1, 1]
        
        # Testing if the returned data is as expected
        self.assertTrue(len(unique_clusters) == n_clusters_mock)
        #self.assertEqual(cluster_position, expected_position)

if __name__ == '__main__':
    unittest.main()