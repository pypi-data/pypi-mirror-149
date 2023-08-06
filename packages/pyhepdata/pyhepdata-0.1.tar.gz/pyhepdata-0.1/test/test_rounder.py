#!/usr/bin/env python3 
"""Test case for Rounder

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')

from hepdata.rounder import Rounder

class TestRounder(unittest.TestCase):

    def test_one_value(self):
        self.assertEqual(Rounder.round(12.345,2),12)
        self.assertEqual(Rounder.round(1.2345,2),1.2)
        self.assertEqual(Rounder.round(0.12345,2),0.12)
        self.assertEqual(Rounder.round(0.012345,2),0.012)
        self.assertEqual(Rounder.round(12.3456,4),12.35)
        self.assertEqual(Rounder.round(12.3456,3),12.3)
        self.assertEqual(Rounder.round(12.3450,4),12.34)
        self.assertEqual(Rounder.round(12.3350,4),12.34)


    def test_n_values(self):
        self.assertEqual(Rounder.round([12.345,0.12345],2),[12,0.12])

    def test_result(self):
        v = 12.3456
        e = [1.23456,0.123456,0.0123456]
        self.assertEqual(Rounder.roundResult(v,e,2),
                         (12.346,[1.235,0.123,0.012]))
        e = [1.2345,0.12345,0.012345]
        self.assertEqual(Rounder.roundResult(v,e,2),
                         (12.346,[1.234,0.123,0.012]))

if __name__ == '__main__':
    unittest.main()

#
# EOF
#
