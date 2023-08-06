#!/usr/bin/env python3 
"""Test case for Licensed

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')

from pprint import pprint 
from hepdata.licensed import Licensed

class A(Licensed):
    def __init__(self):
        super(A,self).__init__()

    def license(self,name=None,url=None,description=None):
        return self._license(name,url,description)

class TestLicensed(unittest.TestCase):

    def test_full(self):
        a = A()
        l = a.license('a','b','c')
        e = {Licensed.NAME: 'a',
             Licensed.URL: 'b',
             Licensed.DESCRIPTION: 'c'}

        self.assertEqual(l,e)

    def test_partial(self):
        a = A()
        l = a.license('a',description='c')
        e = {Licensed.NAME: 'a',
             Licensed.DESCRIPTION: 'c'}

        self.assertEqual(l,e)
        self.assertFalse(Licensed.URL in l)
        
if __name__ == '__main__':
    unittest.main()

#
# EOF
#
