#!/usr/bin/env pyXplor

import protocol
opts,args=xplor.parseArguments([
    ("allAtomInitFile","filename",
     """file with initial atomic coordinates. Execution is fastest if
     this is created using Xplor-NIH and contains coordinates for all 
     atoms and covalent geometry is correct."""),
    ("beadFile","filename","""A file which can be colon-separated list of 
    PDB-formatted files with coarse-grained bead coordinates, or can be the 
    name of a file contain one bead filename per line."""),
    ("bplFile","filename","""name of .bpl file containing the base-pairing 
    information""")])

inputPDB=None
beadFilename=None
bplFilename=None
for opt in opts:
    if opt[0]=="allAtomInitFile": inputPDB=opt[1]
    if opt[0]=="beadFile": beadFilename=opt[1]
    if opt[0]=="bplFile": bplFilename=opt[1]
    pass

import os
if not (inputPDB and os.path.exists(inputPDB)):
    print("The -allAtomInitFile option must be specified with an existing "
          "file as the argument.")
    exit(1)
    pass
if not beadFilename:
    print("The -beadFile option must be specified.")
    exit(1)
    pass
if not (bplFilename and os.path.exists(bplFilename)):
    print("The -bplFile option must be specified.")
    exit(1)
    pass

from pdbTool import PDBTool
if ":" in beadFilename:
    beadFilenames=beadFilename.split(':')
else:
    if not os.path.exists(beadFilename):
        print(f"-beadFile {beadFilename} does not exist")
        exit(1)
        pass

    if PDBTool(beadFilename).format()=="PDB":
        beadFilenames = [beadFilename ]
    else:
        beadFilenames=[]
        for name in open(beadFilename).readlines():
            name=name.strip()
            if name[0] == '#':
                continue
            pass
        beadFilenames.append( name )
        pass
    pass

for name in beadFilenames:
    if not os.path.exists(name):
        print(f"file {name} listed in {beadFilename} does not exist.")
        exit(1)
        pass
    if PDBTool(name).format()!="PDB":
        print(f"file {name} listed in {beadFilename} is not in PDB format.")
        exit(1)
        pass
    pass

    
protocol.loadPDB(inputPDB)

import regularize
regularize.addUnknownAtoms_new()

#protocol.writePDB("allAtom.pdb")

#
from potList import PotList
potList = PotList()
crossTerms=PotList('cross terms')
startStructure = 0
#
# Lists highTempParams and rampedParams will hold simulationTools.StaticRamp and
# simulationTools.MultRamp objects to handle parameter changes between the high
# termperature and annealing stage, and within the annealing stage (e.g., ramped
# force constants).
#
from simulationTools import StaticRamp, MultRamp, InitialParams, AnnealIVM

highTempParams = []
rampedParams = []


from globDiffPotTools import create_GlobDiffPot
#
globDiff = create_GlobDiffPot('globDiffA',
                              selection="all",
                              useChainID=True,
                              globFilename=beadFilenames[0],
                              globMap=[("name P","name P"),
                                       ("name C1' C2' C3' C4' O4'","name S"),
                                       ("resname ADE and name N1", "name Ab"),
                                       ("resname GUA and name N1", "name Gb"),
                                       ("resname CYT and name N3", "name Cb"),
                                       ("resname URI and name N3", "name Ub"),
                                       ])

globDiff.setThreshold(0.5)
globDiff.setUpperBound(0.1)
globDiff.setScale(3)
potList.append( globDiff )


from regularize import fixupCovalentGeom
#assumed to be good covalent geom
#fixupCovalentGeom()
#if xplor.p_processID==0:
#    protocol.writePDB("start.pdb")
#    pass                              

from posDiffPotTools import create_PosDiffPot
refRMSD = create_PosDiffPot("refRMSD","not name H*",
                            pdbFile=inputPDB,
                            cmpSel="not name H*")
refRMSD.setUpperBound(2)
refRMSD.setScale(10)
crossTerms.append(refRMSD)

#
# Set up distance restraint potential (e.g., from NOEs).
#
import noePotTools
noe = PotList('noe')

def readDuplexes(filename):
    """Return list of tuples containing pairs of resids of paired bases.
    """
    lines=open(filename).readlines()
    inHelicalSegment=False
    import string
    pairs=[]
    for line in lines:
        if (line.startswith('$ bplist')):
            inHelicalSegment=True
            pass

        if inHelicalSegment and line[0] in string.digits:
            pairs.append( [int(s) for s in line.split()] )
            #print(pairs)
            pass


        pass
    #ret.append(pairs)
    return pairs

def genRestraints(pairs,
                  dist=3.,
                  deltaLess=1.5,
                  deltaPlus=0.,
                  selTemplate=r"resid %d and not name H* and not name *'"
                  ):
    """
    From a list of pairs of residue numbers, generate a restraint table using
    the given selTemplate for each residue, and an allowed distance range of
    dist-deltaLess ... dist+deltaPlus.

    """
    ret =""
    for a,b in pairs:
        asel = selTemplate % a
        bsel = selTemplate % b
        ret += "assign (%s) (%s) %f %f %f\n" % (asel,bsel,
                                                dist,deltaLess,deltaPlus)
        pass
    return ret


basePairResids = readDuplexes(bplFilename)

restraints = genRestraints(basePairResids)
pot = noePotTools.create_NOEPot('bpDist', restraints=restraints)
noe.append(pot)

potList.append(noe)
rampedParams.append(MultRamp(2, 30, "noe.setScale(VALUE)"))

#
# Set up potential for base-pair planarity restraints.
#
from xplorPot import XplorPot
#protocol.initPlanarity('plane.tbl')
#potList.append(XplorPot('PLAN'))
# (The setup of this term remains unchanged throughout; no need to involve
# highTempParams and/or rampedParams.)


#
# Set up potential for base-pair planarity restraints.
#
protocol.initPlanarity(basePairs=basePairResids)
potList.append(XplorPot('PLAN'))
# (The setup of this term remains unchanged throughout; no need to involve
# highTempParams and/or rampedParams.)


#
# Setup parameters for atom-atom repulsive term (van der Waals-like term).
#
from repelPotTools import create_RepelPot,initRepel
repel = create_RepelPot('repel')
potList.append(repel)
rampedParams.append( StaticRamp("initRepel(repel,use14=False)") )
rampedParams.append( MultRamp(.004, 4, "repel.setScale( VALUE)") )
# nonbonded interaction only between C1' atoms
highTempParams.append( StaticRamp("""initRepel(repel,
                                               use14=True,
                                               scale=0.004,
                                               repel=1.2,
                                               moveTol=45,
                                               interactingAtoms="name C1'"
                                               )""") )
#
# Set up statistical torsion angle potential (torsionDB).
#
from torsionDBPotTools import create_TorsionDBPot
torsiondb = create_TorsionDBPot(name='torsiondb',system='rna')
potList.append(torsiondb)
rampedParams.append(MultRamp(0.5, 4, "torsiondb.setScale(VALUE)"))


# Selected 1-4 interactions.
# ---
# 1-4 interactions are ommited from the above term (repel) because they are
# mostly affected by torsionDB (torsiondb).  However, torsionDB doesn't affect
# torsions of terminal, protonated groups (e.g., methyl rotation).  Thus, 1-4
# interactions involved in such torsions are set up here.  (Note: a more elegant
# solution might be implemented in the near future.)
#
from torsionDBPotTools import create_Terminal14Pot
repel14 = create_Terminal14Pot('repel14')
potList.append(repel14)
highTempParams.append(StaticRamp("repel14.setScale(0)"))
rampedParams.append(MultRamp(0.004, 4, "repel14.setScale(VALUE)"))



#
# Set up bond length potential.
# (Needed even if no Cartesian minimization is used, for "broken" rings.)
#
bond = XplorPot('BOND')
potList.append(bond)
# (The setup of this term remains unchanged throughout; no need to involve
# highTempParams and/or rampedParams.)


#
# Set up bond angle potential.
# (Needed even if no Cartesian minimization is used, for "broken" rings.)
#
angl = XplorPot('ANGL')
potList.append(angl)
rampedParams.append(MultRamp(0.4, 1.0, "potList['ANGL'].setScale(VALUE)"))

#
# Set up improper dihedral angle potential.
# (Needed even if no Cartesian minimization is used, for "broken" rings.)
#
impr = XplorPot('IMPR')
potList.append(impr)
rampedParams.append(MultRamp(0.1, 1.0, "potList['IMPR'].setScale(VALUE)"))


#
# Set up statistical base-base positional potential.

# In general, however, all RNA residues should be selected (e.g.,
# for an isolated RNA molecule use selection='all').
# Reference: Clore, GM & Kuszewski, J, (2003) J. Am. Chem. Soc. 125:1518-1525.
#
#FIX: add pairs?
#protocol.initOrie(system='rna', selection='all',
#                  distCutoff=15 #  will speed things up considerably - supported
#                  #               in Xplor-NIH versions 3.2.2 and up.
#                  )
#
#potList.append(XplorPot('ORIE'))
#rampedParams.append(MultRamp(0.002,0.3,"xplor.command('orie scale VALUE end')"))

xplor.fastCommand("param hbonds print=false end end")
potList.append(XplorPot('HBON'))
potList['HBON'].setScale(1.0)



#
# Done with energy terms.

#
# Give atoms uniform weights, except for anisotropy axes (if any).
#
protocol.massSetup()


#
# Set up IVM object(s).
#

# IVM object for torsion-angle dynamics/minimization.
import ivm
dyn = ivm.IVM()


# Argument flexRiboseRing below is a string that selects residues whose ribose
# rings will have all endocyclic angles flexible.  In general, all ribose rings
# should be selected.  In this example, the non-RNA ligand (residue 34) has to
# be excluded.
protocol.torsionTopology(dyn, flexRiboseRing='all')

## Optional IVM object for final Cartesian minimization.
minc = ivm.IVM()
##
##for tensor in tensors.values():
##    tensor.setFreedom("varyDa, varyRh") # allow all tensor parameters float here
##
protocol.cartesianTopology(minc)



#
# Temperature set up.
#
temp_ini = 1500.0   # initial temperature
temp_fin = 25.0     # final temperature


potListWoutOrie=[term for term in potList if term.instanceName()!='ORIE']

def calcOneStructure(loopInfo):
    """ this function calculates a single structure, performs analysis on the
    structure, and then writes out a pdb file, with remarks.
    """

    beadNum = loopInfo.structNum
    beadFilename = beadFilenames[beadNum]
    path,basename = os.path.split(beadFilename)
    name,ext = os.path.splitext(basename)
    loopInfo.pdbTemplate=name+"_aa.pdb" #name for output PDB.

    from atomSel import AtomSel
    protocol.initCoords(beadFilename,
                        erase=True,
                        selection=atomSel.AtomSel("all",
                                                  globDiff.xsim))
    if len( AtomSel("not known") ) > 0:
        raise Exception(f"There are unknown bead atoms in {beadFilename}.")
    

    # initialize parameters for high temp dynamics.
    InitialParams( rampedParams )
    # high-temp dynamics setup - only need to specify parameters which
    #   differfrom initial values in rampedParams
    InitialParams( highTempParams )

    protocol.initMinimize(minc,
                          potList=[globDiff,bond,angl,impr],
                          numSteps=1000,   
                          printInterval=100)

    minc.run()

    protocol.initMinimize(minc,
                          potList=[globDiff,bond,angl,impr,repel],
                          numSteps=500,   
                          printInterval=100)

    minc.run()

    protocol.initMinimize(minc,
                          potList=[globDiff,bond,angl,impr,repel,noe],
                          numSteps=500,   
                          printInterval=100)

    minc.run()

    protocol.initMinimize(minc,
                          potList=potList,
                          numSteps=500,   
                          printInterval=100)

    minc.run()


#
#
#    # high temp dynamics
#    #
#    protocol.initDynamics(dyn,
#                          potList=potList, # potential terms to use
#                          bathTemp=temp_ini,
#                          initVelocities=1,
#                          finalTime=5,    # stops at 150ps or 15000 steps
#                          numSteps=3000,   # whichever comes first
#                          printInterval=100)
#
#    dyn.setETolerance( temp_ini/100 )  #used to det. stepsize. default: t/1000 
#    dyn.run()
#
#    # initialize parameters for cooling loop
#    InitialParams( rampedParams )
#
#
    # initialize integrator for simulated annealing
    #
    protocol.initMinimize(minc,
                          potList=potList,
                          numSteps=50,       #at each temp: 400 steps or
                          printInterval=10)

    # perform simulated annealing
    #
    AnnealIVM(initTemp=temp_ini,
              finalTemp=temp_fin,
              tempStep=200,
              ivm=minc,
              rampedParams=rampedParams).run()
#              
#    # final torsion angle minimization
#    #
#    protocol.initMinimize(dyn,
#                          printInterval=50)
#    dyn.run()
#
#    # final all- atom minimization
    #
    protocol.initMinimize(minc,
                          potList=potList,
                          dEPred=10)
    minc.run()

    pass



from simulationTools import StructureLoop, FinalParams
StructureLoop(numStructures=len(beadFilenames),
              doWriteStructures=True,
              startStructure=startStructure,
              structLoopAction=calcOneStructure,
              genViolationStats=False,
              averagePotList=potList,
#              averageSortPots=[potList['BOND'],potList['ANGL'],potList['IMPR'],
#                               noe,rdcs,potList['CDIH']],
              averageCrossTerms=crossTerms,
              averageContext=FinalParams(rampedParams),
              #averageFilename="SCRIPT_ave.pdb",    #generate regularized ave structure
              averageFitSel="name P",
              averageCompSel="not PSEUDO and not name H*"     ).run()

