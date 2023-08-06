"""Add uncertainties using a model

Copyright 2019 Christian Holm Christensen 
"""
import math
from . combiner import Combiner
from . result import Result

class Adder(Combiner):
    """Combine (add) uncertainties"""
    def __init__(self,model):
        """Constructor"""
        super(Adder,self).__init__(model)

    def f(self,x,sign,step):
        w    = [self._m.w(o) for o in self._d]
        sumw = sum(w)
        for o,ww in zip(self._d,w):
            o._x += sign*step * ww

        return sum([o._x**2 / self._m.var(x,o) for o in self._d])
                
        
    def e(self,sign,step,end):

        for o in self._d:
            o._x = 0

        x     = 0
        oldff = 0
        while sign * x < end:
            ff = self.f(x,sign,step)

            x += sign * step

            if ff > 1 and oldff < 1:
                s  = x - step * (ff - 1) / (ff - oldff)

            oldff = ff

        return s
        
    def __call__(self,fac=0.0001,detail=False):
        """Perform the calculation 
        
        Parameters:
        -----------
            fac : factor 
                Fraction of range to use as step size
        """
        lowest  = 3*math.sqrt(sum([o.low()**2 for o in self._d]))
        highest = 3*math.sqrt(sum([o.low()**2 for o in self._d]))
        step    = fac * (highest+lowest)
        l       = self.e(-1,step,lowest)
        h       = self.e(+1,step,highest)

        if detail:
            return Result(0,l,h,0,lowest,highest)
        return l,h
#
# EOF
#
