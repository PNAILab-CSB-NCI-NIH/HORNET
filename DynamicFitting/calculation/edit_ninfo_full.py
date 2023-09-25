#### Edit ninfo file with given weight factors
#### Usage: $ python3 edit_ninfo.py [2,2,2,2,2,2,2] monomer.ninfo restraints.txt cg_pdb 
#### list order of scale factors [bond, angle, dihedral_1, dihedral_2,long_range, basepair, basestack]
#### Value of each scale factor range (0:9)
#### a new ninfo file is produced with a name ninfo_file_mod

import sys
from configparser import ConfigParser

def usage():
  print("Usage:")
  print("1. To only scale the force coefficients:")
  print("python edit_ninfo_full.py scale_factor ninfo_file")
  print("\n2. To scale coefficients and add tertiary restraints")
  print("python edit_ninfo_full.py scale_factor ninfo_file restraint_file cg_pdbfile")
  print("\n        scale_factor    given as [x,x,x,x,x,x,x] representing [bond, angle, dihedral_1, dihedral_2,long_range,")
  print("                        basepair, basestack], x respresents integer multiplication factor, x < 10")
  print("        ninfo_file      native info file from cafemol")
  print("        restraint_file  file containing list of tertiary restraints, eg. at scripts_path/calculation/restraints_monomer.txt")
  print("        cg_pdbfile      coarse grained PDB file")


def scale_Coef(input_file, out_file, scale_factors, contact_info):
  [bd_factor, ba_factor, dih_factor1, dih_factor2,long_factor, bp_factor, bs_factor] = map(float, scale_factors.strip('[]').split(','))
  total_contact = get_totalContact(input_file) ## Total number of tertiary contacts in ninfo file
  with open(input_file,'r') as fin, open(out_file, 'w') as fout :
    count_contact = 0
    for line in fin:
        if line.startswith("bond"):
            item1_list = [line.split()[0]]
            item2_list = [item.rjust(7) for item in line.split()[1:8]]
            item3_list = [item.rjust(13) for item in line.split()[8:11]]
            item4 = '%.4f'% (float(line.split()[11])*bd_factor)
            item4_list = [item4.rjust(13)]
            item5_list = [line.split()[12].rjust(3)]
            sum_list = item1_list+item2_list+item3_list+item4_list+item5_list
            sum_string = "".join(sum_list)
            fout.write(sum_string+"\n")
        elif line.startswith("angl"):
            item1_list = [line.split()[0]]
            item2_list = [item.rjust(7) for item in line.split()[1:10]]
            item3_list = [item.rjust(13) for item in line.split()[10:13]]
            item4 = '%.4f'% (float(line.split()[13])*ba_factor)
            item4_list = [item4.rjust(13)]
            item5_list = [line.split()[14].rjust(4)]
            sum_list = item1_list+item2_list+item3_list+item4_list+item5_list
            sum_string = "".join(sum_list)
            fout.write(sum_string+"\n")
        elif line.startswith("dihd"):
            item1_list = [line.split()[0]]
            item2_list = [item.rjust(7) for item in line.split()[1:12]]
            item3_list = [item.rjust(13) for item in line.split()[12:15]]
            item4 = '%.4f'% (float(line.split()[15])*dih_factor1)
            item5 = '%.4f'% (float(line.split()[16])*dih_factor2)
            item4_list = [item4.rjust(13)]
            item5_list = [item5.rjust(13)]
            item6_list = [line.split()[17].rjust(5)]
            sum_list = item1_list+item2_list+item3_list+item4_list+item5_list+item6_list
            sum_string = "".join(sum_list)
            fout.write(sum_string+"\n")
        elif line.startswith("contact"):
            item1_list = [line.split()[0]]
            item2_list = [item.rjust(7) for item in line.split()[1:8]]
            item3_list = [item.rjust(13) for item in line.split()[8:10]]
            item4_list = [item.rjust(7) for item in line.split()[10]]
            item5 = '%.4f'% (float(line.split()[11])*long_factor)
            item5_list = [item5.rjust(13)]
            item6_list = [line.split()[12].rjust(4)]
            sum_list = item1_list+item2_list+item3_list+item4_list+item5_list+item6_list
            sum_string = "".join(sum_list)
            fout.write(sum_string+"\n")
            count_contact += 1
            if (count_contact == total_contact and num_arg == 5):
                [res_i, res_j, res_i2, res_j2, chain_i, chain_j, dist, weight, type_i, type_j] = contact_info
                fmt_contact = '%-7s%7d%7d%7d%7d%7d%7d%7d%13.4f%13.4f%7d%13.4f%4s'
                for rank in range(len(res_i)):
                    count_contact += 1
                    fout.write(fmt_contact  % ("contact",count_contact,int(chain_i[rank]),int(chain_j[rank]),res_i2[rank], res_j2[rank],
                                               res_i[rank],res_j[rank], float(dist[rank]), 1.0,1,
                                               float(weight[rank]),type_i[rank]+"-"+type_j[rank]))
                    fout.write("\n")


        elif line.startswith("basepair"):
            item1_list = [line.split()[0]]
            item2_list = [item.rjust(7) for item in line.split()[1:8]]
            item3_list = [item.rjust(13) for item in line.split()[8:10]]
            item4_list = [line.split()[10].rjust(7)]
            item5 = '%.4f'% (float(line.split()[11])*bp_factor)
            item5_list = [item5.rjust(13)]
            item6_list = [line.split()[12].rjust(5)]
            item7_list = [line.split()[13].rjust(2)]
            sum_list = item1_list+item2_list+item3_list+item4_list+item5_list+item6_list+item7_list
            sum_string = "".join(sum_list)
            fout.write(sum_string+"\n")
        elif line.startswith("basestack"):
            item1_list = [line.split()[0]]
            item2_list = [item.rjust(7) for item in line.split()[1:8]]
            item3_list = [item.rjust(13) for item in line.split()[8:10]]
            item4_list = [line.split()[10].rjust(7)]
            item5 = '%.4f'% (float(line.split()[11])*bs_factor)
            item5_list = [item5.rjust(13)]
            item6_list = [line.split()[12].rjust(5)]
            sum_list = item1_list+item2_list+item3_list+item4_list+item5_list+item6_list
            sum_string = "".join(sum_list)
            fout.write(sum_string+"\n")

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
  if len( sys.argv ) == 3:
    num_arg = len(sys.argv)
    scale_factors = sys.argv[1]
    input_file = sys.argv[2]  ## this is the ninfo file
    out_file = input_file.split(".")[0]+"_mod.ninfo"
    contact_info = [None]
    scale_Coef(input_file, out_file, scale_factors, contact_info)
    
  elif len( sys.argv ) == 5:
    #print("provide scale_factor, ninfo_file, restraint_file, and cg_pdbfile")
    #sys.exit()
    num_arg = len(sys.argv)   
    scale_factors = sys.argv[1]
    input_file = sys.argv[2]  ## this is the ninfo file
    out_file = input_file.split(".")[0]+"_mod.ninfo"
    res_file = sys.argv[3]
    pdb_name = sys.argv[4]
    ## Scale the coefficient weights
    contact_info = get_restraints(res_file, input_file, pdb_name)
    #print(contact_info)
    scale_Coef(input_file, out_file, scale_factors, contact_info)

  else:
    print("provide correct number of arguments, see usage")
    usage()
    sys.exit()