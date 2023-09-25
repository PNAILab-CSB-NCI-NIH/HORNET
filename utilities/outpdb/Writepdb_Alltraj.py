#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 14:16:02 2023

@author: frazaodesouzam2
"""

import mdtraj as md
import os
import sys
import numpy as np
import pandas as pd
os.system('pwd')

path_traj = './'                # Path to file with frame number to be written out 
file_name = 'Top10.csv'         # Path to Top10, Cohort file or other where we want to write the pdbs
dcd_traj  = './'                # Path to dcd files with name k*.dcd where * is the respected used kappa value for dynamic fitting
ref       = './ref_model.pdb'   # Reference topology structure in CG model

fn = f'{path_traj}/{file_name}'
df1 = pd.read_csv(fn, sep=',')

# Write output CG-Model for aa-Conv
kappas = df1['kapa'].unique()

for i in kappas:
    i = int(i)
    # Locating dcd file for k = i
    file = f'{dcd_traj}/k{i}.dcd'
    traj = md.load_dcd(file, top=ref)
    FRAME = df1[df1['kapa'] == i]['frame']
    if len(FRAME) > 0:
        # Write pdb every 1 frames (could be optimized as needed) 
        for z in range (0, len(FRAME), 1):
            Targ = int(FRAME.iat[z])
            if Targ > 0:
                P = Targ - 1
                traj[(P)].save("Modelk%sFrame_%s.pdb"%(i,Targ))
