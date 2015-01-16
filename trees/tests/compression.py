import unittest
from trees.compression import *

__author__ = 'pawel'


class CountOccurencesTest(unittest.TestCase):
    def test_it(self):
        s = "A B XA"
        freq = count_occurences(s)
        self.assertDictEqual({'A': 2, 'B': 1, ' ': 2, 'X': 1}, freq)
