Converting coarse-grained structures to corresponding all-atom versions

Requires installed the program Xplor-NIH version 3.5, or newer

input files:
  One or more RNA structures in coarse-grained (three-bead per residue) 
  representation.

  In addition to the coarse-grained structure, base-pairing
  information must be provided in a .bpl file, any program that recognize base-pair interactions can be used to generate the file (example file model_file.bpl)

  This calculation is much faster if an input all-atom model is
  present, having good covalent geometry.

Ps. The all-atom refined model with goo covalent geometry can be generated using the script genIni.py
	Input: all-atom model - file name: rna_ini-allatom.pdb
	output: rna_ini-allatom_good.pdb

	Example:
		pyXplor genIni.py rna_ini-allatom.pdb
	

outputs:
  For each input coarse-grain model, an output all-atom PDB is written
  in the current directory whose filename has the suffix "_aa"
  added to the root (non-extension) portion of the corresponding input
  coarse-grain filename. For example, an input file named bead.pdb
  would generate an all-atom representation file named bead_aa.pdb.

Below is a sample program invocation, with the names of input files
specified in angle brackets.

xplor toAllAtom.py \
       -allAtomInitFile <all-atom PDB filename> \
       -bplFile <.bpl filename> \
       <bead PDB> ... \
       -o toAllAtom.out

Example:
	xplor toAllAtom.py -allAtomInitFile rna_ini-allatom_good.pdb -bplFile model_file.bpl k50Model_7041.pdb -o toAllAtom.out

##### Convert all atom model to Cafemol format 
  Usage:
    ./format_pdb_xplor.sh <path_to_pdb_folder> 

Inputs:
  path_to_pdb_folder: path to the folder with desire all atom pdb to be convert to Cafemol reading format 
Outputs:
	A folder named FMT_PDB/ is created if all pdb files in the <path_to_pdb_folder> directory whose filename has the suffix "_fmt"