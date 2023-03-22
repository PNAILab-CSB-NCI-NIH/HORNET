
## regularizes bond, angle and improper terms, not allowing significant motion of the P atoms
## Usage: xplor regularize.py FILE.pdb > regularize.out
## where you specify FILE.pdb. The regularized structure is written to FILE.pdb.out

opts,args=xplor.parseArguments()

file=args[0]

import protocol
protocol.loadPDB(file,deleteUnknownAtoms=True)

from potList import PotList
potList = PotList()

from xplorPot import XplorPot

for term in "BOND ANGL IMPR".split():
    potList.append( XplorPot(term) )
    pass

from posDiffPotTools import create_PosDiffPot
ncs = create_PosDiffPot('ncs',"name P*","initial")


from simulationTools import analyze

print( analyze( potList ) )


from simulationTools import minimizeRefine
minimizeRefine(ncs)

print( analyze( potList ) )

protocol.writePDB(file+"_ref.pdb")
