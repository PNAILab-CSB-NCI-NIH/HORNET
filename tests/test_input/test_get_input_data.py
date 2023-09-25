import os
import pandas as pd
import numpy as np
import unittest
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.input import get_input_data

class TestGetInputData(unittest.TestCase):

    def setUp(self):
        self.path = '.data_test'

        # Create temporary dir
        if (not os.path.exists(self.path)):
            os.mkdir(self.path)

        # Create temporary files
        file1 = open(f"{self.path}/en_allk1.txt", "w")
        file2 = open(f"{self.path}/en_allk2.txt", "w")
        file3 = open(f"{self.path}/bases_k1.csv", "w")
        file4 = open(f"{self.path}/bases_k2.csv", "w")
        
        # Write data to files
        file1.write(
"""# initial_energy
# total_energy =       23758.206
# t_series
#########################################################
#           step    tempk     radg       etot      velet qscore     rmsd
#unit       step    tempk     radg       etot      velet qscore     rmsd      local         go      repul  stack_rna      hbond      elect      afmcc     afmfit      stage
#########################################################
#all           0   298.00    38.41   23758.21     679.46  0.664     0.00   12186.94    4720.03       0.76    3655.32    1736.39     249.66  0.8183924    1208.90      -0.63
#""")
        
        file2.write(
"""# initial_energy
# total_energy =       23758.206
# t_series
#########################################################
#           step    tempk     radg       etot      velet qscore     rmsd
#unit       step    tempk     radg       etot      velet qscore     rmsd      local         go      repul  stack_rna      hbond      elect      afmcc     afmfit      stage
#########################################################
#all           0   298.00    38.41   23758.21     679.46  0.664     0.00   12186.94    4720.03       0.76    3655.32    1736.39     249.66  0.8183924    1208.90      -0.63
#""")
        
        file3.write("base_pair,base_stack,frame,kapa\n"
                    "5,10,0,1\n"
                    "5,10,1,1\n")
        
        file4.write("base_pair,base_stack,frame,kapa\n"
                    "6,12,0,2\n"
                    "6,12,1,2\n")
        
        file1.close()
        file2.close()
        file3.close()
        file4.close()

    def tearDown(self):
        os.system(f"rm -rf {self.path}")

    def test_invalid_path(self):
        # Test with invalid path parameter
        with self.assertRaises(FileExistsError):
            df = get_input_data(path='./')

    def test_default_files(self):
        # Test using default test files
        base_pairing = -1
        base_stacking = -1
        initial = "en_all"
        df = get_input_data(self.path, base_pairing, base_stacking, initial)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        baseP_expected = np.sort(df['baseP'].unique())
        baseS_expected = np.sort(df['baseS'].unique())
        self.assertTrue(len(baseP_expected) == 2)
        self.assertTrue(len(baseS_expected) == 2)
        self.assertTrue(5 in baseP_expected and 6 in baseP_expected)
        self.assertTrue(10 in baseS_expected and 12 in baseS_expected)
    
    def test_custom_parameters(self):
        # Test with custom parameters
        base_pairing = 2
        base_stacking = 3
        initial = "en_all"
        df = get_input_data(self.path, base_pairing, base_stacking, initial)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertTrue(df['baseP'].unique() == [2])
        self.assertTrue(df['baseS'].unique() == [3])

if __name__ == "__main__":
    unittest.main()