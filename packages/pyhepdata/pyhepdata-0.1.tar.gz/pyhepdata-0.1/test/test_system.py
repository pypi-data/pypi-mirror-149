#!/usr/bin/env python3

"""Test of the units database 

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')

import hepdata.names as hn

class TestSystem(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(hn.System.PP,	'P P')
        self.assertEqual(hn.System.AUAU,'AU AU')

    def test_pretty(self):
        self.assertEqual(hn.System.pretty(hn.System.PP),
                         r'$\mathrm{p}\mathrm{p}$')
        self.assertEqual(hn.System.pretty(hn.System.AUAU),
                         r'$\mathrm{Au}-\mathrm{Au}$')
        self.assertEqual(hn.System.pretty(hn.System.AA),
                         r'$\mathrm{A}-\mathrm{A}$')

    def test_register(self):
        hn.System.register('FOO','FOO BAR',r'\mathrm{Foo}')
        self.assertEqual(hn.System.FOO,	'FOO BAR')
        self.assertEqual(hn.System.pretty(hn.System.FOO),
                         r'$\mathrm{Foo}$')

        hn.System.register('XEXE',
                           aa=True,
                           projectile=hn.Particle.XE,
                           target=hn.Particle.XE)
        self.assertEqual(hn.System.XEXE,	'XE XE')
        self.assertEqual(hn.System.pretty(hn.System.XEXE),
                         r'$\mathrm{Xe}-\mathrm{Xe}$')
        
    def test_missing(self):
        with self.assertRaises(NameError):
            print(System.FUBAR)

if __name__ == '__main__':
    unittest.main()

#
# EOF
#
        
