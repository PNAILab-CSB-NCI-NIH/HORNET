import sys
## Usage: $ python scale_coef_duplex.py [2,1,1,1,1,1,1] [3,1,1,1,1,1,1] cbl_dimer.ninfo input_Y4J.bpl cbl_dimer.pdb

def usage():
  print("Usage:")
  print("python scale_coef_duplex_ninfo.py scale_duplex scale_nonduplex ninfo_file basepair_file cg_pdbfile\n")
  print("    scale_duplex       given as [x,x,x,x,x,x,x] representing [bond, angle, dihedral_1, dihedral_2, long_range, basepair, basestack]") 
  print("                       x represents an integral multiplication factor x < 10")
  print("    scale_nonduplex    given as [x,x,x,x,x,x,x] representing [bond, angle, dihedral_1, dihedral_2, long_range, basepair, basestack]")
  print("    ninfo_file         native info file from cafemol")
  print("    basepair_file      basepair info file for duplex, example at scripts_path/rna2d3d/input.bpl")
  print("    cg_pdbfile         coarse grained PDB filei\n")
  print("                       If all of the residues participating in bond, angle, long range, basepair and basestack belong to duplex, the duplex scaling factor is chosen. For dihedral, if both second and third resiude belong to the duplex, the duplex scaling factor is applied.")

def scale_coef(input_file, basepair_file, pdb_name, out_file, factors_dup, factors_ndup):
  [bd_dup, ba_dup, dih1_dup, dih2_dup,long_dup, bp_dup, bs_dup] = map(float, factors_dup.strip('[]').split(','))
  [bd_ndup, ba_ndup, dih1_ndup, dih2_ndup, long_ndup, bp_ndup, bs_ndup] = map(float, factors_ndup.strip('[]').split(','))
  duplex, nonduplex = getDuplex(basepair_file, pdb_name)
  #print(duplex)
  
  with open(input_file,'r') as fin, open(out_file, 'w') as fout :
    count_contact = 0
    for line in fin:
        if line.startswith("bond"):
            item1_list = [line.split()[0]]
            item2_list = [item.rjust(7) for item in line.split()[1:8]]
            item3_list = [item.rjust(13) for item in line.split()[8:11]]
            res_i, res_j = int(line.split()[6]), int(line.split()[7])
            if (res_i in duplex and res_j in duplex):
              item4 = '%.4f'% (float(line.split()[11])*bd_dup)
            elif (res_i in nonduplex or res_j in nonduplex):
              item4 = '%.4f'% (float(line.split()[11])*bd_ndup)
            else:
              print("residue not belonging to duplex or non duplex")
              sys.exit(1)
            #item4 = '%.4f'% (float(line.split()[11])*bd_dup)
            item4_list = [item4.rjust(13)]
            item5_list = [line.split()[12].rjust(3)]
            sum_list = item1_list+item2_list+item3_list+item4_list+item5_list
            sum_string = "".join(sum_list)
            fout.write(sum_string+"\n")
        elif line.startswith("angl"):
            item1_list = [line.split()[0]]
            item2_list = [item.rjust(7) for item in line.split()[1:10]]
            item3_list = [item.rjust(13) for item in line.split()[10:13]]
            res_i, res_j, res_k = int(line.split()[7]), int(line.split()[8]), int(line.split()[9])
            if (res_i in duplex and res_j in duplex and res_k in duplex):
              item4 = '%.4f'% (float(line.split()[13])*ba_dup)
            elif (res_i in nonduplex or res_j in nonduplex or res_k in nonduplex):
              item4 = '%.4f'% (float(line.split()[13])*ba_ndup)
            else:
              print("residue not belonging to duplex or non duplex")
              sys.exit(1)
            #item4 = '%.4f'% (float(line.split()[13])*ba_dup)
            item4_list = [item4.rjust(13)]
            item5_list = [line.split()[14].rjust(4)]
            sum_list = item1_list+item2_list+item3_list+item4_list+item5_list
            sum_string = "".join(sum_list)
            fout.write(sum_string+"\n")
        elif line.startswith("dihd"):
            item1_list = [line.split()[0]]
            item2_list = [item.rjust(7) for item in line.split()[1:12]]
            item3_list = [item.rjust(13) for item in line.split()[12:15]]
            res_i, res_j, res_k, res_l = int(line.split()[8]), int(line.split()[9]), int(line.split()[10]), int(line.split()[11])
            if (res_j in duplex and res_k in duplex ):
              item4 = '%.4f'% (float(line.split()[15])*dih1_dup)
              item5 = '%.4f'% (float(line.split()[16])*dih2_dup)
            elif (res_i in nonduplex or res_j in nonduplex or res_k in nonduplex or res_l in nonduplex):
              item4 = '%.4f'% (float(line.split()[15])*dih1_ndup)
              item5 = '%.4f'% (float(line.split()[16])*dih2_ndup)
            else:
              print("residue not belonging to duplex or non duplex")
              sys.exit(1)
            #item4 = '%.4f'% (float(line.split()[15])*dih1_dup)
            #item5 = '%.4f'% (float(line.split()[16])*dih2_dup)
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
            res_i, res_j = int(line.split()[6]), int(line.split()[7])
            if (res_i in duplex and res_j in duplex):
              item5 = '%.4f'% (float(line.split()[11])*long_dup)
            elif (res_i in nonduplex or res_j in nonduplex):
              item5 = '%.4f'% (float(line.split()[11])*long_ndup)
            else:
              print("residue not belonging to duplex or non duplex")
              sys.exit(1)
 
            #item5 = '%.4f'% (float(line.split()[11])*long_factor)
            item5_list = [item5.rjust(13)]
            item6_list = [line.split()[12].rjust(4)]
            sum_list = item1_list+item2_list+item3_list+item4_list+item5_list+item6_list
            sum_string = "".join(sum_list)
            fout.write(sum_string+"\n")
        elif line.startswith("basepair"):
            item1_list = [line.split()[0]]
            item2_list = [item.rjust(7) for item in line.split()[1:8]]
            item3_list = [item.rjust(13) for item in line.split()[8:10]]
            item4_list = [line.split()[10].rjust(7)]
            res_i, res_j = int(line.split()[6]), int(line.split()[7])
            if (res_i in duplex and res_j in duplex):
              item5 = '%.4f'% (float(line.split()[11])*bp_dup)
            elif (res_i in nonduplex or res_j in nonduplex):
              item5 = '%.4f'% (float(line.split()[11])*bp_ndup)
            else:
              print("residue not belonging to duplex or non duplex")
              sys.exit(1)
            #item5 = '%.4f'% (float(line.split()[11])*bp_dup)
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
            res_i, res_j = int(line.split()[6]), int(line.split()[7])
            if (res_i in duplex and res_j in duplex):
              item5 = '%.4f'% (float(line.split()[11])*bs_dup)
            elif (res_i in nonduplex or res_j in nonduplex):
              item5 = '%.4f'% (float(line.split()[11])*bs_ndup)
            else:
              print("residue not belonging to duplex or non duplex")
              sys.exit(1)
            #item5 = '%.4f'% (float(line.split()[11])*bs_dup)
            item5_list = [item5.rjust(13)]
            item6_list = [line.split()[12].rjust(5)]
            sum_list = item1_list+item2_list+item3_list+item4_list+item5_list+item6_list
            sum_string = "".join(sum_list)
            fout.write(sum_string+"\n")

        else:
            fout.write(line)
  return


def readDuplexes(filename):
    """Return list of tuples containing pairs of resids of paired bases.
    """
    lines=open(filename).readlines()
    inHelicalSegment=False
    import string
    pairs=[]
    for line in lines:
        if (line.startswith('$ bplist')):
            inHelicalSegment=True
            pass

        if inHelicalSegment and line[0] in string.digits:
            pairs.append( line.split() )
            #print(pairs)
            pass


        pass
    #ret.append(pairs)
    return sum(pairs, [])

def getSequence(filename):
    """Return the sequence of residues from the base pair input file.
    """
    lines=open(filename).readlines()
    inSeq=False
    import string
    seq=[]
    for line in lines:
        if (line.startswith('>')):
            inSeq=True
            pass

        if inSeq and line[0].isalpha():
            seq.append( line.split() )
            #print(line)
            pass


        pass
    #print(seq)
    #print(sum(seq, []))
    return sum(seq, [])

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

def getDuplex(basepair_file, pdb_name):
    """ Get duplex and non duplex particle resids"""
    duplex = [int(i) for i in readDuplexes(basepair_file)]
    #print(len(duplex))
    seq = getSequence(basepair_file)
    all_resids = list(range(1, len(seq)+1))
    # print(all_resids)
    non_duplex = list(set(all_resids) -set(duplex))
    #print(len(non_duplex))

    ## Now finding the corresponding particle number of the resids
    atoms = get_atomName(pdb_name)
    particle_resduplex = []
    particle_resnonduplex = []

    if atoms[0] == "P":
      dup_list1 = [(3*(y-1)+1) for y in duplex]
      dup_list2 = [(3*(y-1)+2) for y in duplex]
      dup_list3 = [(3*(y-1)+3) for y in duplex]
      ndup_list1 = [(3*(y-1)+1) for y in non_duplex]
      ndup_list2 = [(3*(y-1)+2) for y in non_duplex]
      ndup_list3 = [(3*(y-1)+3) for y in non_duplex]
      particle_resduplex.append(dup_list1+dup_list2+dup_list3)
      particle_resnonduplex.append(ndup_list1+ndup_list2+ndup_list3)
    if atoms[0] == "S":
      dup_list1 = [(3*(y-1)) for y in duplex if y != 1]
      dup_list2 = [(3*(y-1)+1) for y in duplex]
      dup_list3 = [(3*(y-1)+2) for y in duplex]
      ndup_list1 = [(3*(y-1)) for y in non_duplex if y != 1]
      ndup_list2 = [(3*(y-1)+1) for y in non_duplex]
      ndup_list3 = [(3*(y-1)+2) for y in non_duplex]
      particle_resduplex.append(dup_list1+dup_list2+dup_list3)
      particle_resnonduplex.append(ndup_list1+ndup_list2+ndup_list3)
    #print([sum(particle_resduplex, []), sum(particle_resnonduplex, [])])
    return [sum(particle_resduplex, []), sum(particle_resnonduplex, [])]
 
if __name__ == '__main__':  
  if len( sys.argv ) == 6:
    factors_dup = sys.argv[1]
    factors_ndup = sys.argv[2]
    input_file = sys.argv[3]
    out_file = input_file.split(".")[0]+"_mod.ninfo"
    basepair_file = sys.argv[4]
    pdb_name = sys.argv[5]
    scale_coef(input_file, basepair_file, pdb_name, out_file, factors_dup, factors_ndup)
  else:
    print("provide correct number of arguments")
    usage() 
    sys.exit(1)



