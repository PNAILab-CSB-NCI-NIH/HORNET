#!/bin/sh

#number of bead models to convert to all-atom for each slurmXplor job
beadsPerJob=30

#bead files to convert (the files must not have the same name)
beadFilenameList=$1

scriptName=toAllAtom
scriptFile=$(readlink -f {path}/aa_conv/${scriptName}.py)  #### Full path to toAllAtom.py script

#put all bead files (and log files) in this directory
runDir=allAtom

mkdir -p $runDir

# A set of initial coordinates
# it is best if this file isn't missing any atoms and has satisfied 
# covalent geometry
allAtomInitFile=$(readlink -f {path}/aa_conv/rna_ini-allatom_good.pdb)   ###good covalent geometry (Run genDist.py using pyXplor to generate rna_ini-allatom_good.pdb file)
#File containing base-pairing definitions
bplFile=$(readlink -f /data/PNAI/Maximilia/scripts/aa_conv/FLRnaseP/FLRNaseP.bpl)       ####Path and file to bplFile


submitJobCommand="$scriptFile \
	          -allAtomInitFile $allAtomInitFile \
	          -bplFile $bplFile "
#submitJobCommand="echo $submitJobCommand"

if ! [ -f "$beadFilenameList" ]; then
    echo "must specify a file containing bead filenames"
    exit 1
fi

export PATH=/data/schwitrs/xplor-nih-3.5.1/bin:$PATH

submitCount=0
submitList=""
jobCount=0
for beadFilename in $(cat $beadFilenameList); do
    if ! [ -f "$beadFilename" ]; then
	echo "file $beadFilename does not exist"
	continue
    fi
    if [ "$submitList" = "" ]; then
	submitList="$beadFilename"
    else
	submitList="${submitList}:$beadFilename"
    fi
    submitCount=$(expr $submitCount + 1)
    if [ $submitCount -ge $beadsPerJob ]; then
	jobName=${scriptName}-${jobCount}
	(cd $runDir; \
	    $submitJobCommand -o ${jobName}.out -N $jobName \
	    -beadFile "$submitList")
	submitList=""
	submitCount=0
	jobCount=$(expr $jobCount + 1)
    fi
done

#leftover bead files:
jobName=${scriptName}-${jobCount}
[ "$submitList" = "" ] || (cd $runDir; \
    $submitJobCommand -o ${jobName}.out -N $jobName \
    -beadFile "$submitList")
