#! /bin/tcsh
#SBATCH --job-name="DF"

cd $SLURM_SUBMIT_DIR

/data/PNAI/yuba/software/cafemol_mod/bin/cafemol input.inp -machinefile $SLURM_JOB_NODELIST > runlog


