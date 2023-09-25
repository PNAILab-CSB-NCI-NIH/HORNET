import os
import pandas as pd
import numpy as np
import unittest
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.input import prepare_inputs

class TestPrepareInputs(unittest.TestCase):

    def setUp(self):
        self.path = '.data_test'

        # Create temporary dir
        if (not os.path.exists(self.path)):
            os.mkdir(self.path)

        # Create temporary files
        file1 = open(f"{self.path}/en_allk1.txt", "w")
        file2 = open(f"{self.path}/en_allk55.txt", "w")
        file3 = open(f"{self.path}/bases_k1.csv", "w")
        file4 = open(f"{self.path}/bases_k55.csv", "w")
        
        # Write data to files
        file1.write(
"""# initial_energy
# total_energy =       23758.206
# t_series
#########################################################
#           step    tempk     radg       etot      velet qscore     rmsd
#unit       step    tempk     radg       etot      velet qscore     rmsd      local         go      repul  stack_rna      hbond      elect      afmcc     afmfit      stage
#########################################################""")
        
        file2.write(
"""# initial_energy
# total_energy =       23758.206
# t_series
#########################################################
#           step    tempk     radg       etot      velet qscore     rmsd
#unit       step    tempk     radg       etot      velet qscore     rmsd      local         go      repul  stack_rna      hbond      elect      afmcc     afmfit      stage
#########################################################""")
        
        file3.write("base_pair,base_stack,frame,kapa\n")
        
        file4.write("base_pair,base_stack,frame,kapa\n")

        for i in range(2005):
            file1.write(f"#all           0   298.00    38.41   -1     679.46  0.664     0.00   {i}    -1       0.76    3655.32    1736.39     249.66  0.8183924    1208.90      -0.63\n")
            file2.write(f"#all           0   298.00    38.41   -1     679.46  0.664     0.00   {i}    -1       0.76    3655.32    1736.39     249.66  0.8183924    1208.90      -0.63\n")
            file3.write(f"5,10,{i},1\n")
            file4.write(f"6,12,{i},55\n")
        for i in range(5):
            file1.write("#all           0   298.00    38.41   1     679.46  0.664     0.00   1    -1       0.76    3655.32    1736.39     249.66  0.8183924    1208.90      -0.63\n")
            file2.write("#all           0   298.00    38.41   1     679.46  0.664     0.00   1    -1       0.76    3655.32    1736.39     249.66  0.8183924    1208.90      -0.63\n")
            file3.write(f"5,10,{i+2005},1\n")
            file4.write(f"6,12,{i+2005},55\n")
        for i in range(5):
            file1.write("#all           0   298.00    38.41   -1     679.46  0.664     0.00   1    1       0.76    3655.32    1736.39     249.66  0.8183924    1208.90      -0.63\n")
            file2.write("#all           0   298.00    38.41   -1     679.46  0.664     0.00   1    1       0.76    3655.32    1736.39     249.66  0.8183924    1208.90      -0.63\n")
            file3.write(f"5,10,{i+2010},1\n")
            file4.write(f"6,12,{i+2010},55\n")
        
        file1.close()
        file2.close()
        file3.close()
        file4.close()

    def tearDown(self):
        os.system(f"rm -rf {self.path}")

    def test_invalid_path(self):
        # Test with invalid path parameter
        with self.assertRaises(FileExistsError):
            prepare_inputs(path='./')

    def test_default_files(self):
        # Test using default test files
        base_pairing = -1
        base_stacking = -1
        prepare_inputs(self.path, base_pairing, base_stacking)
        self.assertTrue(os.path.exists(f"{self.path}/Full_Trajectory.csv"))
        df = pd.read_csv(f"{self.path}/Full_Trajectory.csv")
        self.assertTrue(len(df) == 3)
        self.assertTrue(df['baseP'].unique() == [5])
        self.assertTrue(df['baseS'].unique() == [10])
    
    def test_custom_parameters(self):
        # Test with custom parameters
        base_pairing = 2
        base_stacking = 3
        prepare_inputs(self.path, base_pairing, base_stacking)
        self.assertTrue(os.path.exists(f"{self.path}/Full_Trajectory.csv"))
        df = pd.read_csv(f"{self.path}/Full_Trajectory.csv")
        self.assertTrue(len(df) == 3)
        self.assertTrue(df['baseP'].unique() == [2])
        self.assertTrue(df['baseS'].unique() == [3])

if __name__ == "__main__":
    unittest.main()