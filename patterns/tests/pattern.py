import unittest
from patterns.pattern import rabin_karp


class GraphTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_it(self):
        self.assertEqual(1, rabin_karp(substring="a", string="xalt"))
        self.assertEqual(0, rabin_karp(substring="o", string="olo"))
        self.assertEqual(-1, rabin_karp(substring="xa", string="olo"))
