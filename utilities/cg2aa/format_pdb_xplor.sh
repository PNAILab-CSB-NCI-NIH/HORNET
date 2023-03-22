## Use Xplor-NIH pdb2ens script to format pdbs
## convert from Xplor-NIH refinement outputs to standard PDB format

## Usage: bash format_pdb_xplor.sh path_to_pdbs
###############################################################################
# Help                                                                         #
################################################################################
Help()
{
   # Display Help
   echo "convert PDBs generated from Xplor-NIH refinement to standard PDB format"
   echo
   echo "Usage: "
   echo "      bash format_pdb_xplor.sh path_to_pdbs"
   echo 
   echo "      path_to_pdbs    folder containging the PDB files"
   echo "      A new folder 'FMT_PDB' is created inside the given path, that contains the formatted PDBs"
   echo
}
# Get the options
while getopts ":h" option; do
   case $option in
      h) # display Help
         Help
         exit;;
   esac
done
# While no arguments
if [[ $# -eq 0 ]] ; then
    Help
    exit 0
fi

cd $1
fmt_dir="FMT_PDB"
## remove the directory if it exists
if [ -d $fmt_dir ]; then rm -Rf $fmt_dir; fi
mkdir $fmt_dir
FileList=`ls *.pdb`

## Loop through each pdb and change the format
for name in $FileList
do
  echo "working on $name"
  pdb_base=`basename ${name%.*}`
  pdb_out=$pdb_base"_fmt.pdb"
  #echo $pdb_out
  ens2pdb -delete 'name H*' $name > $fmt_dir"/"$pdb_out 
done

