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
sns.set(font_scale=1)

path_traj = '{dir_path}/UML/data/'   #### Path to Full_Trajectory file
dcd_traj = '{path_folder with all dcd files named as k*.dcd}'      #####path to dcd files with name k*.dcd where * is the respected used kappa value for dynamic fitting
ref = '{path}/file_name.pdb'   #### reference topology structure in CG model

fn = f'{path_traj}/Full_Trajectory.csv'
df1 = pd.read_csv(fn, sep=',')
##print (df1.shape)
#############Write output CG-Model for aa-Conv
kappas =df1['kapa'].unique() 
##print(max(kappas))
for i in kappas:
     file = f'{dcd_traj}/k{i}.dcd'    ##locating dcd file for k = i
     traj = md.load_dcd(file, top=ref)
     #print (traj)
     ka=i
     FRAME = df1[df1['kapa'] == i]['frame']
     if len(FRAME) > 0:
         print (file)
         for z in range (0,len(FRAME),1000):  #Write pdb every 1000 frames
             #print (FRAME.iat[z])
             Targ = FRAME.iat[z]
             if Targ > 0:
               P = Targ - 1 
               traj[(P)].save("Modelk%sFrame_%s.pdb"%(ka,Targ))
