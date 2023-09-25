#! /bin/tcsh
#SBATCH --job-name="HoRNet"

cd $SLURM_SUBMIT_DIR

module load python/3.9

# Input prep
python input_prep.py

# UML
python UML.py

# DNN
module load cuDNN/7.6.5/CUDA-10.1 python/3.7
python Prediction.py

python Prediction_Cohort.py


