import os
import sys
import pandas as pd

kappa_num=pd.read_csv('kappa.txt')
n_jobs = len(kappa)
init = 0 #starts at 0

src = '/data/PNAI/Maximilia/scripts/pred_RMSD/trtrRnaseP'
workingdir = '/data/PNAI/Maximilia/CafeMol/Yun_Tzai/trtrRnaseP/cafemol/analysis'
base = '/data/PNAI/Maximilia/CafeMol/Yun_Tzai/trtrRnaseP/cafemol'
dirs = [d for d in os.listdir(base) if d[0] == 'P']
n_jobs = len(dirs)

os.mkdir(f"{workingdir}/output")
for i in range(0,n_jobs):
	name = dirs[i]
	print(f"Submit job {i}/{n_jobs-1} ({name})")
	os.chdir(f"{workingdir}/output")
	full_dir = f"{workingdir}/output/{name}"
	os.mkdir(full_dir)
	os.chdir(full_dir)
	os.system(f"cp {src}/*.sh .")
	os.system(f"cp {src}/*.py .")
	os.system(f"cp {workingdir}/job.sh .")
	os.system(f"sed -ie \'s:path = :path = \"{full_dir}\":g\' input_prep.py")
	os.system(f"sed -ie \'s:path = :path = \"{full_dir}\":g\' UML.py")
	os.system(f"sed -ie \'s:path = :path = \"{full_dir}\":g\' Prediction.py")
	os.system(f"sed -ie \'s:path = :path = \"{full_dir}\":g\' Prediction_Cohort.py")
	k_dirs = [d for d in os.listdir(f"{base}/{name}") if d[0] == 'k']
	for k in k_dirs:
		os.system(f"cp -v {base}/{name}/{k}/output/*.ts en_all{k}.txt")
	os.system(f"sbatch --cpus-per-task={cpus} --mem={memory} --time={walltime} --partition={partition} job.sh")
	#os.system(f"sbatch --ntasks=32 --ntasks-per-core=1 --partition=multinode --constraint=x2695 job.sh")
