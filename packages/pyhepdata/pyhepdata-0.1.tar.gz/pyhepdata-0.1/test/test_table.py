#!/usr/bin/env python3 
"""Test case for Table

Copyright 2019 Christian Holm Christensen
"""
import math
import unittest
import sys
sys.path.append('..')

from pprint import pprint
from hepdata.table import Table

class TestTable(unittest.TestCase):

    def test_basic(self):
        a = Table()
        i = a.independent('x','xu')
        d = a.dependent  ('y','yu')

        y = [12.345, 1.2345, 0.12345, 0.012345]
        for xx,yy in enumerate(y):
            i.value(value=xx)
            d.value(yy)

        a.assertSizes()

    def test_mismatch(self):
        a = Table()
        i = a.independent('x','xu')
        d = a.dependent  ('y','yu')

        y = [12.345, 1.2345, 0.12345, 0.012345]
        for xx,yy in enumerate(y):
            if xx < 3:
                i.value(value=xx)
            d.value(yy)

        with self.assertRaises(AssertionError):
            a.assertSizes()
        
    def test_select(self):
        a = Table()
        i1 = a.independent('x1','xu')
        i2 = a.independent('x2','xu')
        i3 = a.independent('x3','xu')
        d1 = a.dependent  ('y1','yu')
        d2 = a.dependent  ('y2','yu')
        d3 = a.dependent  ('y3','yu')

        ii,dd = a.select(['x1'],['y1','y2'])
        self.assertEqual(len(ii),1)
        self.assertEqual(len(dd),2)

        ii,dd = a.select(None,['y4'])
        self.assertEqual(len(ii),3)
        self.assertEqual(len(dd),0)

    def _makeTable(self):
        t = Table()
        x = t.independent('x','xu')
        y = t.dependent  ('y','yu')

        for i in range(5):
            x.value(i-.5,i+.5)
            y.value(i).symerror(i/10,'a').asymerror(-i/10,i/5,'b')

        return t, x, y
    
    def test_columns(self):
        t, x, y = self._makeTable()
        
        xe,hx = x.xe(columns=True,header=True)
        ye,hy = y.ye(columns=True,header=True)
        self.assertEqual(xe[0],list(range(5)))
        self.assertEqual(xe[1],    [.5]*5)
        self.assertEqual(ye[0],    list(range(5)))
        self.assertEqual(ye[1],    [x/10 for x in range(5)])
        self.assertEqual(ye[2][1:],[(-x/10,x/5) for x in range(1,5)])
        self.assertEqual(hx,       ('x','xu'))
        self.assertEqual(hy[0],    ('y','yu'))
        self.assertEqual(hy[1:],   ['a','b'])

    def test_columns_pairs(self):
        t, x, y = self._makeTable()
        
        xe = x.xe(columns=True,alwaystuple=True)
        ye = y.ye(columns=True,alwaystuple=True)
        self.assertEqual(xe[0],list(range(5)))
        self.assertEqual(xe[1],[(.5,.5)]*5)
        self.assertEqual(ye[0],list(range(5)))
        self.assertEqual(ye[1],[(-x/10,x/10) for x in range(5)])
        self.assertEqual(ye[2],[(-x/10,x/5) for x in range(5)])
        
    def test_columns_bounds(self):
        t, x, y = self._makeTable()
        
        xe = x.xe(columns=True,bounds=True)
        ye = y.ye(columns=True,bounds=True)
        self.assertEqual(xe[0],list(range(5)))
        self.assertEqual(xe[1],[(-.5+i,.5+i) for i in range(5)])
        self.assertEqual(ye[0],list(range(5)))
        self.assertEqual(ye[1],[(x-x/10,x+x/10) for x in range(5)])
        self.assertEqual(ye[2],[(x-x/10,x+x/5) for x in range(5)])
        
if __name__ == '__main__':
    unittest.main()

#
# EOF
#
        
