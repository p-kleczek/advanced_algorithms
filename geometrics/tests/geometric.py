import unittest
from geometrics.geometric import *

__author__ = 'pawel'


class PointTest(unittest.TestCase):
    def test_equal(self):
        p1 = Point(x=3, y=2)
        p2 = Point(x=3, y=2)
        self.assertEqual(p1, p2)

    def test_less_than(self):
        p1 = Point(x=3, y=5)
        p2 = Point(x=3, y=2)
        self.assertTrue(p2 < p1)

        p1 = Point(x=2, y=2)
        p2 = Point(x=3, y=2)
        self.assertTrue(p1 < p2)


class GeometricTest(unittest.TestCase):
    def test_det(self):
        p = Point(x=2, y=3)
        q = Point(x=1, y=2)
        r = Point(x=3, y=6)
        self.assertEqual(-2, det(p, q, r))
