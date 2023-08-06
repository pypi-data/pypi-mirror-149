#!/usr/bin/env python3 
"""Test case for Resource

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')

from hepdata.resource import Resource

class TestResource(unittest.TestCase):

    def test_full(self):
        a = Resource('a','b','c')
        e = {Resource.LOCATION: 'a',
             Resource.DESCRIPTION: 'b',
             Resource.TYPE: 'c'}

        self.assertEqual(a._d,e)

    def test_empty(self):
        with self.assertRaises(Exception):
            a = Resource()
        
if __name__ == '__main__':
    unittest.main()

#
# EOF
#
