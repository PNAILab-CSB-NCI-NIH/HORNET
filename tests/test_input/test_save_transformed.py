import unittest
import os
import pandas as pd
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.input import save_transformed

class TestSaveTransformed(unittest.TestCase):

    def setUp(self):
        self.tmp = '.tmp'
        self.path = '.data_test'

        # Create temporary dir
        if (not os.path.exists(self.tmp)):
            os.mkdir(self.tmp)
        if (not os.path.exists(self.path)):
            os.mkdir(self.path)

    def tearDown(self):
        os.system(f"rm -r {self.tmp}")
        os.system(f"rm -r {self.path}")
    
    def test_save_transformed(self):
        # Create a test DataFrame
        df = pd.DataFrame({'col1': ['1', '2', '3'], 'col2': ['4', '*', '6']})
        n_lines_without_star = 3  # cols name \n 1,4 \n 3,6

        # Call the function with default parameters
        name = 'FullTrajectory'
        save_transformed(df, path=self.path, name=name)
        
        # Check if the file is saved in the correct path
        self.assertTrue(os.path.exists(f"{self.path}/{name}.csv"))
        
        # Check entries
        with open(f"{self.path}/{name}.csv", 'r') as file:
            lines = file.readlines()
            self.assertTrue(len(lines) == n_lines_without_star)
            for line in lines:
                self.assertNotIn('*', line)
    
    def test_save_transformed_no_star(self):
        # Create a test DataFrame
        df = pd.DataFrame({'col1': ['1', '2', '3'], 'col2': ['4', '5', '6']})
        n_lines_without_star = 4 # cols name \n 1,4 \n 2,5 \n 3,6

        # Call the function with default parameters
        name = 'FullTrajectory_no_star'
        save_transformed(df, path=self.path, name=name)
        
        # Check if the file is saved in the correct path
        self.assertTrue(os.path.exists(f"{self.path}/{name}.csv"))
        
        # Check entries
        with open(f"{self.path}/{name}.csv", 'r') as file:
            lines = file.readlines()
            self.assertTrue(len(lines) == n_lines_without_star)
        
if __name__ == '__main__':
    unittest.main()