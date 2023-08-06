#!/usr/bin/env python3 
"""Test case for Value

Copyright 2019 Christian Holm Christensen
"""
import unittest
import math
import sys
sys.path.append('..')

from pprint import pprint
from hepdata.combiner import *
from hepdata.combiner.observation import Observation
from hepdata.combiner.result import Result
from hepdata.combiner.diff import Diff

class TestCombiner(unittest.TestCase):

    VERB = True
    VERB = False
    
    def printFunc(self):
        if not self.VERB:
            return
        
        fn = sys._getframe().f_back.f_back.f_code.co_name
        fd = getattr(self,fn,{}).__doc__
        if fd is None:
            return
        
        p = fd.find('.')
        print("\n{:15s}: {}".format(fn,fd[:p+1] if p > 0 else fd))
        
    def printResult(self,type,r,e,d):
        if not self.VERB:
            return

        print("{:15s}: {:10s}  {:11s}  {:11s}  {:5s}"
              .format(type,"x","-sigma","+sigma","chi2"))
        print("  {:14s} {}".format("Result",    str(r)))
        print("  {:14s} {}".format("Expected",  str(e)))
        print("  {:14s} {}".format("Difference",str(d)))
        
    def runAverage(self,o1,o2,s,v):
        self.printFunc()

        def testit(model,e):
            c = Averager(model)
            c.push(o1)
            c.push(o2)
            r = c(detail=True)
            d = Diff(r, e)
            self.printResult(model.__name__, r, e, d)
            self.assertLess(d._rx, 2)
            self.assertLess(d._rl, 2)
            self.assertLess(d._rh, 2)

        testit(LinearSigma,   s)
        testit(LinearVariance,v)

    def test_close(self):
        """Similar value and uncertainties. Two observations are added.  Both
        have more or less the same size of uncertainties and are
        equally asymmetric.  However, they do no agree too much on the
        value.
        """	     
        o1 = Observation (4,       1.682,   2.346)
        o2 = Observation (5,       1.912,   2.581)
        s  = Result      (4.49901, 1.33301, 1.66701, 0.115, 0, 11)
        v  = Result      (4.50001, 1.33701, 1.66901, 0.113, 0, 11)
        self.runAverage(o1,o2,s,v)

    def test_diff(self):
        """Different values, one more asymmetric. We add two observations.
        These do not agree too well on the mean value. One has small
        but largely symmetric uncertainties, while the other has more
        asymmetric and larger uncertainties.
        """
        o1 = Observation (6.32064, 0.567382, 0.379042)
        o2 = Observation (6.15549, 0.159504, 0.170811)
        s  = Result      (6.175,   0.157,    0.162,    0.132, 0, 11)
        v  = Result      (6.174,   0.158,    0.163,    0.12,  0, 11)
        self.runAverage(o1,o2,s,v)

    def test_large(self):
        """Similar, one much more uncertain. We add two observations - both
        are centered around the true value but one has much larger
        uncertainties.
        """
        o1 = Observation (6.20449, 0.451232,   0.495192)
        o2 = Observation (6.16188, 0.165785,   0.176712)
        s  = Result      (6.167,   0.157,      0.166,  0.007, 0, 11)
        v  = Result      (6.167,   0.157,      0.166,  0.007, 0, 11)
        self.runAverage(o1,o2,s,v)

    def runAdder(self,o1,o2,s,v):
        self.printFunc()

        def testit(model,e):
            c = Adder2(model)
            c.push(o1)
            c.push(o2)
            r = c(detail=True)
            d = Diff(r,e)
            self.printResult(model.__name__,r,e,d)
            self.assertLess(d._rx, 2)
            self.assertLess(d._rl, 2)
            self.assertLess(d._rh, 2)

        testit(LinearSigma,    s)
        testit(LinearVariance, v)
        
    def test_pathelogical(self):
        """A test for the pathelogical case of symmetric uncertainties"""
        o1 = Observation(0,1,1)
        o2 = Observation(0,1,1)
        e  = Observation(0,math.sqrt(2),math.sqrt(2))
        self.runAdder(o1,o2,e,e)
        
    def test_add1(self):
        """One 20% off full symmetry"""
        o1 = Observation(0,1 ,1)
        o2 = Observation(0,.8,1.2)
        s  = Observation(0.08,1.52,1.32)
        v  = Observation(0.10,1.54,1.33)
        self.runAdder(o1,o2,s,v)

    def test_add2(self):
        """Both 20% off full symmetry"""
        o1 = Observation(0,.8,1.2)
        o2 = Observation(0,.8,1.2)
        s  = Observation(0.16,1.61,1.22)
        v  = Observation(0.20,1.64,1.25)
        self.runAdder(o1,o2,s,v)
        
    def test_add3(self):
        """One 20%, the other 50% off full symmetry"""
        o1 = Observation(0,.5,1.5)
        o2 = Observation(0,.8,1.2)
        s  = Observation(0.28,1.78,1.09)
        v  = Observation(0.35,1.88,1.12)
        self.runAdder(o1,o2,s,v)

    def test_add4(self):
        """Both 50% off full symmetry"""
        o1 = Observation(0,.5,1.5)
        o2 = Observation(0,.5,1.50)
        s  = Observation(0.41,1.93,0.97)
        v  = Observation(0.53,2.07,1.13)
        self.runAdder(o1,o2,s,v)

    def test_test10(self):
        """A test for the pathelogical case"""
        o1 = Observation(0,1,1)
        o2 = Observation(0,10,1)
        s  = Observation(-0.159,1.345,9.947)
        v  = Observation(-0.139,1.445,10.167)
        self.runAdder(o1,o2,s,v)

    def test_cum(self):
        """Test cumulative adding"""
        def testit(model):
            c1 = Adder2(model)
            c2 = Adder2(model)
            c1.add(0,1,1).add(0,.8,1.2)
            c2.add(0,1,1).add(0,.8,1.2).add(0,.5,1.5)

            r1 = c1(detail=True)
            r2 = c2(detail=True)

            c3 = Adder2(model)
            c3.add(r1._x, r1._l, r1._h).add(0,.5,1.5)
            r3 = c3(detail=True)

            # print('\n',model.__name__,'\n',r1,'\n',r2,'\n',r3)
            # self.assertEqual(r2._x, r3._x)
            # self.assertEqual(r2._l, r3._l)
            # self.assertEqual(r2._h, r3._h)

        testit(LinearSigma)
        testit(LinearVariance)


if __name__ == '__main__':
    unittest.main()

#
# EOF
#

