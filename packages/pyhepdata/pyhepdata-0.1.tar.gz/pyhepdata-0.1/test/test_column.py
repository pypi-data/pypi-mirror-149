#!/usr/bin/env python3 
"""Test case for Column

Copyright 2019 Christian Holm Christensen
"""
import unittest
import sys
sys.path.append('..')

from pprint import pprint
from hepdata.column import Column
from hepdata.rounder import Rounder

class Data:
    """A dummy data type 

    Parameters
    ----------
    x : float 
        The data to store 
    """
    def __init__(self,x=0):
        self._d = [x]
        self._t  =[f'{x}']

    def round(self,n):
        """Round to n decimal places"""
        self._d[0] = round(self._d[0], n)
        self._t[0] = f'{self._d[0]}'

    def roundNsig(self,n):
        """Round to n significant digits"""
        self._d[0] = Rounder.round(self._d[0], n)
        self._t[0] = f'{self._d[0]}'

class A(Column):
    """A dummy column type 

    Parameters
    ----------
    n : str
        Column name 
    u : str 
        Column unit 
    """
    def __init__(self,n,u=None):
        super(A,self).__init__(n,u)

    def add(self,x):
        """Add a value"""
        self._append(Data(x))
        
class TestColumn(unittest.TestCase):
    """Test of hepdata.Column"""
    
    def test_basic(self):
        """Test basic Column stuff"""
        a = A('x','u')
        self.assertEqual(a.name, 'x')
        self.assertEqual(a.units, 'u')
        self.assertEqual(len(a), 0)

        x = [12.345, 1.2345, 0.12345, 0.012345]
        for xx in x:
            a.add(xx)

        self.assertEqual(len(a), len(x))
        self.assertEqual([v[0] for v in a.values], x)

    def test_round(self):
        """Test round Column data to decimal places"""
        a = A('x','u')
        x = [12.345, 1.2345, 0.12345, 0.012345]
        for xx in x:
            a.add(xx)

        a.round(2)
        r = [round(xx,2) for xx in x]
        self.assertEqual([v[0] for v in a.values], r)

    def test_roundNsig(self):
        """Test round Column data to significant digits"""
        a = A('x','u')
        x = [12.345, 1.2345, 0.12345, 0.012345]
        for xx in x:
            a.add(xx)

        a.roundNsig(2)
        r = [Rounder.round(xx,2) for xx in x]
        self.assertEqual([v[0] for v in a.values], r)
        
        
if __name__ == '__main__':
    unittest.main()

#
# EOF
#
