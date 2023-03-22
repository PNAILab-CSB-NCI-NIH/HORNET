## Helper scripts for setting up and submitting  CG-dynamic fitting runs

## Install (if desire) the CG-dynamic fitting CafeMol/3.2.0 software.

1. For dynamic fitting using AFM topography information is required to install CafeMol/3.2.0 software. Installation instruction and helper is available at https://www.cafemol.org/download/.
“CafeMol: A coarse-grained biomolecular simulator for simulating proteins at work. H. Kenzaki, N. Koga, N. Hori, R. Kanada, W. Li, K. Okazaki, XQ. Yao, and S. Takada Journal of Chemical Theory and Computation (2011) 7(6) pp1979-1989 DOI:10.1021/ct2001045”

2. If you desire to increase the maximum number of AFM pixel sizes to deal with larger images, you can enter into src folder inside Cafemol (version 3.2.0) directory, open the file file const_maxsize.F90 and replace the number 1000 in line 142 to, for example, 500000:
- Line 141: integer, parameter :: CARRAY_MXLINE = 500000 !< maximum # of lines in one input-block
 
3. Some scripts in this folder require to have installed Python/3.7 and R/4.0 to run

4. The usage of each script is explained in the protocol.txt file
