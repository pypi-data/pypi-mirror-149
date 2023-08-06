"""Base class for various kinds of combiners 

Copyright 2019 Christian Holm Christensen
"""
from . observation import Observation

class Combiner:
    """Base class for combiners"""
    def __init__(self,model):
        """Constructor

        Parameters
        ----------
            model : class 
                Model to use (LinearSigma or LinearVariance)
        """
        self._d = []
        self._m = model

    def push(self,o):
        """Add and observation"""
        self._d.append(o)
        return self

    def add(self,x,l,h):
        """Add an observation"""
        return self.push(Observation(x,l,h))
#
# EOF
#
