#!/usr/bin/env python
# coding: utf-8
"""
Author:
        Hermann F. Degenhardt <degenhardthf@nih.gov>
        Maximilia F. S. Degenhardt <frazaodesouzam2@nih.gov>
"""

import pandas as pd
import os, sys, json
import seaborn as sns

from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, AlphaDropout
from tensorflow.keras.optimizers import Adam
from keras.regularizers import l2

built_feat = [
    'cc7xEtot'
]
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

def read_data(dataset, n_residues, min_frame, max_kappa):
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
        df_i = clean_data(df_i, min_frame, max_kappa)
        df_i = normalize(df_i, n_residues[i])
        df_i = featurize(df_i)
        dfs.append(df_i)
    df = pd.concat(dfs)
    df = df.reset_index(drop=True)
    return df


def clean_data(df, frame_cut, kappa_cut):
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


def normalize(df, n_residues):
    """
        Returns a normalized DataFrame. This step is necessary since each RNA
        will yield different values of energies depending on its size, radius of
        gyration and other characteristics.
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


def extract_mean_and_sigma(df, output_folder):
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

    # Clear
    fmean.close()
    fsigma.close()

    return mean, sigma


def standardize(df, mean=None, sigma=None):
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
    if mean is None or sigma is None:
        raise ValueError("Problem in Mean or Sigma parameters.")
    for f in feat:
        if f not in mean.keys():
            raise KeyError(f"{f} not in mean dictionary.")
    for f in feat:
        if f not in sigma.keys():
            raise KeyError(f"{f} not in sigma dictionary.")

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


def train(
        output_folder = 'output_folder',
        dataset = [],
        n_residues = [],
        validation = "",
        validation_residues = -1,
        max_epochs = 300,
        max_kappa = 50,
        min_frame = 2000,
        loss_function = 'mse',
        seed = 101
    ):
    """
        Main function to train HORNET model.
        Parameters
        ----------
        output_folder : string
            Output folder where the model and configurations will be stored
        dataset : Array(string)
            An array of strings containing the data locations
        n_residues : Array(int)
            An array of integers containing the number of residues from each dataset 
        validation : string
            The path containing the validation location; if this is not passed, it will
            split the dataset into 2 parts.
        validation_residues : int
            The number of residues for the validation set, if passed
        max_epochs : int
            Number of epochs to train the model 
        max_kappa : int
            Maximum accepted kappa 
        min_frame : int
            Minimum frame cut 
        loss_function : string
            Accepts 'mse' or 'huber'
        seed : int
            Seed to be used if one wants to follow fully reproducible results 
    """

    # Create output folder
    print("\n - Setting up")
    print(f"Output folder: {output_folder}")

    assert not os.path.exists(output_folder), "Output folder already exists!"
    os.system(f"mkdir {output_folder}")
    LOSS = loss_function

    # Check some parameters
    if type(dataset) is not list:
        raise TypeError("Dataset must be a list of files.")
    if type(n_residues) is not list:
        raise TypeError("Dataset must be a list of files.")
    if len(dataset) != len(n_residues):
        raise ValueError("Dataset and n_residues must have the same length.")

    # Read datasets from argument
    print("\n - Reading training data")
    df = read_data(dataset,n_residues,min_frame,max_kappa)
    mean, sigma = extract_mean_and_sigma(df,output_folder)
    df = standardize(df,mean,sigma)
    df = df[all_feat]
    print(f"   > Shape of training data: {df.shape}")

    if len(df) == 0:
        raise ValueError("No training data found or completely filtered.")

    # If user inserted a validation set
    if (validation != ""):
        print("\n - Reading validation data")
        df_val = read_data([validation],[validation_residues],min_frame,max_kappa)
        df_val = standardize(df_val,mean,sigma)
        df_val = df_val[all_feat]
        print(f"   > Shape of validation data: {df_val.shape}")

        if len(df_val) == 0:
            raise ValueError("No validation data found or completely filtered.")
        X_train, X_val, y_train, y_val = df[feat], df_val[feat], df[target], df_val[target]
    else:
        X_train, X_val, y_train, y_val = train_test_split(df[feat],df[target],test_size=0.2,random_state=101)

    # Get the model and configure data
    print("\n - Setting up model")
    model = create_model(seed=seed)
    checkpoint = tf.keras.callbacks.ModelCheckpoint(f"{output_folder}/best_val_loss.h5", 
        verbose = 1, 
        monitor = 'val_loss',
        save_best_only = True, 
        mode = 'auto'
    )
    
    # Train the model
    print("\n - Training")
    history = model.fit(
        X_train,
        y_train,
        epochs=max_epochs,
        batch_size=128,
        callbacks=[checkpoint],
        validation_data=(X_val, y_val)
    )
    tf.keras.backend.clear_session()

    # Save trained model for maximum epochs
    model.save(f"{output_folder}/model_{max_epochs}e")

    # Reload the weights from the epoch with best loss on validation set to save and for sequential plots
    model.load_weights(f"{output_folder}/best_val_loss.h5")

    # Save trained model for best loss on the validation set
    model.save(f"{output_folder}/model")

    # Evaluate performance using an initial validation set
    print("\n - Evaluate Initial Validation Set")
    results = pd.DataFrame()
    results['y'] = y_val
    results['yh'] = model.predict(X_val)

    # Plot predictions
    try:
        sns.displot(data=results, x="yh", y="y", bins=200)
        plt.xlim(0,40)
        plt.ylim(0,40)
        plt.xlabel("Predicted RMSD (Initial Validation Set)")
        plt.ylabel("Real RMSD (Initial Validation Set)")
        plt.savefig(f"{output_folder}/validation_prediction.png")
        plt.draw()
        plt.close()
    except:
        pass

    # Plot loss
    sns.lineplot(data=history.history['loss'],     color='blue',   label="Training Set")
    sns.lineplot(data=history.history['val_loss'], color='orange', label="Validation Set")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.savefig(f"{output_folder}/loss.png")
    plt.draw()
    plt.close()


def predict(
        output_folder = 'output_folder',
        model_location = 'input_folder',
        dataset = '',
        n_residues = '',
        max_kappa = 50,
        min_frame = 2000
    ):
    """
        Main function to predict RMSDs based on the trained model.
        Parameters
        ----------
        output_folder : string
            Output folder where the model and configurations will be stored
        model_location : string
            Folder where the trained model and configurations are be stored
        dataset : Array(string)
            An array of strings containing the data locations
        n_residues : Array(int)
            An array of integers containing the number of residues from each dataset 
        min_frame: int
            Minimum frame cut 
        max_kappa: int
            Maximum accepted kappa
    """

    print("\n - Setting up")
    print(f"   Output folder: {output_folder}")
    print(f"   Predictions will be stored at {output_folder}/{dataset.split('/')[-1][:-4]}_prediction.csv.")

    if (not os.path.exists(output_folder)):
        f"   Creating output folder"
        os.system(f"mkdir {output_folder}")

    print("\n - Reading data")
    df = read_data([dataset],[n_residues],min_frame,max_kappa)
    mean, sigma = retrieve_mean_and_sigma(model_location)
    df = standardize(df,mean,sigma)
    print(f"   > Shape of data: {df.shape}")
    if len(df) == 0:
        raise ValueError("No data found or completely filtered.")

    print("\n - Setting up model")
    X = df[feat]
    model = retrieve_model(model_location)

    print("\n - Evaluate Predictions")
    df['prediction'] = model.predict(X)
    cols = ['frame','kapa','prediction']

    df[cols].to_csv(f"{output_folder}/{dataset.split('/')[-1][:-4]}_prediction.csv",index=False)
    print(f"   Predictions stored at {output_folder}/{dataset.split('/')[-1][:-4]}_prediction.csv.")
    
    df = df.sort_values(by=['prediction'], ascending=True)
    n_top = 10
    df[cols].iloc[:n_top].to_csv(f"{output_folder}/{dataset.split('/')[-1][:-4]}_Top{n_top}.csv",index=False)
    print(f"   Top {n_top} predictions stored at {output_folder}/{dataset.split('/')[-1][:-4]}_Top{n_top}.csv.")