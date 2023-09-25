#### Edit ninfo file with given weight factors
#### Usage: $python remove_contacts_ninfo.py  "A:1-20,B:30-40" test.ninfo cg.pdb 
#### list order of scale factors [bond, angle, dihedral_1, dihedral_2,long_range, basepair, basestack]
#### Value of each scale factor range (0:9)
#### a new ninfo file is produced with a name ninfo_file_mod

import sys
from configparser import ConfigParser

def usage():
  print("Usage:")
  print('python remove_contacts_ninfo.py  "A:1-20,B:30-40" ninfo_file cg_pdbfile\n')
  print("In above example we choose chain A with residues 1 thr 20, and chain B with resiudes 30 thr 40, the script will remove all long range restraints between each of these groups and rest of the molecule.")

def scale_Coef(input_file, out_file, chains_in, resids, pdb_name):
  with open(pdb_name,'r') as fin:
      chains = []
      for line in fin:
        if line.startswith("ATOM"):
          chain_id = line[19:22].strip()
          chains.append(chain_id)
      #print(set(chains))
      unique_chainids = sorted(set(chains)) ## sort based on chain A, B etc
      resi_per_chain = len(chains)/len(unique_chainids)
      atoms = get_atomName(pdb_name)
      particle_resids = []
      for res_group in resids:
        if atoms[0] == "P":
          num_list1 = [(3*(y-1)+1) for y in res_group]
          num_list2 = [(3*(y-1)+2) for y in res_group]
          num_list3 = [(3*(y-1)+3) for y in res_group]
          particle_resids.append(num_list1+num_list2+num_list3)
        if atoms[0] == "S":
          num_list1 = [(3*(y-1)) for y in res_group if y != 1]
          num_list2 = [(3*(y-1)+1) for y in res_group]
          num_list3 = [(3*(y-1)+2) for y in res_group]
          particle_resids.append(num_list1+num_list2+num_list3)
      #print(particle_resids)
      #print(resi_per_chain) 
      #print(chains_in)
      chain_dict = {"A":1, "B":2}
      all_resids = list(range(1,int(resi_per_chain)+1))
  with open(input_file,'r') as fin, open(out_file, 'w') as fout :    
    for line in fin:
        if line.startswith("contact"):
            item1_list = [line.split()[0]]
            item2_list = [item.rjust(7) for item in line.split()[1:8]]
            item3_list = [item.rjust(13) for item in line.split()[8:10]]
            item4_list = [item.rjust(7) for item in line.split()[10]]
            item5 = '%.4f'% (float(line.split()[11]))
            item5_list = [item5.rjust(13)]
            item6_list = [line.split()[12].rjust(4)]
            sum_list = item1_list+item2_list+item3_list+item4_list+item5_list+item6_list
            sum_string = "".join(sum_list)
            ## define the condition for removing the given sets of residues
            chain_A, chain_B = line.split()[2], line.split()[3]
            res_i, res_j = int(line.split()[6]), int(line.split()[7])
            #print(res_i, res_j)
            flag = 0
            for rank in range(len(particle_resids)):
              chain_id = chain_dict[chains_in[rank]]
              complement_list = list(set(all_resids) - set(particle_resids[rank]))
              #print(particle_resids[rank])
              #print(complement_list)
              if (chain_A == str(chain_id) and chain_B == str(chain_id)):
                if (res_i in particle_resids[rank] and res_j in complement_list):
                   flag = 1
              elif (chain_A == str(chain_id) and chain_B == str(chain_id)):
                if (res_i in complement_list and res_j in particle_resids[rank]):
                   flag = 1
              elif (chain_A == str(chain_id) and chain_B != str(chain_id)):
                if (res_i in particle_resids[rank] and res_j in all_resids):
                   flag = 1
              elif (chain_A != str(chain_id) and chain_B == str(chain_id)):
                if (res_i in all_resids and res_j in particle_resids[rank]):
                   flag = 1
            if flag == 1:
              pass
            else:
              fout.write(line) 

        else:
            fout.write(line)
  return

def get_restraints(res_file, ninfo_file, pdb_name):
    """
    Parse the restraints file and format the ninfo
    """
    parser = ConfigParser()
    parser.read(res_file)
    for name, value in parser.items("Interaction Types"):
        if name == "tertiary":
            list_items = value.lstrip().splitlines()
            ## Initialize a list of lists
            features = [[] for i in range(len(list_items[0].split()))]
            for lines in list_items[1:len(list_items)]:
                for rank in range(0,len(features)):
                    features[rank].append(lines.split()[rank])
            ## assign name to elemens in the features list
            [res_i, res_j, chain_i, chain_j, dist, weight, type_i, type_j] = [i for i  in features]
            #print(res_i, chain_i, chain_j)
    ## get the list of atoms in pdb
    atoms = get_atomName(pdb_name)
    #print(atoms)
    with open(pdb_name,'r') as fin:
      chains = []
      for line in fin:
        if line.startswith("ATOM"):
          chain_id = line[19:22].strip()
          chains.append(chain_id)
    #print(set(chains))
    unique_chainids = sorted(set(chains)) ## sort based on chain A, B etc
    #print(unique_chainids)
    chainid_dict = {} ## define a dictionary of chain id and atom count
    for pos in range(len(unique_chainids)):
      #print(pos) 
      chainid_dict[pos] = chains.count(unique_chainids[pos])
    #print(chainid_dict)
    ## Get the residue number to name map
    res_map = map_resid2name(pdb_name)
    ## map unicode characters to utf-8
    #res_i, res_j, chain_i, chain_j, dist, weight, type_i, type_j = map(str,res_i), map(str,res_j),map(str,chain_i),map(str,chain_j),map(str,dist),map(str,weight),map(str,type_i),map(str,type_j)
    for list_item in [res_i, res_j, chain_i, chain_j, dist, weight, type_i, type_j]:
      [x.encode('UTF8') for x in list_item]
      #print(list_item)
    res_i2, res_j2 = [None]*len(res_i), [None]*len(res_i) ## initiate two lists for renumbering residues in second chain
    if (atoms[0] == "P"):
        for rank in range(len(res_i)):
          #print("P is first")
          if (type_i[rank] == "P" and chain_i[rank] == "1"):
            res_i[rank] = (int(res_i[rank])-1)*3 + 1
            res_i2[rank] = res_i[rank]
          if (type_i[rank] == "P" and chain_i[rank] == "2"):
            res_i[rank] = (int(res_i[rank])-1)*3 + 1
            res_i2[rank] = res_i[rank] + int(chainid_dict[0])
          if (type_j[rank] == "P" and chain_j[rank] == "1"):
            res_j[rank] = (int(res_j[rank])-1)*3 + 1
            res_j2[rank] = res_j[rank]
          if (type_j[rank] == "P" and chain_j[rank] == "2"):
            res_j[rank] = (int(res_j[rank])-1)*3 + 1
            res_j2[rank] = res_j[rank] + int(chainid_dict[0])

          if (type_i[rank] == "S" and chain_i[rank] == "1"):
            res_i[rank] = (int(res_i[rank])-1)*3 + 2
            res_i2[rank] = res_i[rank]
          if (type_i[rank] == "S" and chain_i[rank] == "2"):
            res_i[rank] = (int(res_i[rank])-1)*3 + 2
            res_i2[rank] = res_i[rank] + int(chainid_dict[0])
          if (type_j[rank] == "S" and chain_j[rank] == "1"):
            res_j[rank] = (int(res_j[rank])-1)*3 + 2
            res_j2[rank] = res_j[rank]
          if (type_j[rank] == "S" and chain_j[rank] == "2"):
            res_j[rank] = (int(res_j[rank])-1)*3 + 2 
            res_j2[rank] = res_j[rank] + int(chainid_dict[0])


          if (type_i[rank] == "B" and chain_i[rank] == "1"):
            type_i[rank] = list(res_map[int(res_i[rank])])[1]
            res_i[rank] = (int(res_i[rank])-1)*3 + 3
            res_i2[rank] = res_i[rank] 
          if (type_i[rank] == "B" and chain_i[rank] == "2"):
            type_i[rank] = list(res_map[int(res_i[rank])])[1]
            res_i[rank] = (int(res_i[rank])-1)*3 + 3
            res_i2[rank] = res_i[rank] + int(chainid_dict[0])
          if (type_j[rank] == "B" and chain_j[rank] == "1"):
            type_j[rank] = list(res_map[int(res_j[rank])])[1]
            res_j[rank] = (int(res_j[rank])-1)*3 + 3
            res_j2[rank] = res_j[rank]
          if (type_j[rank] == "B" and chain_j[rank] == "2"):
            type_j[rank] = list(res_map[int(res_j[rank])])[1]
            res_j[rank] = (int(res_j[rank])-1)*3 + 3
            res_j2[rank] = res_j[rank] + int(chainid_dict[0])


    elif (atoms[0] == "S"):
        for rank in range(len(res_i)):
          #print("P is first")
          if (type_i[rank] == "P" and chain_i[rank] == "1"):
            res_i[rank] = (int(res_i[rank])-1)*3 
            res_i2[rank] = res_i[rank]
          if (type_i[rank] == "P" and chain_i[rank] == "2"):
            res_i[rank] = (int(res_i[rank])-1)*3
            res_i2[rank] = res_i[rank] + int(chainid_dict[0])
          if (type_j[rank] == "P" and chain_j[rank] == "1"):
            res_j[rank] = (int(res_j[rank])-1)*3
            res_j2[rank] = res_j[rank]
          if (type_j[rank] == "P" and chain_j[rank] == "2"):
            res_j[rank] = (int(res_j[rank])-1)*3
            res_j2[rank] = res_j[rank] + int(chainid_dict[0])

          if (type_i[rank] == "S" and chain_i[rank] == "1"):
            res_i[rank] = (int(res_i[rank])-1)*3 + 1
            res_i2[rank] = res_i[rank]
          if (type_i[rank] == "S" and chain_i[rank] == "2"):
            res_i[rank] = (int(res_i[rank])-1)*3 + 1
            res_i2[rank] = res_i[rank] + int(chainid_dict[0])
          if (type_j[rank] == "S" and chain_j[rank] == "1"):
            res_j[rank] = (int(res_j[rank])-1)*3 + 1
            res_j2[rank] = res_j[rank]
          if (type_j[rank] == "S" and chain_j[rank] == "2"):
            res_j[rank] = (int(res_j[rank])-1)*3 + 1
            res_j2[rank] = res_j[rank] + int(chainid_dict[0])


          if (type_i[rank] == "B" and chain_i[rank] == "1"):
            type_i[rank] = list(res_map[int(res_i[rank])])[1]
            res_i[rank] = (int(res_i[rank])-1)*3 + 2
            res_i2[rank] = res_i[rank]
          if (type_i[rank] == "B" and chain_i[rank] == "2"):
            type_i[rank] = list(res_map[int(res_i[rank])])[1]
            res_i[rank] = (int(res_i[rank])-1)*3 + 2
            res_i2[rank] = res_i[rank] + int(chainid_dict[0])
          if (type_j[rank] == "B" and chain_j[rank] == "1"):
            type_j[rank] = list(res_map[int(res_j[rank])])[1]
            res_j[rank] = (int(res_j[rank])-1)*3 + 2
            res_j2[rank] = res_j[rank]
          if (type_j[rank] == "B" and chain_j[rank] == "2"):
            type_j[rank] = list(res_map[int(res_j[rank])])[1]
            res_j[rank] = (int(res_j[rank])-1)*3 + 2
            res_j2[rank] = res_j[rank] + int(chainid_dict[0])

    #print(res_i, res_i2, res_j, res_j2) 
    return [res_i, res_j, res_i2, res_j2, chain_i, chain_j, dist, weight, type_i, type_j]


def get_atomName(pdb_name):
    """ Return a list of atom names in a pdb file """
    pdb_file = open(pdb_name, 'r')
    atoms = []
    for line in pdb_file:
        n = line[12:16].strip()
        if (line.startswith("ATOM")):
            # extract n (atom name)
            atoms.append(n)
    return atoms
    

def get_totalContact(ninfo_file):
    """Count the number of lines in ninfo file starting with term 'contact' """
    with open(ninfo_file,'r') as fin:
        count_contact = 0
        line_count = 0
        for line in fin:
            line_count += 1
            if line.startswith("contact"):
                count_contact +=1
    return count_contact


def map_resid2name(pdb_name):
    """
read xyz from pdb
generate a resid to resname dictionary
    """
    xyz = []
    pdb_file = open(pdb_name, 'r')
    for line in pdb_file:
        n = line[12:16].strip()
        if (line.startswith("ATOM")):
            # extract n (atom name), rn (residue name), r (residue no.),x, y, z coordinates
            rn = line[17:20].strip()
            r = int(line[22:26].strip())
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())
            #if line[12:16].strip() == "CA":
            xyz.append([n, rn, r, x, y, z])
    pdb_file.close()
    # define a residue dictionary
    res_dis = {}
    first_res = xyz[0][2]
    res_dis[first_res] = xyz[0][1]
    #print(first_res)
    for item in xyz:
        if (item[2] != first_res):
            res_dis[item[2]] = item[1]
        first_res = item[2]
    #print(res_dis)
    return res_dis


if __name__ == '__main__':
  #import ast
  if len( sys.argv ) == 4:
    num_arg = len(sys.argv)
    user_contacts = sys.argv[1]
    input_file = sys.argv[2]  ## this is the ninfo file
    out_file = input_file.split(".")[0]+"_removed.ninfo"
    pdb_name = sys.argv[3]
    inputList = user_contacts.split(",")
    # create two buckets to conatain the chains and resids.
    chains_in = []
    resids = []
    for element in inputList:
      chain = element.split(":")[0]
      group = element.split(":")[1]
      chains_in.append(chain)
      resids.append(list(range(int(group.split("-")[0]),int(group.split("-")[1]))))
    #print(chains, resids)
    scale_Coef(input_file, out_file, chains_in, resids, pdb_name)
    
  else:
    print("provide correct number of arguments, see usage")
    usage()
    sys.exit()