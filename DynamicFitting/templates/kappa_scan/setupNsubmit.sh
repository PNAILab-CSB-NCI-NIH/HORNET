## Sets up the various kappa directories and submit each run
## Usage: bash setupNsubmit.sh template_directory  kappa.txt  
## k1, k2, k3 are kappa values
## kappa.txt file should not have empty lines on the end of file

###############################################################################
# Help                                                                         #
################################################################################
Help()
{
   # Display Help
   echo "Generate copies of a template folder to run cafemol runs at various kappa values"
   echo "and submit all the runs"
   echo
   echo "Usage: "
   echo "      bash setupNsubmit.sh template_directory kappa.txt"
   echo 
   echo "      template_directory    template folder that has a complete set up for the cafemol run"
   echo "      kappa.txt             file with column of kappa values"
   echo 
   echo "      example of kappa.txt is given at scripts_path/calculation/"
   echo "      please remove any empty lines at the end of file in kappa.txt"
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

tmpl_folder=`basename $1`
echo "The template folder is: " $tmpl_folder

## parse the list of kappa values 
kfile=$2
while IFS= read -r line
do
  #echo "kappa value read is:" $line
  folder_name="k"$line
  if [[ $tmpl_folder != $folder_name ]]; then
    rm -rf $folder_name
    cp -r $tmpl_folder $folder_name
  fi  
  cd $folder_name
  rm -rf "output"
  mkdir "output"
  echo "currently working in directory: " $(pwd)
  ## extract the number_of_particles info from the input file
  group=`grep "GROUP" input.inp`
  arrGroup=($(echo $group | tr "-" "\n"))
  item_group=${arrGroup[2]}
  no_of_particles="${item_group::-1}"
  ## edit kappa value in the cafemol input file
  kappa_result=$(echo "scale=4;$line*$no_of_particles*0.001987*298" | bc)
  #echo $kappa_result 
  #echo $no_of_particles
  python $analysisPath"/calculation/edit_kappa.py" input.inp $line $kappa_result $no_of_particles
  mv -f temp_cafe.inp input.inp
  cd ../

done <$kfile

