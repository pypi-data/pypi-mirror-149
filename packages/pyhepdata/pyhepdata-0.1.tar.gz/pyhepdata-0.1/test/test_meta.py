#!/usr/bin/env python3 
"""Test case for Meta

Copyright 2019 Christian Holm Christensen
"""
import math
import unittest
import io
import sys
sys.path.append('..')

from pprint import pprint
from hepdata.meta import Meta

class TestMeta(unittest.TestCase):

    def test_basic(self):
        a = Meta('m','d','f')

    def test_keywords(self):
        a = Meta('m','d','f')
        
        a.keyword('a','b')
        a.keyword('a','c')
        self.assertEqual(a._d['keywords'][0]['values'],['c'])
                
        a.keyword('a','d',False)
        self.assertEqual(a._d['keywords'][0]['values'],['c','d'])

        a.keyword('a',None)
        self.assertEqual(len(a._d['keywords']),0)

    def test_table(self):
        a  = Meta('m','d','f')
        t  = a.table()
        tt = a.table()
        self.assertTrue(id(t) == id(tt))

    def test_allinone(self):
        a  = Meta('m','d','f')
        t  = a.table(True)
        self.assertTrue(a.allInOne())

    def test_seperate(self):
        a  = Meta('m','d','f')
        t  = a.table()
        self.assertFalse(a.allInOne())

    # def test_stream(self):
    #     a  = Meta('m','d','f')
    #     t  = a.table()
    #     o  = io.StringIO()
    #     a.stream(o)
    #     e = 'dependent_variables: []\nindependent_variables: []\n'
    #     self.assertEqual(o.getvalue(),e)
        
if __name__ == '__main__':
    unittest.main()

#
# EOF
#
        
