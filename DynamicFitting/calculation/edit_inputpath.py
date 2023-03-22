#### Edit cafemol input file for path and md step
#### Usage: $ python3 edit_input.py input_file output_path pdb_path
#### given input file is edited in place.

import sys
import fileinput

if len( sys.argv ) < 5:
    print("provide cafe_inputfile, output_path, pdb_path, ninfo_path")
    sys.exit()

input_file = sys.argv[1]
output_path = sys.argv[2]
pdb_path = sys.argv[3]
ninfo_path = sys.argv[4]
out_file = "input_cafe.inp"
with open(input_file,'r') as fin, open(out_file, 'w') as fout :
    for line in fin:
        if line.startswith("path "):
            line_string = "path = "+output_path
            fout.write(line_string+"\n")
        elif line.startswith("path_pdb"):
            line_string = "path_pdb = "+pdb_path
            fout.write(line_string+"\n")
        elif line.startswith("path_ini"):
            line_string = "path_ini = "+pdb_path
            fout.write(line_string+"\n")
        elif line.startswith("path_natinfo"):
            line_string = "path_natinfo = "+ninfo_path
            fout.write(line_string+"\n")
        elif line.startswith("i_run_mode"):
            line_string = "i_run_mode = 2"
            fout.write(line_string+"\n")
        else:
            fout.write(line)
