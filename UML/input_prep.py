#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author:
        Maximilia F. S. Degenhardt <frazaodesouzam2@nih.gov>
        Hermann F. Degenhardt <degenhardthf@nih.gov>
"""
import os, sys
import pandas as pd
from utils import get_input_data, filter_data, save_transformed

def main():
    """
        Main function to prepare the files from the dynamic fitting as input to UML
        and DNN approaches.
        Parameters
        ----------
        path : string
            Input and output folder where the files from the analysis will be stored
        base_pairing : int
            Number of base-pairing
        base_stacking : int
            Number of base-stacking
    """
    # Get user argument
    path, base_pairing, base_stacking = args(sys.argv)

    # Read files
    if (base_pairing > 0 and base_stacking > 0):
        print(f" - Average number of base-pairing: {base_pairing}")
        print(f" - Average number of base-stacking: {base_stacking}")
    print(f" - Reading files from: {path}")
    df = get_input_data(path, base_pairing, base_stacking)

    # Filtering
    print(" - Filtering")
    df = filter_data(df)

    # Save dataset
    print(" - Saving")
    save_transformed(df,path=path,name='Full_Trajectory')

def help():
    return """
input_prep.py: Prepare the inputs for HORNET approaches (UML and DNN).
USAGE:
    python input_prep.py <input-directory> [<base-pairing>] [<base-stacking>] [-h]

Positional Arguments:
    <input-directory>           Type [String]: Input and output directory.
                                Example: 'data'
    <base-pairing>              Type [Int]: Average number of base-pairing.
                                Example: 80
    <base-stacking>             Type [Int]: Average number of base-stacking.
                                Example: 120

Options:
    [-h, --help]                Displays usage and help information for the script.
                                
Example:
python input_prep.py data

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

    path = 'data'
    base_pairing = -1
    base_stacking = -1
    if len(user_args) > 0:
        path = user_args[0]
    if len(user_args) > 1:
        base_pairing = int(user_args[1])
        base_stacking = int(user_args[2])

    return path, base_pairing, base_stacking

if __name__ == '__main__':
    main()
