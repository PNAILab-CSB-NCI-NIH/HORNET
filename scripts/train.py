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
from hornet.model import train

def get_arg(args, option):
    """
    Get the value of an option from a list of command line arguments.
    
    Parameters:
        args (list): The list of command line arguments.
        option (str): The option to retrieve the value of.
        
    Returns:
        str: The value of the option, or None if the option is not found.
    """
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
                                Example: 268 for trRNAseP RNA.
    [-e, --epochs]              Type [Int]: Number of epochs to train the model.
                                Default: 300
    [-k, --kappa-cut]           Type [Int]: Number of kappa cut to train the model.
                                Default: 50
    [-f, --frame-cut]           Type [Int]: Number of frame cut to train the model.
                                Default: 2000
    [-l, --loss-function]       Type [String]: Loss function to be used to train the model.
                                Default: "huber", can be either 'huber' or 'mse'
    [-s, --seed]                Type [Int]: Seed to mantain reproducible results across tests.
                                Default: 101, use 0 for random
    [-h, --help]                Displays usage and help information for the script.

Requirements:
    python = 3.9
    tensorflow = 2.13
"""

def args(argslist):
    """
    Parses a list of arguments and returns the necessary values for further processing.

    Parameters:
        argslist (list): List of arguments to parse.

    Returns:
        tuple: A tuple containing the following values:
            - output_folder (str): The output folder path.
            - dataset (list): A list of dataset names.
            - n_residues (list): A list of integers representing the number of residues.
            - validation (str): A string representing the validation method.
            - validation_residues (int): The number of validation residues.
            - max_epochs (int): The maximum number of epochs.
            - max_kappa (int): The maximum kappa value.
            - min_frame (int): The minimum frame value.
            - loss_function (str): The loss function to be used.
            - seed (int): The random seed value.
    """

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
    loss_function_possibilities = ["huber", "mse"]
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
        print(help())
        print("ERROR: Required arguments not found: output folder, dataset or number of residues")
        sys.exit(1)

    if 'output_folder' in passed.keys():
        output_folder = os.getcwd() + "/" + str(passed['output_folder'])
    if 'dataset' in passed.keys():
        dataset = passed['dataset'].split(',')
    if 'n_residues' in passed.keys():
        try:
            n_residues = [int(p) for p in passed['n_residues'].split(',')]
        except:
            raise ValueError(f"ERROR: Invalid number of residues: {passed['n_residues']}")
    if 'validation' in passed.keys():
        validation = str(passed['validation'])
    if 'validation_residues' in passed.keys():
        if passed['validation_residues'].isnumeric():
            validation_residues = int(passed['validation_residues'])
        else:
            raise ValueError(f"ERROR: Invalid number of validation residues: {passed['validation_residues']}")
    if 'max_epochs' in passed.keys():
        if passed['max_epochs'].isnumeric():
            max_epochs = int(passed['max_epochs'])
        else:
            raise ValueError(f"ERROR: Invalid number of max epochs: {passed['max_epochs']}")
    if 'max_kappa' in passed.keys():
        if passed['max_kappa'].isnumeric():
            max_kappa = int(passed['max_kappa'])
        else:
            raise ValueError(f"ERROR: Invalid number of max kappa: {passed['max_kappa']}")
    if 'min_frame' in passed.keys():
        if passed['min_frame'].isnumeric():
            min_frame = int(passed['min_frame'])
        else:
            raise ValueError(f"ERROR: Invalid number of min frame: {passed['min_frame']}")
    if 'loss' in passed.keys():
        loss_function = passed['loss']
    if 'seed' in passed.keys():
        if passed['seed'].isnumeric():
            seed = int(passed['seed'])
        else:
            raise ValueError(f"ERROR: Invalid seed number : {passed['seed']}")
    if seed == 0:
        seed = None

    if loss_function not in loss_function_possibilities:
        raise ValueError(f"ERROR: Invalid loss function: {loss_function}")

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
