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

sys.path.append("../src")
from hornet.model import predict

def help():
        return """
predict.py: Evaluate RMSDs based on the trained HORNET model
USAGE:
    python predict.py -d <dataset> -n <number-of-residues> -m <model-location>
                      [-o <output-directory>] [-k <kappa-cut>] [-f <frame-cut>] [-h]

SYNOPSIS:
    Predict RMSDs (score) using HORNET model, based on the argument parameters of the user.

Required Arguments:
    [-d, --dataset]             Type [String]: Data location to be used for predictions
                                Example: "../data/predict_sample1.csv"
    [-n, --number-of-residues]  Type [Int]: Number of residues related to the input RNA
                                dataset. Considering the example above, if predict_sample1
                                has 268 ncl, one should use: 
                                Example: 268
    [-m, --model-location]      Type [String]: Directory where the model is stored.
                                Example: 'my_trained_model'

Optional Arguments
    [-o, --output-directory]    Type [String]: Output directory.
                                Example: 'my_output'
    [-k, --kappa-cut]           Type [Int]: Number of kappa cut to train the model.
                                Default: 50
    [-f, --frame-cut]           Type [Int]: Number of frame cut to train the model.
                                Default: 2000
    [-h, --help]                Displays usage and help information for the script.

Requirements:
    python = 3.9
    tensorflow = 2.13
"""

def get_arg(args, option):
    """
    A function that retrieves the argument value associated with a given option from a list of arguments.

    Parameters:
        args (list): A list of arguments.
        option (str): The option to search for within the list of arguments.

    Returns:
        str: The argument value associated with the given option, or None if the option is not found.
    """
    for i in range(len(args)):
        if args[i] in option:
                return args[i+1]

def args(argslist):
    """
    Parses a list of arguments and returns the necessary values for further processing.

    Parameters:
        argslist (list): A list of arguments to parse.

    Returns:
        tuple: A tuple containing the following values:
            - output_folder (str): The output folder for predictions.
            - model_location (str): The location of the model.
            - dataset (str): The dataset to use.
            - n_residues (int): The number of residues.
            - max_kappa (int): The maximum kappa value.
            - min_frame (int): The minimum frame value.
    """

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

    if ('dataset' not in passed.keys() or \
        'n_residues' not in passed.keys() or \
            'model_location' not in passed.keys()):
        print(help())
        print("ERROR: One of more required arguments not found: dataset, model or number of residues")
        sys.exit(1)
        
    if 'model_location' in passed.keys():
        model_location = os.getcwd() + "/" + str(passed['model_location'])
    if 'dataset' in passed.keys():
        dataset = passed['dataset']
        output_folder = dataset[0:-len(dataset.split("/")[-1])]
        if output_folder == "":
            output_folder = os.getcwd()
    if 'output_folder' in passed.keys():
        output_folder = os.getcwd() + "/" + str(passed['output_folder'])
    if 'n_residues' in passed.keys():
        if passed['n_residues'].isnumeric():
            n_residues = int(passed['n_residues'])
        else:
            raise ValueError("Expecting an integer for the number of residues")
    if 'max_kappa' in passed.keys():
        if passed['max_kappa'].isnumeric():
            max_kappa = int(passed['max_kappa'])
        else:
            raise ValueError("Expecting an integer for the maximum kappa value")
    if 'min_frame' in passed.keys():
        if passed['min_frame'].isnumeric():
            min_frame = int(passed['min_frame'])
        else:
            raise ValueError("Expecting an integer for the minimum frame value")

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
