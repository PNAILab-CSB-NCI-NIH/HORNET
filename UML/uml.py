#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author:
        Maximilia F. S. Degenhardt <frazaodesouzam2@nih.gov>
        Hermann F. Degenhardt <degenhardthf@nih.gov>
"""

import os, sys, math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

from utils import *

def main():
    """
        Main function to use UML approach over the inputs from dynamic fitting. It
        will create the Filtered, Cluster, and Cohort of structures at the end.
        Parameters
        ----------
        input_file : string
            Full trajectory from simulation
    """
    # Get user argument
    input_file = args(sys.argv)

    # Reading data
    print(f" - Read data: {input_file}")
    full_traj = pd.read_csv(input_file)

    # Initial Cleaning and Featurization
    print(" - Clear data")
    full_traj = filter_data(full_traj)
    full_traj = create_features(full_traj)

    # ------------ STEP 1: Energy Filtering ------------
    print(" - STEP 1: Energy Filtering")
    # Energy Filtering
    filtered = energy_filter(full_traj)
    filtered.reset_index(inplace=True)

    # ------------- STEP 2: PCA+Clustering -------------
    print(" - STEP 2: PCA + Clustering")
    # PCA
    pca_ana, pca_std, pca, scores_pca, PCA_variance, n_components = create_pca_dataset(filtered)

    # KMeans Clustering
    n_clusters = 5
    df_segm_pca_kmeans, km = create_pca_kmeans_clustering(pca_ana,scores_pca,filtered,n_components=n_components,N_CLUSTERS=n_clusters)

    # Cluster Selection
    means_Etot, index_minEtot = get_min_cluster_index(df_segm_pca_kmeans,'etot')
    means_go, index_minGo = get_min_cluster_index(df_segm_pca_kmeans,'go')
    means_local, index_minLocal = get_min_cluster_index(df_segm_pca_kmeans,'local')

    if (index_minLocal == index_minGo == index_minEtot) == False:
        print("Warning: mean_etot, mean_go and min_local are not located in the same cluster.")
    cluster = df_segm_pca_kmeans[df_segm_pca_kmeans['Segment'] == index_minGo]

    # ---------------- STEP 3: Cohort ----------------
    print(" - STEP 3: Cohort")
    # Filter after PCA analysis
    cohort = cluster_filter(cluster)

    # Save datasets
    print(" - Saving datasets")
    filtered.to_csv('data/Filtered_Data.csv', index=False)
    cluster.to_csv('data/Select_Cluster.csv', index=False)
    cohort.to_csv('data/Final_Cohort.csv', index=False)

def help():
    return """
uml.py: Run the UML approach from HORNET to select top cohort of structures.
USAGE:
    python uml.py <full-trajectory-file> [-h]

Positional Arguments:
    <full-trajectory-file>      Type [String]: Input file (Full trajectory).
                                Example: 'data/Full_Trajectory.csv'
                                
Options:
    [-h, --help]                Displays usage and help information for the script.

Example:
python uml.py data/Full_Trajectory.csv

Requirements:
    python = 3.7
"""

def args(argslist):
    """Parses command-line args from "sys.argv". Returns a list of parsed arguments."""

    # Input list of arguments to parse
    print(" - Checking arguments...")
    user_args = argslist[1:]

    if '-h' in user_args or '--help' in user_args:
        print(help())
        sys.exit(0)

    input_file = 'data/Full_trajectory.csv'
    if len(user_args) > 0:
        input_file = user_args[0]

    return input_file

if __name__ == '__main__':
    main()
