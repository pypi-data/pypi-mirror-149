#!/usr/bin/env python3

"""Test of the variables database 

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')

import hepdata.names as hn

class TestVariable(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(hn.Variable.PT,   'PT')
        self.assertEqual(hn.Variable.OMEGA,'OMEGA')

    def test_phrases(self):
        self.assertEqual(hn.Variable.phrases(hn.Variable.PT),
                         [hn.Phrase.PT_DEPENDENCE])
        self.assertEqual(hn.Variable.phrases(hn.Variable.OMEGA),[])

    def test_units(self):
        self.assertEqual(hn.Variable.units(hn.Variable.PT),  hn.Unit.GEVC)
        self.assertEqual(hn.Variable.units(hn.Variable.OMEGA),None)

    def test_pretty(self):
        self.assertEqual(hn.Variable.pretty(hn.Variable.PT),
                         r'$p_{\mathrm{T}}$')
        self.assertEqual(hn.Variable.pretty(hn.Variable.OMEGA),
                         r'$\Omega$')

    def test_register(self):
        hn.Variable.register('FOO','BAR',r'f',
                             {'NEW_UNIT': 'U'},
                             [{'NEW_PHRASE': 'This is a new phrase'}],
                             True)
        self.assertEqual(hn.Variable.FOO,	'BAR')
        self.assertEqual(hn.Variable.pretty(hn.Variable.FOO), r'$f$')
        self.assertEqual(hn.Variable.phrases(hn.Variable.FOO),
                         ['This is a new phrase'])
        self.assertEqual(hn.Variable.units(hn.Variable.FOO),  hn.Unit.NEW_UNIT)
        self.assertEqual(hn.Observable.FOO, hn.Variable.FOO)
        
    def test_missing(self):
        with self.assertRaises(NameError):
            print(Variable.FUBAR)

if __name__ == '__main__':
    unittest.main()

#
# EOF
#
        
