#!/usr/bin/env python3

"""Test of the observables database 

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')

import hepdata.names as hn

class TestObservable(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(hn.Observable.Y_DENSITY, 'DN/DYRAP')
        self.assertEqual(hn.Observable.RAA,'RAA')

    def test_phrases(self):
        self.assertEqual(hn.Observable.phrases(hn.Observable.Y_DENSITY),
                         [hn.Phrase.YRAP_DEPENDENCE,
                          hn.Phrase.DENSITY])
        self.assertEqual(hn.Observable.phrases(hn.Observable.RAA),
                         [hn.Phrase.NUCL_MODIFICATION,
                          hn.Phrase.AA_COLLISION])

    def test_units(self):
        self.assertEqual(hn.Observable.units(hn.Observable.Y_DENSITY),None)
        self.assertEqual(hn.Observable.units(hn.Observable.MEANPT),
                         hn.Unit.GEVC)

    def test_pretty(self):
        self.assertEqual(hn.Observable.pretty(hn.Observable.Y_DENSITY),
                         r'$\frac{\mathrm{d}N}{\mathrm{d}y}$')
        self.assertEqual(hn.Observable.pretty(hn.Observable.MEANPT),
                         r'$\langle p_{\mathrm{T}}\rangle$')

    def test_register(self):
        hn.Observable.register('FOO','BAR',r'f',
                             {'NEW_UNIT': 'U'},
                             [{'NEW_PHRASE': 'This is a new phrase'}],
                             True)
        self.assertEqual(hn.Observable.FOO,	'BAR')
        self.assertEqual(hn.Observable.pretty(hn.Observable.FOO), r'$f$')
        self.assertEqual(hn.Observable.phrases(hn.Observable.FOO),
                         ['This is a new phrase'])
        self.assertEqual(hn.Observable.units(hn.Observable.FOO),
                         hn.Unit.NEW_UNIT)
        self.assertEqual(hn.Observable.FOO, hn.Variable.FOO)
        
    def test_missing(self):
        with self.assertRaises(NameError):
            print(Observable.FUBAR)

if __name__ == '__main__':
    unittest.main()

#
# EOF
#
        
