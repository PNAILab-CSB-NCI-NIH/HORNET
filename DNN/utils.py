#!/usr/bin/env python
# coding: utf-8
"""
Author:
        Hermann F. Degenhardt <degenhardthf@nih.gov>
        Maximilia F. S. Degenhardt <frazaodesouzam2@nih.gov>
"""

import numpy as np
import pandas as pd
import random, math, os, sys, json

from sklearn.model_selection import train_test_split
from sklearn import metrics
import tensorflow as tf
from tensorflow.keras.layers import Dense,Dropout,AlphaDropout
from tensorflow.keras.optimizers import Adam
from keras.regularizers import l2

feat = [
    'etot', 'local', 'go', 'repul', 'stack', 'hbond', 'elect',
    'afmfit', 'afmcc',
    'cc7xEtot'
]
target = 'rmsd'
all_feat = feat.copy()
all_feat.append(target)

etot_sum = ['local', 'go', 'repul', 'elect', 'stack', 'hbond']
norm_by_size = ['local', 'go', 'repul', 'elect']
norm_by_kappa = ['afmfit']
norm_by_base_pairs = ['hbond']
norm_by_base_stacking = ['stack']

BP = 'baseP'
BS = 'baseS'
RG = 'radg'
KP = 'kapa'
LOSS = 'mse'

mse_loss = tf.keras.losses.MeanSquaredError()
huber_loss = tf.keras.losses.Huber()

def read_data(dataset,n_residues,min_frame,max_kappa):
    """
        Returns a DataFrame containing all of the dataset included in training.
        Parameters
        ----------
        dataset : Array(string)
            An array of strings containing the data locations
        n_residues : Array(int)
            An array of integers containing the number of residues from each dataset 
        min_frame: int
            Minimum frame cut 
        max_kappa: int
            Maximum accepted kappa 
  
        Returns
        ----------
        df : DataFrame
            Concatenated DataFrame
    """
    dfs = []
    for i in range(len(dataset)):
        print(f"   + {dataset[i]}")
        df_i = pd.read_csv(dataset[i])
        df_i = clean_data(df_i,min_frame,max_kappa)
        df_i = normalize(df_i,n_residues[i])
        df_i = featurize(df_i)
        dfs.append(df_i)
    df = pd.concat(dfs)
    df = df.reset_index(drop=True)
    return df

def clean_data(df,frame_cut,kappa_cut):
    """
        Returns a filtered DataFrame. This step is necessary to perform the first
        cleaning of the data from the simulations.
        Parameters
        ----------
        df : DataFrame
            The DataFrame containing the data to be normalized
        frame_cut : int
            The number of initial frames that should be disconsidered from the simulation
        kappa_cut : int
            The maximum kappa value accepted 
  
        Returns
        ----------
        df : DataFrame
            Filtered DataFrame
    """
    print(f"     Initial len: {len(df)}")
    print(f"     Frame cut: {frame_cut}")
    print(f"     Kappa cut: {kappa_cut}")
    df = df[df['frame'] > frame_cut]
    df = df[df['kapa'] < kappa_cut]
    df = df[df['etot'] < 0]
    df = df[df['go'] < 0]
    print(f"     Final len: {len(df)}")
    return df

def normalize(df,n_residues):
    """
        Returns a normalized DataFrame. This step is necessary since each RNA
        will yield different values of energies depending on its size and other
        characteristics.
        Parameters
        ----------
        df : DataFrame
            The DataFrame containing the data to be normalized
        n_residues : int
            The number of residues of the RNA that this data is associated with 
  
        Returns
        ----------
        df : DataFrame
            Normalized DataFrame
    """

    # Normalize energies by their dependencies
    n_beads = n_residues*3
    for j in norm_by_size:
        df[j] = df[j]/n_beads
    for j in norm_by_kappa:
        df[j] = df[j]/(n_beads*df[KP])
    for j in norm_by_base_pairs:
        df[j] = df[j]/df[BP]
    for j in norm_by_base_stacking:
        df[j] = df[j]/df[BS]

    return df

def featurize(df,cc_power=7):
    """
        Returns a featurized DataFrame.
        Parameters
        ----------
        df : DataFrame
            The DataFrame containing the data to be normalized
        cc_power : int
            AFM cc Power 
  
        Returns
        ----------
        df : DataFrame
            Featurized DataFrame
    """
    df['etot'] = 0.
    for energy in etot_sum:
        df['etot'] = df['etot'] + df[energy]
    df['cc7xEtot'] = (df['afmcc']**cc_power)*df['etot']

    return df

def extract_mean_and_sigma(df,output_folder):
    """
        Returns the mean and sigma values of the features distribution
        Parameters
        ----------
        df : DataFrame
            The DataFrame containing the data
        output_folder : string
            The location where the mean and sigma will be saved
  
        Returns
        ----------
        mean : dictionary
            A dictionary containing the mean values for the distributions
        sigma : dictionary
            A dictionary containing the sigma values for the distributions
    """
    # Extract parameters
    mean, sigma = {},{}
    for i in feat:
        mean[i] = df[i].mean()
        sigma[i] = df[i].std()
    
    # Save parameters
    fmean  = open(f"{output_folder}/mean.json",'w')
    fsigma = open(f"{output_folder}/sigma.json",'w')
    json.dump(mean, fmean)
    json.dump(sigma, fsigma)

    # Clear
    fmean.close()
    fsigma.close()

    return mean, sigma

def retrieve_mean_and_sigma(model_location):
    """
        Returns the mean and sigma values of the features distribution based
        on the training dataset.
        Parameters
        ----------
        model_location : string
            Folder built using train.py function, containing the dictionaries
            of mean and sigma and the trained model.
  
        Returns
        ----------
        mean : dictionary
            The dictionary containing the mean values for the distributions
        sigma : dictionary
            A dictionary containing the sigma values for the distributions
    """
    # Get files
    fmean  = open(f"{model_location}/mean.json",'r')
    fsigma = open(f"{model_location}/sigma.json",'r')

    # Get dictionaries
    mean_text = fmean.read()
    sigma_text = fsigma.read()
    mean = json.loads(mean_text)
    sigma = json.loads(sigma_text)

    # Clean
    fmean.close()
    fsigma.close()

    return mean, sigma

def standardize(df,mean=None,sigma=None):
    """
        Returns a standardized DataFrame
        Parameters
        ----------
        df : DataFrame
            The DataFrame containing the data to be standardized
        mean : dictionary
            A dictionary containing the mean values for the distributions
            or None in case one wants to build the dictionary  
        sigma : dictionary
            A dictionary containing the sigma values for the distributions
            or None in case one wants to build the dictionary  
  
        Returns
        ----------
        df : DataFrame
            Standardized DataFrame
    """
    assert mean is not None and sigma is not None, "Problem in Mean or Sigma parameters."
    for i in feat:
        df[i] = (df[i]-mean[i])/sigma[i]
        
    return df

def create_model(seed):
    """
        Returns the neural network architecture
        Parameters
        ----------
        seed : int
            The seed used for weight initializing if looking for completely reproducible results 
  
        Returns
        ----------
        model : Sequential
            Keras Sequential Model
    """
    initializer = tf.keras.initializers.HeNormal(seed=seed)
    activation = "elu"
    model = tf.keras.Sequential(
        [
            Dense(128, activation=activation, name="layer01", kernel_initializer=initializer),
            Dropout(0.2),
            Dense(64,  activation=activation, name="layer02", kernel_initializer=initializer),
            Dropout(0.2),
            Dense(16,  activation=activation, name="layer03", kernel_initializer=initializer),
            Dropout(0.2),
            Dense(1, name="output"),
        ]
    )
    model.compile(
        optimizer = Adam(learning_rate = 1e-3),
        loss = mse_loss if LOSS == 'mse' else huber_loss
    )
    return model

def retrieve_model(model_location):
    """
        Returns trained model
        Parameters
        ----------
        model_location : string
            Folder built using train.py function, containing the dictionaries
            of mean and sigma and the trained model.
  
        Returns
        ----------
        model : Sequential
            Keras Sequential Model
    """
    model = tf.keras.models.load_model(f"{model_location}/model")
    return model

def eval_loss(X,y,model,loss_function):
    """
        Returns the evaluated loss function based on the trained model
        Parameters
        ----------
        X : DataFrame
            The DataFrame containing the features
        y : DataFrame
            The DataFrame containing the RMSD
        model : tf.keras.model
            The model to be used in the predictions
        loss_function : string
            Loss to be used in the calculations, accepts only "mse" or "huber"
  
        Returns
        ----------
        loss
            Calculated loss
    """
    assert loss_function in ['mse','huber'], f"Unknown Loss Function: {loss_function}"
    yh = model.predict(X)
    return mse_loss(y,yh).numpy() if loss_function == 'mse' else huber_loss(y,yh).numpy()
