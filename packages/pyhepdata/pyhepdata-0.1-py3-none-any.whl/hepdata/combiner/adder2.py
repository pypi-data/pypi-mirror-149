"""Add uncertainties using a model

Copyright 2019 Christian Holm Christensen 
"""
import math
from . combiner import Combiner
from . result import Result

class Adder2(Combiner):
    """Combine (add) uncertainties"""
    def __init__(self,model):
        """Constructor"""
        super(Adder2,self).__init__(model)
    
    def __call__(self,n=10,detail=False):
        sm = 0
        sp = 0
        dx = 0
        if len(self._d) > 0:
            sumb = sum([self._m.bias(o)    for o in self._d])
            sumv = sum([self._m.biasVar(o) for o in self._d])
            sums = sum([self._m.skew(o)    for o in self._d])
            sm, sp, dx = self._m.add(n, sumb, sumv, sums)
        if detail:
            return Result(dx,sp,sm,0,0,0)
        return sm, sp, dx

#
# EOF
#
