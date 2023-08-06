#!/usr/bin/env python3 
"""Test case for Submission

Copyright 2019 Christian Holm Christensen
"""
import math
import unittest
import io
import sys
sys.path.append('..')

from pprint import pprint
from hepdata.submission import Submission
from hepdata.meta import Meta
from hepdata.table import Table

class TestSubmission(unittest.TestCase):

    def test_basic(self):
        s = Submission()
        m = s.meta('n','d','f')
        t = m.table()
        i = t.independent('x','ux')
        d = t.dependent('y','uy')

    def test_fast(self):
        sys   = 'AU AU'
        sqrts = 200
        var   = 'YRAP'
        obs   = 'DN/DYRAP'
        parts = ['PI+','PI-', 'K+', 'K-', 'P', 'PBAR']
        phrs  = 'Rapidity Dependence'
        s     = Submission()
        t, m  = s.table('d',sys, sqrts, var, obs, parts, phrs, 1, both=True)

        self.assertEqual(m._d[Meta.NAME],        'Table {}'.format(1))
        self.assertEqual(m._d[Meta.LOCATION],    'Table {}'.format(1))
        self.assertEqual(m._d[Meta.DESCRIPTION], 'd')
        self.assertEqual(m._d[Meta.DATA_FILE],   'tab{}.yaml'.format(1))
        # reac = [e[Meta.VALUES] for e in m._d[Meta.KEYWORDS]
        #         if e[Meta.NAME] ==  Meta.REACTIONS][0]
        # reac.sort();
        # ereac = ["{} --> {}".format(sys,p) for p in parts];
        # ereac.sort();
        # self.assertEqual(reac, ereac)
        
        self.assertEqual([e[Meta.VALUES] for e in m._d[Meta.KEYWORDS]
                          if e[Meta.NAME] ==  Meta.REACTIONS][0],
                         ["{} --> {}".format(sys,p) for p in parts])
        self.assertEqual([e[Meta.VALUES] for e in m._d[Meta.KEYWORDS]
                          if e[Meta.NAME] ==  Meta.OBSERVABLES][0],
                         [obs])
        self.assertEqual([e[Meta.VALUES] for e in m._d[Meta.KEYWORDS]
                          if e[Meta.NAME] ==  Meta.PHRASES][0],
                         [phrs])
        self.assertEqual([e[Meta.VALUES] for e in m._d[Meta.KEYWORDS]
                          if e[Meta.NAME] ==  Meta.CMENERGIES][0],
                         [sqrts])

        
    @unittest.skip('Takes too long')
    def test_fill(self):
        s = Submission()
        s.fill('Phys.Lett.,B650,219')

        self.assertEqual(s._l,
                         {'license': 'CC-BY-3.0',
                          'url':'http://creativecommons.org/licenses/by/3.0/'})
        self.assertEqual(s.getPublished(), '2007')
        self.assertEqual(s.getPreprinted(), '2006')
        self.assertEqual(s.ids(),
                         [{'type': 'inspire',
                           'id': 729167,},
                          {'type': 'arxiv',
                           'id': 'nucl-ex/0610021',},
                          {'type': 'doi',
                           'id': '10.1016/j.physletb.2007.05.017',},
                          {'type': 'SPIRES',
                           'id': '6939295'}])


if __name__ == '__main__':
    unittest.main()

#
# EOF
#
        
