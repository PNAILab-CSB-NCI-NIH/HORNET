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

#from sklearn.model_selection import train_test_split
#from sklearn import metrics
#import tensorflow as tf
#from tensorflow.keras.layers import Dense, Dropout, AlphaDropout
#from tensorflow.keras.optimizers import Adam
#from keras.regularizers import l2

from utils import *

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

    print("\n - Setting up model")
    X = df[feat]
    model = retrieve_model(model_location)

    print("\n - Evaluate Predictions")
    df['prediction'] = model.predict(X)
    df.to_csv(f"{output_folder}/{dataset.split('/')[-1][:-4]}_prediction.csv",index=False)
    print(f"   Predictions stored at {output_folder}/{dataset.split('/')[-1][:-4]}_prediction.csv.")

def help():
        return """
predict.py: Evaluate RMSDs based on the trained HORNET model
USAGE:
    python predict.py -o <output-directory> -d <dataset> -n <number-of-residues>
                      -m <model-location> [-k <kappa-cut>] [-f <frame-cut>] [-h]

SYNOPSIS:
    Predict RMSDs (score) using HORNET model, based on the argument parameters of the user.

Required Arguments:
    [-o, --output-directory]    Type [String]: Output directory.
                                Example: 'my_output'
    [-m, --model-location]      Type [String]: Directory where the model is stored.
                                Example: 'my_trained_model'
    [-d, --dataset]             Type [String]: Data location to be used for predictions
                                Example: "data/predict_sample1.csv"
    [-n, --number-of-residues]  Type [Int]: Number of residues related to the input RNA
                                dataset. Considering the example above, if predict_sample1
                                has 200 ncl, one should use: 
                                Example: 200

Optional Arguments
    [-k, --kappa-cut]           Type [Int]: Number of kappa cut to train the model.
                                Default: 50
    [-f, --frame-cut]           Type [Int]: Number of kappa cut to train the model.
                                Default: 2000
    [-h, --help]                Displays usage and help information for the script.

Requirements:
    python = 3.7
    tensorflow = 2.11
"""

def get_arg(args,option):
    for i in range(len(args)):
        if args[i] in option:
                return args[i+1]

def args(argslist):
    """Parses command-line args from "sys.argv". Returns a list of parsed arguments."""

    # Input list of arguments to parse
    print(" - Checking arguments...")
    user_args = argslist[1:]
    output_folder = os.getcwd() + "/test_prediction"
    max_kappa = 50
    min_frame = 2000

    possible_args = [
        ['-h','--help','help'],
        ['-o','--output-folder','output_folder'],
        ['-m','--model-location','model_location'],
        ['-d','--dataset','dataset'],
        ['-n','--number-of-residues','n_residues'],
        ['-k','--kappa-cut','max_kappa'],
        ['-f','--frame-cut','min_frame'],
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
    if 'model_location' in passed.keys():
        model_location = os.getcwd() + "/" + str(passed['model_location'])
    if 'dataset' in passed.keys():
        dataset = passed['dataset']
    if 'n_residues' in passed.keys():
        n_residues = int(passed['n_residues'])
    if 'max_kappa' in passed.keys():
        max_kappa = int(passed['max_kappa'])
    if 'min_frame' in passed.keys():
        min_frame = int(passed['min_frame'])

    print(f"   > Output folder:      {output_folder}")
    print(f"   > Model location:     {model_location}")
    print(f"   > Dataset:            {dataset}")
    print(f"   > Number of Residues: {n_residues}")
    print(f"   > Max Kappa:          {max_kappa}")
    print(f"   > Min Frame:          {min_frame}")

    return output_folder, model_location, dataset, n_residues, max_kappa, min_frame

def main():
    # Get user arguments
    output_folder, model_location, dataset, n_residues, max_kappa, min_frame = args(sys.argv)

    # Call function
    predict(output_folder, model_location, dataset, n_residues, max_kappa, min_frame)

if __name__ == '__main__':
    main()
