## Scale the cafemol input file by x,y,z values and submit runs based on new scaling
## Example: bash scan3D.sh "[0.9,1.1,0.05] [0.9,1.1,0.05] [200,1000,25] 10 k1"

###############################################################################
# Help                                                                         #
################################################################################
Help()
{
   # Display Help
   echo "Generate copies of a template folder to run cafemol runs at various XY and Z scale factors and kappa values"
   echo "and submit all the runs"
   echo
   echo "Usage: "
   echo "      bash scan3D.sh '[x1,x2,dx] [z1,z2,dz] [k1,k2,dk] c templt_folder'"
   echo 
   echo "      x1,x2,dx              x1,x2 lower and upperbound for scale factor for x and y direction, dx is the increment interval"
   echo "                            both x and y pixel coordinates are scaled by the same amount"
   echo "      z1,z2,dz              z1, z2 are lower and upperbound for scale factor for z direction, dz is the increment interval"
   echo "      k1,k2,dk              k1, k2 are lower and upperbound for kappa values, dk is the kappa increment interval"
   echo "      c                     cutoff value for z, z values are first scaled and any scaled value of z below cutoff is set to 0"
   echo "      templt_folder         template folder that has a complete set up for the cafemol run"
   echo 
   echo "      This script also generates a file called scan3Dlist.txt that contain all combinatios of xy and z scale factors and kappa values"
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

cmd_args=$1

## Parse the arguments
arrIN=(${cmd_args// / })
scaleRange_xy=${arrIN[0]}
scaleRange_z=${arrIN[1]}
scaleRange_k=${arrIN[2]}
cutoff_z=${arrIN[3]}
tmpl_folder=${arrIN[4]}

scaleRange_xy="${scaleRange_xy#*\[}"
scaleRange_xy="${scaleRange_xy%\]*}"
scaleRange_xy=(${scaleRange_xy//,/ })
interval_xy=$(echo "${scaleRange_xy[1]}-${scaleRange_xy[0]}"|bc)
N_xy=$(echo "$interval_xy/${scaleRange_xy[2]}"|bc)
start_xy=${scaleRange_xy[0]}

scaleRange_z="${scaleRange_z#*\[}"
scaleRange_z="${scaleRange_z%\]*}"
scaleRange_z=(${scaleRange_z//,/ })
interval_z=$(echo "${scaleRange_z[1]}-${scaleRange_z[0]}"|bc)
N_z=$(echo "$interval_z/${scaleRange_z[2]}"|bc)
start_z=${scaleRange_z[0]}

scaleRange_k="${scaleRange_k#*\[}"
scaleRange_k="${scaleRange_k%\]*}"
scaleRange_k=(${scaleRange_k//,/ })
interval_k=$(echo "${scaleRange_k[1]}-${scaleRange_k[0]}"|bc)
N_k=$(echo "$interval_k/${scaleRange_k[2]}"|bc)
start_k=${scaleRange_k[0]}

#echo $interval_xy $N_xy
#echo $interval_z, $N_z
#echo $interval_k, $N_k

rm -rf "scan3Dlist.txt"

for i in $(eval echo "{0..$N_xy}")
do
  ## start of second nested loop
  for j in $(eval echo "{0..$N_z}")
  do
    ## start of third nested loop
    for k in $(eval echo "{0..$N_k}")
    do
      ## echo $start_xy $start_z $start_k
      folder_name="xy"$start_xy"_z"$start_z"_k"$start_k
      echo $folder_name >> "scan3Dlist.txt"
      if [[ $tmpl_folder != $folder_name ]]; then
        rm -rf $folder_name
        cp -r $tmpl_folder $folder_name
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
        kappa_result=$(echo "scale=4;$start_k*$no_of_particles*0.001987*298" | bc)
        #echo $kappa_result 
        #echo $no_of_particles
        python $analysisPath"/calculation/edit_kappa.py" input.inp $start_k $kappa_result $no_of_particles
        mv -f temp_cafe.inp input.inp
        Rscript $analysisPath"/analysis/scaleAFM_XY_CafeInput.R" "input.inp" [$start_xy,$start_xy,$start_z] $cutoff_z
        mv -f input_scaled.inp input.inp  ## rename the new input file made by Rscript to original name
        cd ../

      fi
      start_k=$(echo "$start_k + ${scaleRange_k[2]}"|bc)
    done
    ## endo of third nested loop
    start_k=${scaleRange_k[0]}
    start_z=$(echo "$start_z + ${scaleRange_z[2]}"|bc) 
  done
  ## end of second nested loop

  #start_k=${scaleRange_k[0]}
  start_z=${scaleRange_z[0]}
  start_xy=$(echo "$start_xy + ${scaleRange_xy[2]}"|bc)

done



