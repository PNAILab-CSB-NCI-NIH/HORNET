import os
import sys
import numpy as np
import pandas as pd
import subprocess
import re

kappa_num = np.loadtxt('kappa.txt')
n_jobs = len(kappa_num)

# Add your working directory here, such as '<path>/HORNET/DynamicFitting/templates/kappa_scan'
workingdir = '<path>/HORNET/DynamicFitting/templates/kappa_scan'

if not os.path.exists(workingdir):
    print(f"Working directory {workingdir} does not exist. Please create it.")

# Number of residues in reference PDB
group = subprocess.check_output(f"grep 'GROUP' {workingdir}/k1/input.inp",shell=True)
group = group.decode()

no_of_particles = re.split('\)|\(|1-',group)
no_of_particles = int(no_of_particles[4])

# For loop to create folders
for i in range(0,n_jobs):
    name = int(kappa_num[i])
    print(f"Creating folder kappa={name}")
    os.mkdir(f"{workingdir}/k{name}")
    os.chdir(f"{workingdir}/k{name}")
    os.system(f"cp -r {workingdir}/k1/* .")
    
    # Set kappa and modify input.inp
    kappa_result = name*no_of_particles*0.001987*298
    os.system(f"sed -ie \'s:k       =  5705.726136:k       =   {kappa_result}:g\' input.inp")
    os.system(f"sed -ie \'s:k=kappa*N*kB*T=12*803*0.001987*298:k=kappa*N*kB*T={name}*803*0.001987*298:g\' input.inp")
