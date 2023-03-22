#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 14:16:02 2023

@author: frazaodesouzam2
"""
import os
import sys
import numpy as np
import pandas as pd
os.system('pwd')

path1 = '{pdb_folder}' ###add path to the pdb model to calculate the base pair and base stack value
cafe='{path}/aa_conv/Bases_Calc/'     #### Add path to the standart cafemol input - Cohort.inp #### Note this should be in a folder diferent than the pdbs

basep=[]
bases=[]
kappa=[]
frame=[]
BasesNumber=pd.DataFrame(columns=['baseP','baseS','native'])
for refine in os.listdir(f"{path1}"):
	if refine.endswith('.pdb'):
		pdb= refine
		T= pdb.split("_")
		F1= T[1].split(".")
		frame.append(F1[0])
		T= pdb.split("k")
		TF= T[1].split("F")
		kappa.append(TF[0])
		os.system(f"cp {cafe}/Cohort.inp .")
		os.mkdir(f"output")
		os.system(f"sed -ie \'s:filename =:filename = {pdb}:g\' Cohort.inp")		
		os.system(f"sed -ie \'s:1    rna:1    rna    {pdb}:g\' Cohort.inp")
		os.system(f"sed -ie \'s:XLNRA:1 {pdb}:g\' Cohort.inp")
		os.system(f"{path_cafemol}/bin/cafemol Cohort.inp -machinefile > runlog") #### Add path to cafemol.exe
		ninfoN=f'output/{pdb}.ninfo'
		ninfo=get_param(ninfoN)
		size=len(ninfo)
		j=0
		for i in ninfo:
			#print(i)
               		if i.startswith('<<<< native basepair'):
               			#print(ninfo[j+1])
               			t=ninfo[j+1].split('=')
               			t=t[1]
               			basep.append(t.strip())
               			#print(basep)
               		if i.startswith('<<<< native basestack'):
               			t=ninfo[j+1].split('=')
               			t=t[1]
               			bases.append(t.strip())
               			#print(bases)
		       	#print(df1[j])
               		j=j+1
BasesNumber['baseP']=basep
BasesNumber['baseS']=bases
BasesNumber['frame']=frame
BasesNumber['kappa']=kappa

BasesNumber.to_csv('BasesTotalValues.csv')
