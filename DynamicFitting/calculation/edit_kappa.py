#### Edit cafemol input file for kappa values
### Usage: $ python3 edit_kappa.py cafemol_inputfile kappa_value kappa_result
### kappa_result is the final calculation using kappa and other parameters
import sys
import fileinput

if len( sys.argv ) !=  5:
    print("provide cafemol_input_file, kappa, kappa result, and number of particles")
    sys.exit()

input_file = sys.argv[1]
kappa = sys.argv[2]
kappa_result = sys.argv[3]
num_particles = sys.argv[4]
out_file = "temp_cafe.inp"
with open(input_file,'r') as fin, open(out_file, 'w') as fout :
    flag1 = 0
    for line in fin:
        if line.startswith("<<<< afm_fitting"):
            flag1 = 1
            fout.write(line)
        elif (flag1 == 1 and line.startswith("** Strength ")):
            line_string = "** Strength of the potential; k=kappa*N*kB*T=" + kappa + "*" + num_particles + "*0.001987*298"
            fout.write(line_string+"\n")
        elif (flag1 == 1 and line.startswith("k ")):
            line_string = "k       =  " + kappa_result
            fout.write(line_string+"\n")
            flag1 = 0
        else:
            fout.write(line)
