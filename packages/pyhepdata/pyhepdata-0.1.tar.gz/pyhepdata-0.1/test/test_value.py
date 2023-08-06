#!/usr/bin/env python3 
"""Test case for Value

Copyright 2019 Christian Holm Christensen
"""
import unittest
import math
import sys
sys.path.append('..')

from pprint import pprint
from hepdata.value import Value

class TestValue(unittest.TestCase):

    #VERB = True
    #VERB = False
    
    def test_basic(self):
        a = Value(0)
        self.assertEqual(a.value(),0)
        self.assertEqual(a.e(), [])

        a.symerror(1)
        self.assertEqual(a.e()[0],1)

        a.asymerror(1,2)
        self.assertEqual(a.e(),[1,(1,2)])
        
    def test_round(self):
        a = Value(12.3456)
        
        a.symerror(1.23456)
        a.symerror(0.123456)
        a.symerror(0.0123456)
        a.roundNsig(2)
        
        
        self.assertEqual(a.y(),12.346)
        self.assertEqual(a.e(),[1.235,0.123,0.012])

        # if self.VERB:
        #     print(a.y(),a.e())

    def test_sumsq(self):
        a = Value(12.3456)
        e = [1.23456, 0.123456, 0.0123456]
        for ee in e:
            a.symerror(ee)

        exp = math.sqrt(sum(map(lambda x: x**2,e)))
        res = a.e(Value.sumsq)
        self.assertEqual(res,exp)

        a.asymerror(e[-1],e[-1])
        exp = math.sqrt(sum(map(lambda x: x**2,e+[e[-1]])))
        res = a.e(Value.sumsq)
        self.assertEqual(res,exp)

        with self.assertRaises(ValueError):
            a.asymerror(e[-1],e[-1]+.001)
            self.assertEqual(a.e(Value.sumsq),exp)
        
    def test_linstd(self):
        a = Value(12.3456)
        e = [1.23456, 0.123456, 0.0123456]
        for ee in e:
            a.symerror(ee)
        a.asymerror(-e[0],e[0]+.1)
        res,d = a.e(Value.linstd,delta=True)
        exp = (-1.76, 1.812)

        for r,e in zip(res,exp):
            self.assertAlmostEqual(r,e,3)
        self.assertAlmostEqual(d,0.019,3)
        
    def test_linvar(self):
        a = Value(12.3456)
        e = [1.23456, 0.123456, 0.0123456]
        for ee in e:
            a.symerror(ee)
        a.asymerror(-e[0],e[0]+.1)
        res,d = a.e(Value.linvar,delta=True)
        exp   = (-1.761, 1.813)

        for r,e in zip(res,exp):
            self.assertAlmostEqual(r,e,3)
        self.assertAlmostEqual(d,0.024,3)

    def test_filter(self):
        a = Value(12.3456)
        e = [1.23456, 0.123456, 0.0123456, 10]
        l = ['a', 'b', 'c', 'd']
        for ee,ll in zip(e,l):
            a.symerror(ee,ll)

        exp =  math.sqrt(sum(map(lambda x : x**2, e[:-1])))
        res = a.e(Value.withlabel,label_calc=Value.sumsq,labels=['a','b','c'])
        self.assertEqual(res,exp)

        exp = e[0]
        res = a.e(lambda errors,value :
                  Value.withlabel(errors,value,label_calc=Value.sumsq,
                                  labels='a'))
        self.assertEqual(res,exp)

        exp = math.sqrt(sum(map(lambda x : x**2, e[1:])))
        res = a.e(Value.withlabel,label_calc=Value.sumsq,
                  labels=lambda l : l != 'a')
        self.assertEqual(res,exp)

    def test_stack(self):
        a = Value(1)
        for i in range(1,5):
            a.symerror(1)

        exp = [math.sqrt(i*1**2) for i in range(1,5)]
        res = a.e(Value.stack,stack_calc=Value.sumsq)
        self.assertEqual(res,exp)

        a = Value(1)
        a.symerror(1)
        a.asymerror(-.8,1.2)
        a.symerror(.5)
        res = a.e(Value.stack,stack_calc=Value.linvar)

        from hepdata.combiner.adder2 import Adder2
        from hepdata.combiner.linear_variance import LinearVariance
        
        c = Adder2(LinearVariance)
        c.add(1,1,1).add(1,.8,1.2).add(0,.5,.5)
        l, h, _ = c()
        self.assertEqual(res[-1],(-l,h))

    def test_filter_stack(self):
        a = Value(12.3456)
        e = [1.23456, 0.123456, 0.0123456, 10]
        l = ['a', 'b', 'c', 'd']
        for ee,ll in zip(e,l):
            a.symerror(ee,ll)

        exp = math.sqrt(sum([ee**2 for ee in e[:-1]]))
        res = a.e(Value.withlabel, labels=['a','b','c'],
                  label_calc=Value.stack,
                  stack_calc=Value.sumsq)

        self.assertEqual(res[-1],exp)


    def test_ye(self):
        a = Value(12.3456)
        e = [1.23456, 0.123456, 0.0123456]
        for ee in e:
            a.symerror(ee)
        a.asymerror(-e[0],e[0]+.1)
        y, e = a.ye(Value.linstd)
        expy = a.y()+0.019
        expe = (-1.76, 1.812)

        for r,ee in zip(e,expe):
            self.assertAlmostEqual(r,ee,3)
        self.assertAlmostEqual(y,expy,3)
        
if __name__ == '__main__':
    unittest.main()

#
# EOF
#
