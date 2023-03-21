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

sns.set(font_scale=1)

def get_parameter(filename):
    """
        Returns the transformed content of a file from the dynamic fitting.
        Parameters
        ----------
        filename : String
            File name to extract the features

        Returns
        ----------
        dFile : String
            The transformed content of the file
    """
    dFile=[]
    with open(filename,'r') as cmt_file:    
        for line in cmt_file:    
            if line[0] == '#':    
                line = line[4:]    
                dFile.append(line)
    return dFile

def get_input_data(path="data", base_pairing=-1, base_stacking=-1, initial="en_all"):
    """
        Returns input data joining all of the kappas from the dynamic fitting.
        Parameters
        ----------
        path : String
            Path to the files
        base_pairing : Int
            Average number of base-pairing, if passed
        base_stacking : Int
            Average number of base-stacking, if passed
        initial : String
            The prefix of the files to be used

        Returns
        ----------
        df : DataFrame
            The concatenated data from all kappas
    """
    columns = [
        'step', 'tempk', 'radg', 'etot', 'velet', ' qscore', 'rmsd_C', 'local',
        'go', 'repul', 'stack' , 'hbond', 'elect', 'afmcc', 'afmfit', 'stage']

    N = []
    for file in os.listdir(path):
        if file.startswith(initial):
            N.append(file.split(".")[0].split("k")[1])
    N.sort(key=int)

    Num = len(N)
    dfs = []
    for k in range(0,Num):
        df1 = []
        fn0 = f"{path}/en_allk{N[k]}.txt"

        # Create temporary dir
        if (not os.path.exists('.tmp')):
            os.mkdir('.tmp')
        # Remove problematic entries from dynamic fitting
        os.system(f"grep -v \'*\' {path}/en_allk{N[k]}.txt > .tmp/en_allk{N[k]}.txt")

        fn = f".tmp/en_allk{N[k]}.txt"
        df1 = get_parameter(fn)
        print(f"   + {fn0}")
        del df1[0:7]
        T = []
        for i in range(0,len(df1)-1):
            T.append(df1[i].split())
        df1 = pd.DataFrame(T,columns=columns)
        df1 = df1.astype(float)
        df1['frame'] = range(0,len(df1))
        df1['kapa'] = int(N[k])
        if base_pairing < 0 or base_stacking < 0:
            df2 = pd.read_csv(f"{path}/bases_k{N[k]}.txt")
            df2 = df2.rename(columns={"base_pair": "baseP", "base_stack": "baseS"}, errors="raise")
            df1 = df1.merge(df2,how='left',on="frame")
        if base_pairing > 0:
            df1['baseP'] = base_pairing
        if base_stacking > 0:
            df1['baseS'] = base_stacking

        assert (len(df1[df1['baseP'].isna()]) == 0 and len(df1[df1['baseS'].isna()]) == 0), "Found NaN entries in the DataFrame! Please, check your number of base-pairs/base-stacking."
        dfs.append(df1)
        
    return pd.concat(dfs)

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

def create_pca_dataset(df):
    """
        Returns the PCA analysis based on the input dataset.
        Parameters
        ----------
        df : DataFrame
            Input dataset

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
    pca_ana = df.copy()
    pca_ana.reset_index(inplace=True)
    cols = ['etot', 'local', 'go', 'repul', 'stack', 'hbond',
            'elect', 'afmcc', 'afmfit',  'kapa', 'stage']
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
    plt.savefig("PCA_Cumulative_variance.pdf", dpi=50, bbox_inches='tight')
    plt.show()
    #plt.close()

    # Fit the data using number of compenents that mach at least 70-80% of the data
    n_components = 8
    pca = PCA(n_components=n_components)
    pca.fit(pca_std)

    # Calculated resulting components scores for the elements in our data set:
    scores_pca = pca.transform(pca_std)

    PCA_variance = (pca.explained_variance_ratio_)*100
    PCA_variance = pd.DataFrame(PCA_variance,columns = ['PCA'])
    PCA_variance.to_json('PCA_variance.json')

    return pca_ana, pca_std, pca, scores_pca, PCA_variance, n_components

def create_pca_kmeans_clustering(pca_ana,scores_pca,filtered,n_components=8,N_CLUSTERS=5,seed=42):
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
    df_segm_pca_kmeans['frame'] = (filtered['frame'])

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
    print(means)

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

def save_transformed(df,path='data',name='Full_Trajectory.csv'):
    """
        Saves the transformed dataset and remove problematic entries from
        the dynamic fitting, such as ***.
        Parameters
        ----------
        df : DataFrame
            DataFrame to be saved 
        path : String
            Output directory 
        name : String
            Name of the file
    """
    # Create temporary dir
    if (not os.path.exists('.tmp')):
        os.mkdir('.tmp')

    # Save data to temporary dir
    df.to_csv(f".tmp/{name}", index=False)

    # Remove problematic entries
    os.system(f"grep -v \'*\' .tmp/{name} > .tmp/test && mv .tmp/test .tmp/{name}")

    # Save data
    full_path = f"{path}/{name}.csv" if path != '' else f"{name}.csv"
    os.system(f"mv .tmp/{name} {full_path}")