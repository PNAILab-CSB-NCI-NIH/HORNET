import unittest
from unittest.mock import mock_open, patch
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../src")
from hornet.input import get_parameter

class TestGetParameter(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='#   test\n#   case\n#   example\ndo not')
    def test_get_parameter(self, mock_file):
        result = get_parameter('test_file.txt')
        self.assertEqual(result, ['test\n', 'case\n', 'example\n'])

    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_get_parameter_empty_file(self, mock_file):
        result = get_parameter('empty_file.txt')
        self.assertEqual(result, [])

    @patch('builtins.open', new_callable=mock_open, read_data='no comments in this file')
    def test_get_parameter_no_comments(self, mock_file):
        result = get_parameter('no_comments.txt')
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()