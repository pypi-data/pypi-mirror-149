"""Result of combination 

Copyright 2019 Christian Holm Christensen 
"""
from . observation import Observation

class Result(Observation):
    r"""The result of the calculations

    Parameters
    ----------
    x : float
        Value
    l : float
        low error
    h : float
        high error
    chi2 : float 
        :math:`\chi^2`
    low : float 
        Lower bound 
    high : float 
        Upper bound 
    """
    def __init__(self,x,l,h,chi2,low,high):
        """Constructor 

        """
        super(Result,self).__init__(x,l,h)
        self._chi2 = chi2
        self._low  = low
        self._high = high

    def low(self):
        """Get the lower bound
        
        Returns
        -------
        low : float 
            Lower bound 
        """
        return self._low

    def high(self):
        """Get the upper bound
        
        Returns
        -------
        high : float 
            Upper bound 
        """
        return self._high

    def __str__(self):
        """String representation 
        
        Returns
        -------
        s : str 
            String representation 
        """
        return super(Result,self).__str__()\
            + "  {:5.2f}".format(self._chi2)

#
# EOF
#

