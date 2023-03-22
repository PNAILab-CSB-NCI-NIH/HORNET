
#read starting PDB, add unknown atoms, and fix up covalent geom, write out
# resulting PDB

inputPDB="rna_ini-allatom.pdb"
import protocol
protocol.loadPDB(inputPDB)


import regularize
regularize.addUnknownAtoms_new()

from regularize import fixupCovalentGeom
fixupCovalentGeom()

import os
base,ext = os.path.splitext(inputPDB)

protocol.writePDB(base+"_good.pdb")
