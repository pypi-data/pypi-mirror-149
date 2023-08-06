#!/usr/bin/env python3 
"""Test case for Dependent

Copyright 2019 Christian Holm Christensen
"""
import math
import unittest
import sys
sys.path.append('..')
sys.path.append('.')

from pprint import pprint
from hepdata.dependent import Dependent, Value
from hepdata.rounder import Rounder

class TestDependent(unittest.TestCase):

    def test_basic(self):
        a = Dependent('x','u')
        self.assertEqual(a.name, 'x')
        self.assertEqual(a.units, 'u')
        self.assertEqual(len(a), 0)

        y = [12.345, 1.2345, 0.12345, 0.012345]
        for yy in y:
            a.value(yy)

        self.assertEqual(len(a), len(y))
        self.assertEqual([v[Value.VALUE] for v in a.values], y)
        self.assertEqual(a.y, y)
        self.assertEqual(a.e(), [[]]*len(y))

    def test_qualifiers(self):
        a = Dependent('x','u')
        a.qualifier('A','A')
        a.qualifier('B','B')
        a.qualifier('C','C','C')
        self.assertEqual(len(a.qualifiers()),3)
        self.assertEqual(len(a.qualifiers(['A','C'])),2)
        self.assertEqual(len(a.qualifiers(['NAME','C'])),2)
        self.assertEqual(len(a.qualifiers(lambda q : q.get('units',False))),1)
        
    def test_select(self):
        a = Dependent('x','u')
        a.qualifier('q','Q')
        self.assertEqual(a.select('x'),a)
        self.assertEqual(a.select(['x']),a)
        self.assertEqual(a.select(qualifiers=[{'q':'Q'}]),a)
        self.assertEqual(a.select(qualifiers=[{'q':''}]),a)
        self.assertEqual(a.select(qualifiers=[{'q':None}]),None)
        self.assertEqual(a.select(qualifiers=[{'q':'A'}]),None)
        self.assertEqual(a.select(qualifiers=[{'A':''}]),None)


    def test_more(self):
        a = Dependent('x','u')
        for i in range(5):
            v = a.value(i)
            for j in range(1,4):
                v.symerror(j)

        err = math.sqrt(sum([x**2 for x in range(1,4)]))

        ye = a.ye()
        self.assertEqual(len(ye),5)
        self.assertEqual(len(ye[0]),2)
        self.assertEqual(len(ye[0][1]),3)

        ye = a.ye(Value.sumsq)
        self.assertEqual(len(ye),5)
        self.assertEqual(len(ye[0]),2)
        self.assertEqual(ye[0][1],err)
        
        ye = a.ye(Value.stack,stack_calc=Value.sumsq)
        self.assertEqual(len(ye),5)
        self.assertEqual(len(ye[0]),2)
        self.assertEqual(len(ye[0][1]),3)
        self.assertEqual(ye[0][1][2],err)

        ye = a.ye(Value.stack,stack_calc=Value.linvar)
        self.assertEqual(len(ye),5)
        self.assertEqual(len(ye[0]),2)
        self.assertEqual(len(ye[0][1]),3)
        self.assertEqual(ye[0][1][2],(-err,err))

        ye = a.ye(Value.stack,stack_calc=Value.linvar,columns=True)
        self.assertEqual(len(ye),4)
        self.assertEqual(len(ye[0]),5)
        self.assertEqual(len(ye[1]),5)
        self.assertEqual(len(ye[2]),5)
        self.assertEqual(len(ye[3]),5)

        verb = False 
        if verb:
            print(('\n{:5s} '+'| {:13s}'*3).format('value',*(['uncer']*3)))
            for y,e1,e2,e3 in zip(*ye):
                efmt = '| -{:5.3f} +{:5.3f}'
                print(("{:5.3f} "+efmt*3)
                      .format(y,e1[0],e1[1],e2[0],e2[1],e3[0],e3[1]))

    def test_array(self):
        a   = Dependent('x','u')
        y   = range(10)
        e1  = [.1]*8
        e2l = [.2]*10
        e2h = [.3]*10
        e3  = [.4]*8

        a.value(y)\
         .symerror(e1,label='e1')\
         .asymerror(e2l,e2h,label='e2')\
         .symerror(e3,label='e3',missing=1234)
        
        ye = a.ye()
        self.assertEqual(len(ye),10)
        self.assertEqual(len(ye[0]),2)
        self.assertEqual(len(ye[0][1]),3)
        self.assertTrue(math.isnan(ye[-1][1][0]))
        self.assertEqual(ye[-1][1][2],1234)
        
if __name__ == '__main__':
    unittest.main()

#
# EOF
#
