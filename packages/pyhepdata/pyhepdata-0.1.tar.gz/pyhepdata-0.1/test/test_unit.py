#!/usr/bin/env python3

"""Test of the units database 

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')

import hepdata.names as hn

class TestUnit(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(hn.Unit.GEV,	'GEV')
        self.assertEqual(hn.Unit.GEVC,	'GEV/C')

    def test_pretty(self):
        self.assertEqual(hn.Unit.pretty(hn.Unit.GEV),
                         r'$\mathrm{Ge\!V}$')
        self.assertEqual(hn.Unit.pretty(hn.Unit.MEV),
                         r'$\mathrm{Me\!V}$')
        self.assertEqual(hn.Unit.pretty(hn.Unit.PCT),
                         r'$\%$')

    def test_register(self):
        hn.Unit.register('FOO','BAR',r'\mathrm{Foo}')
        self.assertEqual(hn.Unit.FOO,	'BAR')
        self.assertEqual(hn.Unit.pretty(hn.Unit.FOO),
                         r'$\mathrm{Foo}$')

    def test_missing(self):
        with self.assertRaises(NameError):
            print(Unit.FUBAR)

if __name__ == '__main__':
    unittest.main()

#
# EOF
#
        
