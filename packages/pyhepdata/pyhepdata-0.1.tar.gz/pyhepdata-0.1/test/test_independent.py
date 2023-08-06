#!/usr/bin/env python3 
"""Test case for Independent

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')
sys.path.append('.')

from pprint import pprint
from hepdata.independent import Independent, Bin
from hepdata.rounder import Rounder

class TestIndependent(unittest.TestCase):

    def test_basic(self):
        a = Independent('x','u')
        self.assertEqual(a.name, 'x')
        self.assertEqual(a.units, 'u')
        self.assertEqual(len(a), 0)

        x = [12.345, 1.2345, 0.12345, 0.012345]
        for xx in x:
            a.value(value=xx)

        self.assertEqual(len(a), len(x))
        self.assertEqual([v[Bin.VALUE] for v in a.values], x)
        self.assertEqual(a.x,   x)
        self.assertEqual(a.e(), [0]*len(x))

    def test_low_high(self):
        a = Independent('x','u')

        x = range(11)
        for l, h in zip(x[:-1],x[1:]):
            a.value(l,h)

        m = [(h+l)/2 for l,h in zip(x[:-1],x[1:])]
        e = [(h-l)/2 for l,h in zip(x[:-1],x[1:])]

        self.assertEqual(len(a),len(x)-1)
        self.assertEqual(a.x,   m)
        self.assertEqual(a.e(), e)

    def test_low_value_high(self):
        a = Independent('x','u')

        x = range(0,22,3)
        for l, h in zip(x[:-1],x[1:]):
            a.value(l,h,h-1)

        m = [h-1 for h in x[1:]]
        e = [(v-l,h-v) for l,v,h in zip(x[:-1],m,x[1:])]

        self.assertEqual(len(a),len(x)-1)
        self.assertEqual(a.x,   m)
        self.assertEqual(a.e(), e)
        
    def test_array(self):
        a = Independent('x','u')
        a.value(range(4), range(1,5))
        xe = a.xe()
        self.assertEqual(xe[0][0], 0.5)
        self.assertEqual([x[1] for x in xe],[.5]*4)
        
        a = Independent('x','u')
        a.value(range(0,12,3), range(3,15,3),range(1,11,3))
        xe = a.xe()
        self.assertEqual([x[0] for x in xe],list(range(1,13,3)))
        self.assertEqual([len(x[1]) for x in xe],[2]*4)

        a = Independent('x','u')
        a.value(value=range(0,8,2))
        xe = a.xe()
        self.assertEqual([x[0] for x in xe],list(range(0,8,2)))
        self.assertEqual([x[1] for x in xe],[0]*4)
        
if __name__ == '__main__':
    unittest.main()

#
# EOF
#
