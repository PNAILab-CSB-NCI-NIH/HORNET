#!/usr/bin/env python
# coding: utf-8
"""
Author:
        Hermann F. Degenhardt <degenhardthf@nih.gov>
        Maximilia F. S. Degenhardt <frazaodesouzam2@nih.gov>
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random, math, os, sys, json

from utils import *

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
            split the dataset into 2 parts. The real tests should be using other
            trajectories and RNAs.
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

    # Read datasets from argument
    print("\n - Reading training data")
    df = read_data(dataset,n_residues,min_frame,max_kappa)
    mean, sigma = extract_mean_and_sigma(df,output_folder)
    df = standardize(df,mean,sigma)
    df = df[all_feat]
    print(f"   > Shape of training data: {df.shape}")

    # If user inserted a validation set
    if (validation != ""):
        print("\n - Reading validation data")
        df_val = read_data([validation],[validation_residues],min_frame,max_kappa)
        df_val = standardize(df_val,mean,sigma)
        df_val = df_val[all_feat]
        print(f"   > Shape of validation data: {df.shape}")
        X_train, X_val, y_train, y_val = df[feat], df_val[feat], df[target], df_val[target]
    else:
        X_train, X_val, y_train, y_val = train_test_split(df[feat],df[target],test_size=0.2,random_state=101)

    # Get the model and configure data
    print("\n - Setting up model")
    model = create_model(seed=seed)
    
    # Train and save the model
    print("\n - Training")
    model.fit(X_train,y_train,epochs=max_epochs,batch_size=128,validation_data=(X_val, y_val))
    tf.keras.backend.clear_session()
    model.save(f"{output_folder}/model")

    # Evaluate performance using an initial validation set
    print("\n - Evaluate Initial Validation Set")
    results = pd.DataFrame()
    results['y'] = y_val
    results['yh'] = model.predict(X_val)
    results['y-yh'] = results['y'] - results['yh']

    print(f"Std Deviation: {results['y-yh'].std()}")
    results['y-yh'].hist(bins=200)
    plt.xlabel("Real RMSD - Predicted (Initial Validation Set)")
    plt.savefig(f"{output_folder}/validation_distribution.png")
    plt.draw()
    plt.close()

    sns.displot(data=results, x="yh", y="y", bins=200)
    plt.xlim(0,40)
    plt.ylim(0,40)
    plt.xlabel("Predicted RMSD (Initial Validation Set)")
    plt.ylabel("Real RMSD (Initial Validation Set)")
    plt.savefig(f"{output_folder}/validation_prediction.png")
    plt.draw()
    plt.close()

def get_arg(args,option):
    for i in range(len(args)):
        if args[i] in option:
                return args[i+1]

def help():
        return """
train.py: Train the HORNET model
USAGE:
    python train.py -o <output-directory> -d <dataset> -n <number-of-residues>
                    [-v <validation>] [-vn <validation-residues>] [-e <epochs>]
                    [-k <kappa-cut>] [-f <frame-cut>] [-l <loss-function>] [-s <seed>] [-h]

SYNOPSIS:
    Train a HORNET model based on the argument parameters of the user.

Required Arguments:
    [-o, --output-directory]    Type [String]: Output directory.
                                Example: 'my_output'
    [-d, --dataset]             Type [String]: Array of datasets to be used in training,
                                separated by commas.
                                Example: "data/train_sample1.csv,data/train_sample2.csv"
    [-n, --number-of-residues]  Type [Int]: Array of the number of residues related to the
                                RNA datasets. Considering the example above, if train_sample1
                                has 200 ncl and train_sample2 has 500, one should use: 
                                Example: 200,500

Optional Arguments:
    [-v, --validation]          Type [String]: Datasets to be used as validation, if any.
                                Example: "data/train_sample2.csv"
    [-vn, --validation-residues] Type [Int]: Number of residues related to the validation data.
                                Example: 200
    [-e, --epochs]              Type [Int]: Number of epochs to train the model.
                                Default: 300
    [-k, --kappa-cut]           Type [Int]: Number of kappa cut to train the model.
                                Default: 50
    [-f, --frame-cut]           Type [Int]: Number of kappa cut to train the model.
                                Default: 20
    [-l, --loss-function]       Type [String]: Loss function to be used to train the model.
                                Default: "huber", can be either 'huber' or 'mse'
    [-s, --seed]                Type [Int]: Seed to mantain reproducible results across tests.
                                Default: 101, use 0 for random
    [-h, --help]                Displays usage and help information for the script.

Requirements:
    python = 3.7
    tensorflow = 2.11
"""

def args(argslist):
    """Parses command-line args from "sys.argv". Returns a list of parsed arguments."""

    # Input list of arguments to parse
    print(" - Checking arguments...")
    user_args = argslist[1:]
    output_folder = os.getcwd() + "/test_training"
    validation = ""
    validation_residues = -1
    max_epochs = 300
    max_kappa = 50
    min_frame = 2000
    loss_function = "mse"
    seed = 101

    possible_args = [
        ['-h','--help','help'],
        ['-o','--output-folder','output_folder'],
        ['-d','--dataset','dataset'],
        ['-n','--number-of-residues','n_residues'],
        ['-v','--validation','validation'],
        ['-vn','--validation-residues','validation_residues'],
        ['-e','--epochs','max_epochs'],
        ['-k','--kappa-cut','max_kappa'],
        ['-f','--frame-cut','min_frame'],
        ['-l','--loss-function','loss'],
        ['-s','--seed','seed'],
    ]

    if '-h' in user_args or '--help' in user_args:
        print(help())
        sys.exit(0)

    passed = {}
    for p in possible_args:
        if p[0] in user_args or p[1] in user_args:
            passed[p[2]] = get_arg(user_args,p[:-1])
    
    if ('output_folder' not in passed.keys() or \
        'dataset' not in passed.keys() or \
        'n_residues' not in passed.keys()):
        print("Required arguments not found: output folder, dataset or number of residues")
        print(help())
        sys.exit(1)

    if 'output_folder' in passed.keys():
        output_folder = os.getcwd() + "/" + str(passed['output_folder'])
    if 'dataset' in passed.keys():
        dataset = passed['dataset'].split(',')
    if 'n_residues' in passed.keys():
        n_residues = [int(p) for p in passed['n_residues'].split(',')]
    if 'validation' in passed.keys():
        validation = str(passed['validation'])
    if 'validation_residues' in passed.keys():
        validation_residues = int(passed['validation_residues'])
    if 'max_epochs' in passed.keys():
        max_epochs = int(passed['max_epochs'])
    if 'max_kappa' in passed.keys():
        max_kappa = int(passed['max_kappa'])
    if 'min_frame' in passed.keys():
        min_frame = int(passed['min_frame'])
    if 'loss' in passed.keys():
        loss_function = int(passed['loss'])
    if 'seed' in passed.keys():
        seed = int(passed['seed'])
    if seed == 0:
        seed = None

    print(f"   > Output folder: {output_folder}")
    print(f"   > Dataset: {dataset}")
    print(f"   > Number of Residues: {n_residues}")
    print(f"   > Validation: {validation}")
    print(f"   > Validation Residues: {validation_residues}")
    print(f"   > Epochs: {max_epochs}")
    print(f"   > Max Kappa: {max_kappa}")
    print(f"   > Min Frame: {min_frame}")
    print(f"   > Loss Function: {loss_function}")
    print(f"   > Seed: {seed}")

    return output_folder, dataset, n_residues, validation, validation_residues, max_epochs, max_kappa, min_frame, loss_function, seed

def main():
    # Get user arguments
    output_folder, dataset, n_residues, validation, validation_residues, max_epochs, max_kappa, min_frame, loss_function, seed = args(sys.argv)

    # Call function
    train(output_folder, dataset, n_residues, validation, validation_residues, max_epochs, max_kappa, min_frame, loss_function, seed)

if __name__ == '__main__':
    main()
