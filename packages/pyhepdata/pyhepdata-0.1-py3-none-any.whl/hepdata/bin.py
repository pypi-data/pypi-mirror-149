"""A single independent variable value 

Copyright 2019 Christian Holm Christensen
"""
from hepdata.accepts import accepts
from hepdata.rounder import Rounder
from hepdata.utils import _ensureList

class Bin:
    """Define an independent value.

    Either both of low and high should be given, or value should
    be given.
    
    Test case
    ---------
    - `test_bin.py`
    
    Parameters
    ----------
    low : float (optional)
        Lower bound 
    high  : float (optional)
        Upper bound 
    value : float or str (optional)
        'Centre' value

    """
    #: Low field name
    LOW = 'low'
    #: High field name
    HIGH = 'high'
    #: Value field name
    VALUE = 'value'
    
    @accepts(low=float,high=float,value=(float,str))
    def __init__(self,low=None,high=None,value=None): 
        assert (low is not None and high is not None) or value is not None,\
            "Either both low and high or a value must be given"

        self._d = {}
        if low is not None:
            self._d[self.LOW] = low
        if high is not None:
            self._d[self.HIGH] = high
        if value is not None:
            self._d[self.VALUE] = value

    def low(self):
        """Return the low value. 

        If no lower bound is given, return the centre point 
        """
        if self.LOW in self._d:
            return self._d[self.LOW]
        return float(self._d.get(self.VALUE))

    def high(self):
        """Return the high value. 

        If no higher bound is given, return the centre point 
        """
        if self.HIGH in self._d:
            return self._d[self.HIGH]
        return float(self._d.get(self.VALUE))

    def x(self):
        """Return the value.  
        
        If the centre point is given, return that.  Otherwise, we take
        the mid-point between the low and high values.

        Returns
        -------
            x : float 
                The "centre" point 
        """
        if self.VALUE in self._d:
            return float(self._d[self.VALUE])

        return (self._d[self.HIGH]+self._d[self.LOW])/2

    value = x
    
    def e(self,**kwargs):
        """Get the uncertainty on the point.  

        If no lower and upper bounds are given, return 0.

        If only lower and uppper bounds are given, return the
        half-distance between the two.

        If lower and upper bounds as well as centre value is given,
        return a tuple of distances (2) between lower and upper bounds
        to central value.

        Returns
        -------
            uncer : float or (float,float)
                Uncertainty on point
        """
        alwaystuple = kwargs.get('alwaystuple',False)

        if self.LOW not in self._d:
            if alwaystuple:
                return 0,0
            return 0

        if self.VALUE not in self._d:
            r = (self._d[self.HIGH]-self._d[self.LOW])/2
            if alwaystuple:
                return (r,r)
            return r

        return (float(self._d[self.VALUE])-self._d[self.LOW],
                self._d[self.HIGH]-float(self._d[self.VALUE]))

    def xe(self,**kwargs):
        """Get 'midpoint' and uncertainties 

        Parameters
        ----------
        **kwargs : keyword arguments 
            Keyword arguments 
        
            - alwaystuple : bool 
                If True, always return uncertainty as a two-tuple 
            - bounds : bool 
                If True, return uncertainty as bounds 
        Returns
        -------
            x : float 
                Midpoint value 
            e : float or (float,float)
               Uncertainties or bounds 
        """
        bounds = kwargs.get('bounds',False)
        if bounds:
            kwargs['alwaystuple'] = True
            
        x = self.x()
        e = self.e(**kwargs)
        if bounds:
            return x, (x-e[0],x+e[1])

        return x, e
        
    @accepts(n=int)
    def round(self,n):
        """Round value and uncertainties to n digits


        Parameters
        ----------
            - n : int, positive 
              Number of digits
        
        Returns
        -------
            - self : Value 
              Reference to self 
        """
        for k in (self.LOW,self.HIGH,self.VALUE):
            if k in self._d:
                self._d[k] = round(self._d[k],n)
                
        return self

    @accepts(n=int)
    def roundNsig(self,n):
        """Round smallest uncertainty to n significant digits and 
        give the rest of the values to the same precsion

        Parameters
        ----------
            - n : int, positive 
              Number of siginificant digits 
        
        Returns
        -------
            - self : Value 
              Reference to self 
        """
        _, rd = Rounder.roundResult(0,list(self._d.values()),n)
        for k,v in zip(self._d.keys(),_ensureList(rd)):
            self._d[k] = v

        return self

    def sync(self):
        """Synchronise value and text representations"""
        pass
#
# EOF
#
