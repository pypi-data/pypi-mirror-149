"""Difference between observations (or results)

Copyright 2019 Christian Holm Christensen 
"""
from . observation import Observation

class Diff(Observation):
    """Difference between two results - mainly for tests"""
    def __init__(self,r,e):
        super(Diff,self).__init__(e._x    - r._x,
                                  e._l    - r._l,
                                  e._h    - r._h)
        self._rx = self._x / e._x * 100 if e._x != 0 else 0
        self._rl = self._l / e._l * 100 if e._l != 0 else 0
        self._rh = self._h / e._h * 100 if e._h != 0 else 0

    def __str__(self):
        """String representation 
        
        Returns
        -------
           s : str 
               String representation 
        """
        rel = True
        if rel:
            return "{:9.3f}%  {:10.3f}% {:10.3f}%"\
                .format(self._rx,self._rl,self._rh)
        else:
            return "{:10.3f}  {:11.5f} {:11.5f}"\
                .format(self._x,self._l,self._h)

#
# EOF
#
