import unittest, sys, os

from shared.point import Point
from shared.constants import *

class PointUnitTests(unittest.TestCase):
    def test_point_eq(self):
        point1 = Point(1, 1)
        point2 = Point(2, 3)
        point3 = Point(2, 3)
        self.assertNotEqual(point1, point2)
        self.assertNotEqual(point2, point1)
        self.assertNotEqual(point1, point3)
        self.assertNotEqual(point3, point1)
        self.assertEqual(point2, point3)
        self.assertEqual(point3, point2)

    def test_bounds_checking(self):
        over_bounds = BOARD_ROW_LENGTH
        under_bounds = -1
        with self.assertRaises(ValueError):
            point = Point(0, over_bounds)
        with self.assertRaises(ValueError):
            point = Point(over_bounds, 0)
        with self.assertRaises(ValueError):
            point = Point(0, under_bounds)
        with self.assertRaises(ValueError):
            point = Point(under_bounds, 0)

if __name__ == "__main__":
    unittest.main()
