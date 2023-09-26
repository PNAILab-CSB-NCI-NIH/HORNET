## Inset the "TER" expression between two chains in PDB
## Usage: python3 chain_ter.py pdb_file
## output pdb filename is extended by the term "_fmt"

import sys
if len( sys.argv ) < 2:
    print("provide pdbfile")
    sys.exit()
pdb_file = sys.argv[1]
out_file = pdb_file.split(".")[0]+"_fmt.pdb"

## First find the first and last chain
with open(pdb_file,'r') as fin:
    chains = []
    for line in fin:
      if line.startswith("ATOM"):
        chain_id = line[19:22].strip()
        chains.append(chain_id)
    chain_first = chains[0]
    chain_last = chains[-1]
    #print(chain_first, chain_last)
    
## Introduce the TER keywork at the chain transition
with open(pdb_file,'r') as fin, open(out_file, 'w') as fout :
    flag = 0
    for line in fin:
      chain_id = line[19:22].strip()
      if (chain_id == chain_last and flag == 0):
        fout.write("TER"+"\n")
        flag = 1
      fout.write(line)
