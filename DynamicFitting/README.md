## Helper scripts for setting up and submitting CG-dynamic fitting runs

## Install (if desired) the CG-dynamic fitting CafeMol/3.2.0 software.

1. For dynamic fitting using AFM topography information is required to install CafeMol/3.2.0 software. Installation instruction and helper is available at https://www.cafemol.org/download/.
“CafeMol: A coarse-grained biomolecular simulator for simulating proteins at work. H. Kenzaki, N. Koga, N. Hori, R. Kanada, W. Li, K. Okazaki, XQ. Yao, and S. Takada Journal of Chemical Theory and Computation (2011) 7(6) pp1979-1989 DOI:10.1021/ct2001045”

2. If you desire to increase the maximum number of AFM pixel sizes to deal with larger images, you can enter into src folder inside Cafemol (version 3.2.0) directory, open the file const_maxsize.F90 and replace the number 1000 in line 142 to, for example, 500000:
- Line 141: integer, parameter :: CARRAY_MXLINE = 500000 !< maximum # of lines in one input-block

This modification was used in this current work, that allows the use of high resolution AFM images.  
 
3. Some scripts in this folder require to have installed Python/3.7 and R/4.0 to run

4. The usage of each script is explained in the protocol.txt file

However, the user can use its own way to run Cafemol and latter just follow the protocol for structure score and validation using HORNET. But, we recommend to use our scaling factor of the native information file (edit_ninfo_full.py). 

5. Folder templates has examples of files to use and run dynamic fitting procedure. 

	i) Generating CG and native-info file 
	
		$cd templates/monomer_ini
		${cafemol_path}/bin/cafemol.exe input.inp    
	ps. Before run, please, add into input.inp the complete path to root folder of Cafemol softwere at variable path_para 

	output files:
		$cd output 
			- File .pdb has the generated pdf files at step 0 and 10 written in a CG model, use your frame 0 as your reference structure for further calculation using AFM potential
			- File .ninfo contains all required native information that can be used as it is or as input to scaling  the force coefficients and add tertiary contacts. For more information read protocol file. 

	ii) Setting up the dynamic fitting input files using single particle AFM topography 
	
		$cd templates/make_inputfile_AFM
		$bash ../../calculation/make_cafeinput_monomer.sh afm_file.txt pdb_file.pdb ninfo_file.ninfo
	
	ps. Here you will need to have R/4.0 and posibly python/3.7

	output files:
		input_cafe.inp - input file to run cafe mol 
		Folders: pdb, ninfo and outut
			pdb: reference pdb and centered pdf into AFM image
			ninfo: native ninfo file that will be used as reference for dynamic fitting

	 For more information read protocol file. 

	iii) Performing a dynamic fitting 
	
		$cd templates/monomer_run 
		${cafemol_path}/bin/cafemol input.inp
	Ps. Before run, please, add into input.inp the complete path to root folder of Cafemol softwere at variable path_para. For this example case the kappa=12, however, for a complete analysis we strongly recommend to performed a kappa scan, running calculation with kappa in a range from 1 to 50, after that use HORNET for structure evaluation. Here as a axemple only 100 frames were setup to run, in a real case increase this value as nedeed.
	
	For more information read protocol file. 

	iv) For perform a kappa scan example into templates folder:
		$ cd templates/kappa_scan
		$ python folder_temp.py

	Ps. Modify file folder_temp.py adding the working directory full path to currently folder. The value of kappa is defined by kappa.txt file, to perform  the calculation with different kappa values it is just necessary modify the file kappa.txt, make sure not leave any empty line. 
	
	For more information read protocol file. 
