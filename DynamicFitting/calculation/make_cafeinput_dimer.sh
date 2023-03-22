###############################################################################
# Help                                                                         #
################################################################################
Help()
{
   # Display Help
   echo "Prepare the cafemol input file"
   echo
   echo "Usage: "
   echo "      bash make_cafeinput_dimer.sh afm_file cg_pdb_file ninfo_file"
   echo 
   echo "      afm_file         afm data file from MountainSPIP"
   echo "      cg_pdb_file      CG model of PDB obtained from allatom to cg calculation"
   echo "      ninfo_file       native info file from allatom to cg conversion calculation"
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

module load R/4.0
module load python/3.5
afm_file=$1
pdb_file=$2
ninfo_file=$3

afm_base=`basename ${afm_file%.*}`
pdb_base=`basename ${pdb_file%.*}`
pdb_path=`readlink -f $pdb_file`
ninfo_path=`readlink -f $ninfo_file`
pdb_name=`basename $pdb_path`
ninfo_name=`basename $ninfo_path`
#ninfo_dir=${ninfo_path%/*}
currentPDBname="input_cg.pdb"
currentNINFOname="input.ninfo"
echo $afm_base
#echo $pdb_path
#echo $ninfo_path
mkdir -p "pdb" && cp $pdb_path $_
mkdir -p "ninfo" && cp $ninfo_path $_
mkdir -p "output"

## First format the afm data
echo "Now formatting the afm data"
Rscript $analysisPath"/calculation/process_afm_init.R" $afm_file
echo "Now padding the afm data with a default padding of 1"
python $analysisPath"/calculation/molecule_padding.py" 1 $afm_base"_init.txt"
echo "Now merging the afm data with the header"
Rscript $analysisPath"/calculation/process_afm_final.R" "padded_"$afm_base"_init.txt" $analysisPath"/templates/dimer_header.txt" 
echo "Now editing the path for output, pdb and ninfo"
python $analysisPath"/calculation/edit_inputpath.py" "cafe_input.inp" ./output ./pdb $PWD/ninfo
rm -rf "cafe_input.inp"
cafe_file="input_cafe.inp"
echo "Now recentering the CG model with respect ot the afm image coordinates"
Rscript $analysisPath"/calculation/process_pdb_cg_recenter.R" ./pdb/$pdb_name $cafe_file
python $analysisPath"/calculation/chain_ter.py" $pdb_base"_center.pdb"
mv $pdb_base"_center_fmt.pdb" ./pdb
rm -rf $pdb_base"_center.pdb"
pdb_recenter=$pdb_base"_center_fmt.pdb"
## replace the input pdb name in the cafemol input file
sed -i "s/$currentPDBname/$pdb_recenter/g" $cafe_file
sed -i "s/$currentNINFOname/$ninfo_name/g" $cafe_file

