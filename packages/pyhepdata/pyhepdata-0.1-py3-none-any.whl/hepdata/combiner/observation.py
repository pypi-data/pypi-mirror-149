"""A single observation 

Copyright 2019 Christian Holm Christensen 
"""
import math

class Observation:
    """A single observation

    Parameters
    ----------
    x : float
        Value
    l : float
        low error.  Note, a positive value indicates a lower bound 
        _smaller_ than `x`.  This convention is _opposite_ to HepData 
    h : float. 
        high error. Note, a positive value indicates an upper bound 
        _larger_ than `x`. 
    """
    def __init__(self,x,l,h):
        self._x = x
        self._l = l
        self._h = h

    def s(self):
        """Calculate 

        .. math::
            s = 2 l h / (l + h)
        
        Returns
        -------
            s : float 
        """
        if self._l * self._h == 0:
            return 0
        return 2 * self._l * self._h / (self._l + self._h)

    def sPrime(self):
        """Calculate 

        .. math::
            s' = (l - h) / (l + h)
        
        Returns
        -------
            s' : float 
        """
        if math.fabs(self._l + self._h) < 1e-9:
            return 0
        return (self._h - self._l) / (self._h + self._l)

    def sVar(self,guess=0):
        r"""Calculate 

        .. math::
            \mathrm{Var}[s] = s + s' (g - x)
        
        Returns
        -------
            Var[s] : float 
        """
        return self.s() + self.sPrime() * (guess - self._x)

    def v(self):
        """Calculate 

        .. math::
           v = l h
        
        Returns
        -------
            v : float 
        """
        return self._l * self._h

    def vPrime(self):
        """Calculate 

        .. math::
           v' = h - l
        
        Returns
        -------
            v' : float 
        """
        return self._h - self._l

    def low(self):
        """Calculate 
        
        .. math::
            L = x - 3 l 
        
        Returns 
        -------
            L : float 
        """
        return self._x - 3 * self._l

    def high(self):
        """Calculate 
        
        .. math::
            H = x + 3 h
        
        Returns 
        -------
            H : float 
        """
        return self._x + 3 * self._h

    def __str__(self):
        """String representation 
        
        Returns
        -------
           s : str 
               String representation 
        """
        return "{:10.8f}  -{:10.8f} +{:10.8f}".format(self._x,self._l,self._h)

#
# EOF
#
