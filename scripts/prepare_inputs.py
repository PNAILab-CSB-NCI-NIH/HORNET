#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author:
        Maximilia F. S. Degenhardt <frazaodesouzam2@nih.gov>
        Hermann F. Degenhardt <degenhardthf@nih.gov>
"""
import os, sys
import pandas as pd
sys.path.append("../src")
from hornet.input import prepare_inputs


def help():
    return """
prepare_inputs.py: Prepare the inputs for HORNET approaches (UML and DNN).
USAGE:
    python input_prep.py <input-directory> [<base-pairs>] [<base-stacking>] [-h]

Positional Arguments:
    <input-directory>           Type [String]: Input and output directory.
                                Example: 'data'
    <base-pairs>                Type [Int]: Average number of base-pairing.
                                Example: 88
    <base-stacking>             Type [Int]: Average number of base-stacking.
                                Example: 192

Options:
    [-h, --help]                Displays usage and help information for the script.
                                
Example:
python prepare_inputs.py ../data/TUTORIAL

Requirements:
    python = 3.9
"""

def args(argslist):
    """
    Parses a list of arguments and returns a tuple containing the path, base pairing, and base stacking values.

    Parameters:
        argslist (list): A list of arguments to parse.

    Returns:
        tuple: A tuple containing the path (str), base pairing (int), and base stacking (int) values.
    """

    # Input list of arguments to parse
    print(" - Checking arguments...")
    user_args = argslist[1:]

    if '-h' in user_args or '--help' in user_args:
        print(help())
        sys.exit(0)

    path = None
    base_pairing = -1
    base_stacking = -1
    if len(user_args) == 0:
        print(help())
        print("ERROR: Required argument not found: input file.")
        sys.exit(1)
    else:
        path = os.path.abspath(user_args[0])
    
    if len(user_args) > 1:
        if len(user_args) == 3:
            base_pairing = int(user_args[1])
            base_stacking = int(user_args[2])
        else:
            print(help())
            print("ERROR: Since you provided an argument for base-pairs it is expected one for base-stacking as well.")
            sys.exit(1)

    return path, base_pairing, base_stacking

def main():
    # Get user arguments
    path, base_pairing, base_stacking = args(sys.argv)

    # Read files
    prepare_inputs(path, base_pairing, base_stacking)

if __name__ == '__main__':
    main()
