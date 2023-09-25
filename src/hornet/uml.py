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
from copy import deepcopy
from numpy import diff

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

sns.set(font_scale=1)

def filter_data(df):
    """
        Returns the data filtered by fixed cuts.
        Parameters
        ----------
        df : DataFrame
            Dataset to be filtered

        Returns
        ----------
        df : DataFrame
            Filtered dataset
    """
    df = df[df['kapa']  <   50]
    df = df[df['frame'] > 2000]
    df = df[df['etot']  <    0]
    df = df[df['go']    <    0]
    return df

def create_features(df):
    """
        Create features used in the UML approach.
        Parameters
        ----------
        df : DataFrame
            Initial dataset

        Returns
        ----------
        df : DataFrame
            Featurized dataset
    """
    df['afmccpow'] = np.power(df['afmcc'],7)
    df['etotPower'] = df['afmccpow']*df['etot']
    return df

def energy_filter(df):
    """
        Returns the data filtered by energies. This is the first step of the
        UML approach.
        Parameters
        ----------
        df : DataFrame
            Initial dataset

        Returns
        ----------
        df : DataFrame
            Filtered dataset
    """
    # Step 1
    b_repul = df['repul'] < (df['repul'].mean() + 1.*(df['repul'].std()))
    b_hbond = df['hbond'] < (df['hbond'].mean() + 3.*(df['hbond'].std()))
    b_stage = df['stage'] < (df['stage'].mean() + 4.*(df['stage'].std()))
    b_stack = df['stack'] < (df['stack'].mean() + 2.*(df['stack'].std()))
    b_local = df['local'] < (df['local'].mean() + 2.*(df['local'].std()))
    df = df[b_local & b_repul & b_stack & b_stage & b_hbond]

    # Step 2
    b_afmcc = df['afmcc'] > (df['afmcc'].mean() - 2.*df['afmcc'].std())
    b_etot  = df['etot']  < (df['etot'].mean()  + 3.*df['etot'].std())
    df = df[b_afmcc & b_etot]

    return df

def create_pca_dataset(df, output_dir="."):
    """
        Returns the PCA analysis based on the input dataset.
        Parameters
        ----------
        df : DataFrame
            Input dataset
        output_dir : string
            Output directory

        Returns
        ----------
        pca_ana : DataFrame
            Transformed input dataset
        pca_std : DataFrame
            Standardized dataset
        pca : PCA
            PCA decomposition model
        scores_pca : DataFrame
            Components scores
        PCA_variance : DataFrame
            PCA variance
        n_components : int
            Number of PCA components used
    """
    pca_ana = deepcopy(df)
    pca_ana.reset_index(inplace=True)
    cols = ['etot', 'local', 'go', 'repul', 'stack', 'hbond',
            'elect', 'afmcc', 'afmfit', 'kapa', 'stage']
    pca_ana = pca_ana[cols]

    scaler = StandardScaler()
    pca_std = scaler.fit_transform(pca_ana)

    pca = PCA()
    pca.fit(pca_std)

    pca.explained_variance_ratio_
    plt.figure(figsize=(10,8))
    plt.plot(range(1,12), pca.explained_variance_ratio_.cumsum(), marker='o', linestyle='-',color='b')
    plt.xlabel('Number of Components')
    plt.ylabel('Cumulative explained variance')
    plt.savefig(f"{output_dir}/PCA_Cumulative_variance.pdf", dpi=50, bbox_inches='tight')
    plt.show()

    # Fit the data using number of compenents that mach at least 70-80% of the data
    n_components = 8
    n_components_user = input("Please, enter the number of components based on PCA plot (default = 8): ")
    if n_components_user is None or n_components_user in ['', ' ','\n']:
        print("Using default number of components.")
    else:
        try:
            n_components_user = int(n_components_user)
            if n_components_user < 0 or n_components_user > min(len(pca_ana), len(cols)):
                raise ValueError("Invalid number of components.")
            n_components = n_components_user
        except:
            print("Invalid number of components. Using default number of components.")
    print(f"Using {n_components} components.")
    pca = PCA(n_components=n_components)
    pca.fit(pca_std)

    # Calculated resulting components scores for the elements in our data set:
    scores_pca = pca.transform(pca_std)

    PCA_variance = (pca.explained_variance_ratio_)*100
    PCA_variance = pd.DataFrame(PCA_variance,columns = ['PCA'])
    PCA_variance.to_json(f"{output_dir}/PCA_variance.json")

    return pca_ana, pca_std, pca, scores_pca, PCA_variance, n_components

def create_pca_kmeans_clustering(pca_ana, scores_pca, filtered, output_dir=".", n_components=8, N_CLUSTERS=3, seed=42):
    """
        Returns the PCA analysis based on the input dataset.
        Parameters
        ----------
        pca_ana : DataFrame
            Transformed dataset from PCA
        scores_pca : DataFrame
            Components scores
        filtered : DataFrame
            Filtered dataset
        output_dir : string
            Output directory
        n_components : int
            Number of PCA components used
        N_CLUSTERS : int
            Number of KMeans clusters to use
        seed : int
            Seed for reproducibility

        Returns
        ----------
        df_segm_pca_kmeans : DataFrame
            Segmented dataset from PCA+Clustering
        km : KMeans cluster model
            KMeans cluster model
    """

    # Testing the number of cluster that describe the data
    wcss = []
    x_range = range(1,10)
    for i in x_range:
        kmeans_pca = KMeans(n_clusters=i, init='k-means++', random_state=42)
        kmeans_pca.fit(scores_pca)
        wcss.append(kmeans_pca.inertia_)

    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10,8), sharex=True)

    # Elbow-method. The approach consists of looking for a kink or elbow in the WCSS graph.
    ax1.plot(x_range, wcss, marker='o', linestyle='--')
    ax1.set_title('K-means with PCA Clustering')
    ax1.set_xlabel('Number of Clusters')
    ax1.set_ylabel('WCSS')

    Z = diff(wcss)/diff(x_range)
    ax2.plot(x_range[:-1], Z, marker='o', linestyle='--')
    ax2.set_xlabel('Number of Clusters')
    ax2.set_ylabel('WCSS derivative')
    plt.savefig(f"{output_dir}/Kmeans_PCA_clustering.pdf", dpi=50, bbox_inches='tight')
    plt.show()

    n_clusters_user = input("Please, enter the number of clusters based on the Clustering PCA plot (default = 3): ")
    if n_clusters_user is None or n_clusters_user in ['', ' ', '\n']:
        print("Using default number of clusters.")
    else:
        try:
            n_clusters_user = int(n_clusters_user)
            N_CLUSTERS = n_clusters_user
        except:
            print("Invalid number of components. Using default number of components.")
    print(f"Using {N_CLUSTERS} clusters.")

    # Create KMeans
    km = KMeans(n_clusters=N_CLUSTERS, init='k-means++', random_state=seed)
    km = km.fit(scores_pca)

    # Get cluster label of all data
    cluster_labels = km.labels_

    # Segmentation PCA
    df_segm_pca_kmeans = pd.concat([pca_ana.reset_index(drop=True),pd.DataFrame(scores_pca)],axis=1)
    df_segm_pca_kmeans.columns.values[-n_components:] = [f"Component{i}" for i in range(n_components)]
    df_segm_pca_kmeans['Segment k-means PCA'] = km.labels_

    # Clustering
    dic = {}
    for i in range(N_CLUSTERS):
        dic[i] = f"Cluster{i}"
        
    df_segm_pca_kmeans['Segment'] = df_segm_pca_kmeans['Segment k-means PCA'].map(dic)

    feat_dnn = ['etot', 'local', 'go', 'repul', 'stack', 'hbond', 'elect', 'afmfit', 'afmcc']
    cols_to_copy_original = [f for f in feat_dnn]
    cols_to_include = ["frame", "baseP", "baseS"]
    total_colums = cols_to_copy_original + cols_to_include
    for c in total_colums:
        df_segm_pca_kmeans[c] = filtered[c]

    return df_segm_pca_kmeans, km

def get_min_cluster_index(df,col):
    """
        Returns the mean of a given feature for all of the clusters and
        the index with the minimum mean.
        Parameters
        ----------
        df : DataFrame
            DataFrame to extract cluster means and indexes
        col : String
            Column that the mean will be evaluated

        Returns
        ----------
        means : DataFrame
            The mean for all of the clusters
        index : String
            Index of the cluster with minimum mean
    """
    if col not in df.columns:
        raise ValueError(f"Column {col} not in DataFrame.")

    # Extract the means
    means = {}
    for i in df['Segment'].unique():
        means[i] = df[df['Segment']==i][col].mean()
    means_i = [df[df['Segment']==i][col].mean() for i in df['Segment'].unique()]
    minimum = min(means_i)

    # Find the cluster index with minimum mean
    index = ""
    for i in means:
        if(means[i] == minimum):
            index = i
    #print(means)

    return means, index

def cluster_filter(df):
    """
        Select the cohort structures based on energy and cc filters.
        Parameters
        ----------
        df : DataFrame
            DataFrame to be filtered from clustering

        Returns
        ----------
        df : DataFrame
            Cohort of structures based of the filtering
    """
    # Step 1
    cohort  = df.copy()
    b_go    = cohort['go']    < (cohort['go'].mean())
    b_elect = cohort['elect'] > (cohort['elect'].mean() + 1.5*(cohort['elect'].std()))
    b_local = cohort['local'] < (cohort['local'].mean() + 3.0*(cohort['local'].std()))
    cohort  = cohort[b_go & b_elect & b_local]

    # Step 2
    b_etot   = cohort['etot']   < (cohort['etot'].mean() - 1.0*(cohort['etot'].std()))
    b_afmCC  = cohort['afmcc']  > (cohort['afmcc'].mean())
    b_afmfit = cohort['afmfit'] < (cohort['afmfit'].mean() + 2.0*(cohort['afmfit'].std()))
    cohort   = cohort[b_etot & b_afmCC & b_afmfit]

    return cohort


def uml_analysis(input_file):
    """
        Main function to use UML approach over the inputs from dynamic fitting. It
        will create the Filtered, Cluster, and Cohort of structures at the end.
        Parameters
        ----------
        input_file : string
            Full trajectory from simulation
    """

    # Reading data
    print(f" - Read data: {input_file}")
    full_traj = pd.read_csv(input_file)
    output_dir = input_file[0:-len(input_file.split("/")[-1])]
    if output_dir == "":
        output_dir = os.getcwd()
    print(f"Full Trajectory initial size: {len(full_traj)}")

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
    pca_ana, pca_std, pca, scores_pca, PCA_variance, n_components = create_pca_dataset(filtered, output_dir)

    # KMeans Clustering
    n_clusters = 3
    df_segm_pca_kmeans, km = create_pca_kmeans_clustering(pca_ana, scores_pca, filtered, output_dir, n_components=n_components, N_CLUSTERS=n_clusters)

    # Cluster Selection
    means_Etot, index_minEtot = get_min_cluster_index(df_segm_pca_kmeans, 'etot')
    means_go, index_minGo = get_min_cluster_index(df_segm_pca_kmeans, 'go')
    means_local, index_minLocal = get_min_cluster_index(df_segm_pca_kmeans, 'local')

    if (index_minLocal == index_minGo == index_minEtot) == False:
        print("Warning: mean_etot, mean_go and min_local are not located in the same cluster.")
    cluster = df_segm_pca_kmeans[df_segm_pca_kmeans['Segment'] == index_minGo]

    # ---------------- STEP 3: Cohort ----------------
    print(" - STEP 3: Cohort")
    # Filter after PCA analysis
    cohort = cluster_filter(cluster)

    # Save datasets
    print(" - Saving datasets")
    print(f"Filtered size: {len(filtered)}")
    filtered.to_csv(f"{output_dir}/Filtered_Data.csv",  index=False)
    print(f"Cluster size: {len(cluster)}")
    cluster.to_csv( f"{output_dir}/Select_Cluster.csv", index=False)
    print(f"Cohort size: {len(cohort)}")
    cohort.to_csv(  f"{output_dir}/Final_Cohort.csv",   index=False)