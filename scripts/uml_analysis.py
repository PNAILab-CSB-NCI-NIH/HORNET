#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author:
        Maximilia F. S. Degenhardt <frazaodesouzam2@nih.gov>
        Hermann F. Degenhardt <degenhardthf@nih.gov>
"""

import os, sys, math

sys.path.append("../src")
from hornet.uml import uml_analysis

def help():
    return """
uml.py: Run the UML approach from HORNET to select top cohort of structures.
USAGE:
    python uml.py <full-trajectory-file> [-h]

Positional Arguments:
    <full-trajectory-file>      Type [String]: Input file (Full trajectory).
                                Example: 'data/Full_Trajectory.csv'
                                
Options:
    [-h, --help]                Displays usage and help information for the script.

Example:
python uml.py ../data/Full_Trajectory.csv

Requirements:
    python = 3.9
"""

def args(argslist):
    """
    Parse a list of arguments and return the input file to be used. 
    
    Parameters:
        argslist (list): A list of arguments to parse.
        
    Returns:
        str: The input file to be used.
    """

    # Input list of arguments to parse
    print(" - Checking arguments...")
    user_args = argslist[1:]

    if '-h' in user_args or '--help' in user_args:
        print(help())
        sys.exit(0)

    if len(user_args) > 0:
        input_file = user_args[0]
    else:
        print(help())
        print("ERROR: Required argument not found: input file")
        sys.exit(1)

    return input_file

def main():
    # Get user arguments
    input_file = args(sys.argv)

    # Call function
    uml_analysis(input_file)

if __name__ == '__main__':
    main()
