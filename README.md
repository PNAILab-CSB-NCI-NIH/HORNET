# HORNET

HORNET: Holistic RNA Structure Determination by Unsupervised Learning and Deep Neural Networks. HORNET is a software package for determining 3D topological structures of RNA conformers using atomic force microscopy topographic images and deep learning.


## I. Requirements

The software has been designed to be preferably operated on macOS and Linux operating systems. The requirements to run the software are:

1. Working installation of conda (miniconda or anaconda):
- [Linux](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html)
- [Mac](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html)

Tests were performed using conda 23.3.1 and Python 3.9

2. Dynamic Fitting output files (.ts) from CafeMol.  
See [here](DynamicFitting/README.md) for detailed explanations for how to perform Dynamic Fitting calculations using CafeMol. We strongly advise running the Dynamic Fitting using a range of kappa values (e.g., 2 to 24, in increments of 2 or 4).



## II. Installation of HORNET

After installing conda, please open a terminal and follow these steps to install the environment and package:

1. Create a “hornet” [conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) using:

```bash
conda create -n hornet python=3.9
```

2. Load the environment using:

```bash
conda activate hornet
```

3. Install hornet using pip:

```bash
pip install hornet@git+https://github.com/PNAI-CSB-NCI-NIH/HORNET.git
```

Note: HORNET installation should have included Tensorflow via requirements. If you encounter problems at this step, please check [Tensorflow's](https://www.tensorflow.org/install/pip#linux) documentation for help. The version used is 2.13. TensorFlow-related warnings may occur when running HORNET, but can often be ignored.

### Alternative with docker
Some of the latest versions of Mac may present issues when running tensorflow, even if there are no issues during the installation. A possible solution is described [here](https://developer.apple.com/metal/tensorflow-plugin/).

If you do not manage to install the package on your macOS, we included a docker image of the repository [here](https://github.com/users/hdegen/packages/container/package/hornet). To use the dockerized version you will need to download and install [docker](https://www.docker.com). Docker may need to use considerable resources from your computer, so we would advice to close other applications. After the installation, you can copy the image by running:

```bash
docker pull ghcr.io/hdegen/hornet:latest
```

This docker image includes the environment and scripts for running all the steps described below and it is only built if it passes all the unit tests, as directed in the Dockerfile. To start the container, simply use:

```bash
docker run --rm -it ghcr.io/hdegen/hornet
```

After running this command you should receive a bash shell inside the container and shoud be located inside the HORNET repository on the container, where you will have access to all scripts and can follow the next steps for running HORNET.

You can also build your own image of hornet by just running in the root directory of this repository (same place where the Dockerfile is located):

```bash
docker build -t hornet .
```

You can also choose a platform if needed, by including options such as "--platform linux/amd64", for example.

For running your own built image just then use:

```bash
docker run --rm -it hornet
```


## III. Steps for running HORNET

For running HORNET, if the user is not using the docker image they will need to download and unzip this repository in their own computer. If you are using docker, you can skip the next session "Downloading the repository" and go directly to the next one: "Pipeline Steps".

### Downloading the repository

For this initial step, on the top of the webpage there is a green button called "<> code". Press it and select "Download ZIP" on the options displayed. If the user is already used to git repositories, just clone using the git clone command. After donwloading the repository, please locate the downloaded file and unzip it. You can unzip it using the interface or you can also use terminal commands. For terminal commands, open your terminal and go to the directory where you downloaded the file, usually "~/Downloads":

```bash
cd ~/Downloads
```

And unzip the file:
```bash
unzip HORNET-main.zip
```

Finally, go to the HORNET unzipped folder:
```bash
cd HORNET-main
```

### Pipeline Steps

With the repository downloaded and accessible locally, the steps for running the application are as follows:

1. Input Preparation (Pre-processing data step)
2. Unsupervised Machine Learning (UML) Cohort Selection
3. Supervised Neural Network RMSD Estimation

All Python executable scripts can be found in the [scripts](scripts) folder, inside the repository.


### Step 1 - Input Preparation

This step is to transform the output files from dynamic fitting into input files required by HORNET.

#### 1. Copy Dynamic Fitting files

Copy the CafeMol output file (.ts) for each run (kappa value) into a project directory (e.g., HORNET/data/myproject).

#### 2. Rename addressing kappa values

Copy or rename each .ts file as a .txt file with the “en_all” prefix, followed by the kappa value associated with that file (e.g., en_allk14.txt for kappa=14). The kappa values used for AFM in the calculation are embedded in the name of the file and they will be extracted when loading the files.

As an example, if you had your calculation files inside of a given folder <Dynamic-Fitting-Output>, separated by different kappa values as subfolders, you would use:
```bash
cp <Dynamic-Fitting-Output>/<kappa>/<file-name.ts> en_allk<kappa>.txt
```

Note: Example .ts and .txt files associated with the TUTORIAL data are provided in [TUTORIAL](data/TUTORIAL): output_k14.ts, output_k22.ts, en_allk14.txt, and en_allk22.txt.

#### 3. Run the [prepare_inputs.py](scripts/prepare_inputs.py)

The preparation script 'prepare_inputs.py' transforms and merges all files in the current directory with the 'en_all' prefix, and generates an output file called 'Full_Trajectory.csv'. The numbers of base-pairs and base-stacking interactions are required for the normalization of each trajectory. These values can be provided as arguments, in which they are applied universally for all frames of all trajectories (e.g., averaged, estimated based on initial model). Alternatively, this information can be provided for each trajectory as a separate file containing comma separated values for all frames in that trajectory. Such files must be named as `bases_k<kappa>.csv` to match those of their corresponding `en_allk<kappa>.txt` files, and located in the same directory. These values can be found in the .ninfo file generated by CafeMol dynamic fitting (https://www.cafemol.org/) and for each initial (reference) structure, or they can be obtained using other software as desired.

Note: Example .csv files associated with the TUTORIAL data are provided in [TUTORIAL](data/TUTORIAL): bases_k14.csv and bases_k22.csv.

First, cd into the [scripts](scripts) directory.

```bash
cd scripts
```

Then, the script runs as follows:

```bash
python prepare_inputs.py <project-directory> [<base-pairs>] [<base-stacking>]
```

Inputs:
- project-directory: The location where all en_allk*.txt and bases_k*.txt (if applicable) files are located, as described in steps 1. and 2. above. 
- base-pairs (optional): Specified when bases_k<kappa>.csv files are not used.
- base-stacking (optional): Specified when bases_k<kappa>.csv files are not used.

Examples using TUTORIAL data:

(With bases_k<kappa>.csv files)
```bash
python prepare_inputs.py ../data/TUTORIAL
```
or

(With user-specified values)
```bash
python prepare_inputs.py ../data/TUTORIAL 88 192
```

Output:
- A file 'Full_Trajectory.csv' will be created in the same directory as the input file and contains the collection of all energy terms, CCAFM scores, kappa values, base-pairs, and base-stacking information for all calculated structures.

The typical running time on a normal computer is ~2 min for a dataset containing ~20 million entries.


### Step 2 - Unsupervised Machine Learning (UML) Cohort Selection

To select the top cohort structures using unsupervised learning, one just needs to run [uml_analysis.py](scripts/uml_analysis.py) as follows:

```bash
python uml_analysis.py <Path-to-Full-Trajectory-File>
```

For the TUTORIAL data, this would be:
```bash
python uml_analysis.py ../data/TUTORIAL/Full_Trajectory.csv
```

Input:
- Path-to-Full-Trajectory-File: The complete path for the Full_Trajectory.csv file, generated in the previous step.

Output (generated in the same directory as the input file):
- 'PCA_Cumulative_variance.pdf': Plot generated from principal component analysis (see note below)
- 'Kmeans_PCA_clustering.pdf': Plot generated from Kmeans and PCA clustering (see note below)
- 'Filtered_Data.csv': The first step of the UML analysis (Energy Filtering)
- 'Select_Cluster.csv': The second step of the UML analysis (PCA + Clustering)
- 'Final_Cohort.csv': The third step of the UML analysis (Cohort Selection)

The typical running time for this step on a normal computer is ~5 min for a dataset with ~20 million entries.

Note: During this step, the plot 'PCA_Cumulative_variance.pdf' will appear for inspection. After closing this pop-up window, the user can specify the number of principal components (default=8) in the command prompt. The number of principal components chosen should cover a minimum of 70% of the data (cumulative explained variance). Next, the script will generate the file 'Kmeans_PCA_clustering.pdf' to aid in selecting an appropriate number of clusters. Two curves are provided in this file: 1) a plot of Within-Cluster-Sum-of-Squares (WCSS) and 2) its first derivative. A number of clusters should be chosen that best represents the "elbow" of these two curves, i.e., the point at which increasing the number of clusters does not significantly improve the information content (before the plateau region).


### Step 3 - Supervised Neural Network RMSD Prediction

The script [predict.py](scripts/predict.py) is used to predict the RMSDs (scores) for a list of structures, which can be the Full_Trajectory (from Step 1), or any of the UML output files: Filtered_Data, Select_Cluster, Final_Cohort (from Step 2). The trained model will utilize common features among the list of structures as well as other information for normalization, such as the number of residues, base-pairs, and base-stacking interactions. The output files will be written to the same directory as the input data file, unless the output is specified. The script is run as follows:

```bash
python predict.py -d <dataset> -n <number-of-residues>  -m <model-location> \
                  [-o <output-directory>] [-k <kappa-cut>] [-f <frame-cut>] [-h]
```

Required Inputs:
- dataset: Path to the data file to be used, e.g., 'Full_Trajectory.csv', 'Filtered_Data.csv', 'Select_Cluster.csv' or 'Final_Cohort.csv' 
- number-of-residues: Number of residues in the RNA
- model-location: Path of the trained model to be used. If using HORNET's trained model, the location is [hornet](models/hornet). For information on using other trained models, see Section V. below.

Optional Inputs:
- output-directory: Path where the 'predictions' output folder will be created. The default is the same location as the input data file.
- kappa-cut: Maximum accepted kappa value (the default is 50)
- frame-cut: Minimum accepted frame (the default is 2000, but the omission of initial frames is trajectory dependent)
- h: Display the help message for the usage of the script

Example using TUTORIAL data: To predict the RMSDs of the models in the file 'Final_Cohort.csv' using HORNET's trained model, for an RNA of 268 residues, one would use:

```bash
python predict.py -d ../data/TUTORIAL/Final_Cohort.csv -m ../models/hornet -n 268
```

Outputs:
- Prediction file containing all structures (ordered by frame), with the prefix 'dataset_name_prediction' (e.g., Final_Cohort_prediction.csv).
- Prediction file containing only the top-10 scored structures (ordered by predicted RMSD), with the prefix 'dataset_name_Top10' (e.g., Final_Cohort_Top10.csv).

The typical running time on a normal computer is ~1 min for a dataset with ~1 million entries.


## IV. Other Included Utilties

### 1. Generating Coarse-grained PDB Coordinates for Selected Structures

The utility [outpdb](utilities/outpdb/) has been provided to extract the coarse-grained coordinates of the selected frames (.csv) from the their associated CafeMol trajectory files (.dcd). This script [Writepdb_Alltraj.py](utilities/outpdb/Writepdb_Alltraj.py) requires the python/conda package 'MDTraj' (https://anaconda.org/conda-forge/mdtraj):

```bash
pip install mdtraj
```

And the following lines of script must be modified accordingly: 

- file_name: Path to the data file containing the trajectory frame numbers to be extracted (e.g., Top10.csv)
- dcd_traj: Path to the folder containing all associated CafeMol binary files (.dcd), named as k*.dcd, where * is the kappa value (trajectory) associated with the selected frames. 
- ref: Reference coarse-grained PDB structure (e.g., initial PDB file used for dynamic fitting)

A modified example script with associated input files can be found in the [outpdb](utilities/outpdb/) directory, and the required .dcd file can be obtained [here](https://home.ccr.cancer.gov/csb/pnai/data/HorNet/tutorial/k30.dcd). Please, remember to download the dcd file and copy it to your current directory where the script Writepdb_Alltraj.py is located. With all required files placed in the same directory, the script can be run as follows:

```bash
python Writepdb_Alltraj.py
```

Outputs:
- The PDB coordinates for each specified frame are written as individual bead-models (three beads per residue).


### 2. Converting to All-atom Coordinates

For converting coarse-grained bead-models to all-atom coordinates, the utility [cg2aa](utilities/cg2aa) has been provided, which requires the package [XPLOR-NIH](https://nmr.cit.nih.gov/xplor-nih/) (free for academic users). The [cg2aa](utilities/cg2aa) directory contains example scripts, input files, and its own README file for using this utility.


## V. Training a Model

If one wants to train a model using data other than those used to train HORNET, the [train.py](scripts/train.py) script has been provided. Example data files for training and validation are also provided in [TUTORIAL](data/TUTORIAL): 'train_sample1.csv', 'train_sample2.csv' and 'validation_sample.csv'.

```bash
python train.py -o <output-directory> -d <dataset> -n <number-of-residues> \
                [-e <epochs>] [-k <kappa-cut>] [-f <frame-cut>] \
                [-v <validation>] [-vn <validation-residues>] \
                [-l <loss-function>] [-s <seed>] [-h]
```

Required Inputs:
- output-directory: Name given for the output directory that will be created to store the trained model (e.g., /HORNET/tree/main/models/mymodel).
- dataset: Array of dataset(s) to be used for training, separated by commas but without spaces between (e.g., ../data/TUTORIAL/train_sample1.csv,../data/TUTORIAL/train_sample2.csv).
- number-of-residues: Array of the number of RNA residues corresponding to each dataset, in the same order provided in the dataset array (e.g., sample1 and sample2 are both 268 residues, so one would use 268,268 for this argument).

Optional Inputs:
- validation: Dataset to be used for validation of the trained model (e.g., ../data/validation_sample.csv)
- validation-residues: Number of RNA residues corresponding to the validation dataset
- epochs: Maximum number of epochs to train the model
- kappa-cut: Maximum accepted kappa value (the default is 50)
- frame-cut: Minimum accepted frame (the default is 2000, but the omission of initial frames is trajectory dependent)
- loss-function: Loss function to be used to train the model. Accepts: 'huber' or 'mse'
- seed: Seed to maintain reproducible results across testing, use 0 for random
- h: Displays usage and help information for running the script

Outputs:
- A folder (named as defined in the argument) containing the trained model and configuration files for normalizations when using the model.

Example using TUTORIAL data:

To train the model using a single dataset "train_sample1.csv", with an output folder called "train_test" and a maximum of 10 epochs using huber loss (Note: HORNET was trained using a maximum of 300 epochs), one should call:

```bash
python train.py -o train_test \
                -d ../data/TUTORIAL/train_sample1.csv \
                -n 268 \
                -e 10 \
                -l huber
```

When available, a different RNA dataset should be used for validation. A sample of the validation dataset used to select the best epoch for HORNET is also provided for demonstration: [validation_sample.csv](data/TUTORIAL/validation_sample.csv). Note that the number of residues for this RNA (-vn) is 298. In this case, using the 2 sample datasets to train the model ("train_sample1.csv","train_sample2.csv") with the validation set as "validation_sample.csv", it would be:

```bash
python train.py -o train_test_val \
                -d ../data/TUTORIAL/train_sample1.csv,../data/TUTORIAL/train_sample2.csv \
                -n 268,268 \
                -v ../data/TUTORIAL/validation_sample.csv \
                -vn 298 \
                -e 10 \
                -l huber
```

The typical running time on a normal computer is ~1 min per epoch for a dataset with ~1 million entries.

## Citing HORNET
If HORNET helped your research, please cite:

```bibtex
@article{HORNETnature2025,
  author       = {Degenhardt, M. F. S. and Degenhardt, H. F. and and et al.},
  title        = {Determining structures of RNA conformers using AFM and deep neural networks},
  journal      = {Nature},
  volume       = {637},
  pages        = {1234--1243},
  year         = {2025},
  doi          = {10.1038/s41586-024-07559-x},
  url          = {https://doi.org/10.1038/s41586-024-07559-x}
}
```
```bibtex
@software{HORNETzenodo2024,
  author       = {Degenhardt, M. F. S. and Degenhardt, H. F. and and et al.},
  title        = {HORNET code - Holistic RNA Structure Determination},
  version      = {1.0.0},
  year         = {2024},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.10637777},
  url          = {https://doi.org/10.5281/zenodo.10637777}
```
