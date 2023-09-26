#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author:
        Maximilia F. S. Degenhardt <frazaodesouzam2@nih.gov>
        Hermann F. Degenhardt <degenhardthf@nih.gov>
"""
import os, sys
import pandas as pd
from hornet.uml import filter_data

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

def get_input_data(path, base_pairing=-1, base_stacking=-1, initial="en_all"):
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
        fn0 = f"{path}/{initial}k{N[k]}.txt"

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
        for i in range(0, len(df1)-1):
            T.append(df1[i].split())
        df1 = pd.DataFrame(T,columns=columns)
        df1 = df1.astype(float)
        df1['frame'] = range(0, len(df1))
        df1['kapa'] = int(N[k])
        if base_pairing < 0 or base_stacking < 0:
            df2 = pd.read_csv(f"{path}/bases_k{N[k]}.csv")
            df2 = df2.rename(columns={"base_pair": "baseP", "base_stack": "baseS"}, errors="raise")
            df1 = df1.merge(df2, how='left', on=["frame","kapa"])
        if base_pairing > 0:
            df1['baseP'] = base_pairing
        if base_stacking > 0:
            df1['baseS'] = base_stacking
            
        dfs.append(df1)
    
    if len(dfs) == 0:
        raise FileExistsError(f"No files found in {path}.")
    return pd.concat(dfs)


def save_transformed(df, path='data', name='Full_Trajectory'):
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


def prepare_inputs(path, base_pairing=-1, base_stacking=-1):
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

    # Read files
    if (base_pairing > 0 and base_stacking > 0):
        print(f" - Average number of base-pairing: {base_pairing}")
        print(f" - Average number of base-stacking: {base_stacking}")
    print(f" - Reading files from: {path}")
    df = get_input_data(path, base_pairing, base_stacking)

    # Filtering
    print(" - Filtering")
    df = filter_data(df)
    
    # Make sure the dataset was correctly filled
    assert (len(df[df['baseP'].isna()]) == 0 and len(df[df['baseS'].isna()]) == 0), "Found NaN entries in the DataFrame! Please, check your number of base-pairs/base-stacking."
    
    # Save dataset
    print(" - Saving")
    save_transformed(df, path=path, name='Full_Trajectory')