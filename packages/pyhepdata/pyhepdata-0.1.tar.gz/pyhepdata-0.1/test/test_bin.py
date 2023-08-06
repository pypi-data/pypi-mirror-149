#!/usr/bin/env python3 
"""Test case for Bin

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')

from pprint import pprint
from hepdata.bin import Bin

class TestBin(unittest.TestCase):

    def test_low_high(self):
        a = Bin(0,1)
        self.assertEqual(a.low(),0)
        self.assertEqual(a.high(),1)
        self.assertEqual(a.value(),0.5)
        self.assertEqual(a.e(),0.5)
        self.assertEqual(a.xe(),(.5,.5,))
        self.assertEqual(a.xe(alwaystuple=True),(.5,(.5,.5)))
        self.assertEqual(a.xe(bounds=True),(.5,(0,1)))
        self.assertEqual(a.xe(bounds=True,alwaystuple=True),(.5,(0,1)))
        
    def test_value(self):
        a = Bin(value=1)
        self.assertEqual(a.low(),a.high())
        self.assertEqual(a.value(),1)
        self.assertEqual(a.e(),0)
        self.assertEqual(a.xe(),(1,0))
        self.assertEqual(a.xe(alwaystuple=True),(1,(0,0)))
        self.assertEqual(a.xe(bounds=True),(1,(1,1)))
        self.assertEqual(a.xe(bounds=True,alwaystuple=True),(1,(1,1)))

    def test_low_value_high(self):
        a = Bin(low=0,value=1,high=3)
        self.assertEqual(a.low(),0)
        self.assertEqual(a.high(),3)
        self.assertEqual(a.value(),1)
        self.assertEqual(a.e(),(1,2))

        self.assertEqual(a.xe(),(1,(1,2)))
        self.assertEqual(a.xe(alwaystuple=True),(1,(1,2)))
        self.assertEqual(a.xe(bounds=True),(1,(0,3)))
        
        
        
if __name__ == '__main__':
    unittest.main()

#
# EOF
#
