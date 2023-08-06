"""Linear variance model 

Copyright 2019 Christian Holm Christensen 
"""
import math
from . observation import Observation

class LinearVariance:
    r"""Linear in the variance

     A combiner that uses a linear variance approximation.  This is
     to be used if the observations are known to be
     uncorrelated. I.e., in this combiner, we add uncertainties in
     quadrature
      
     .. math::
        \delta^2 = \sum_i \delta_i^2

    The method is documented in 

        https://arxiv.org/abs/physics/0306138
        https://arxiv.org/abs/physics/0401042

    See also 

        https://arxiv.org/abs/physics/0311105
    
    """
    @classmethod
    def w(cls,o):
        """Calculate the weight 

        .. math::
           w = (v + x v')^2 / (2 v + x v')$
        
        for observation 
        
        Parameters
        ----------
            o : Observation 
               Current observation 
        
        Returns
        -------
            w : float 
               The weight
        """
        v  = o.v()
        vp = o.vPrime()
        return (v + o._x * vp)**2 / (2 * v + o._x * vp)

    @classmethod
    def stepW(cls,guess,o):
        """Calculate the weight for observation, given curent value 

        .. math::
            W = v / (v + v' (g - x))^2
        
        for observation 
        
        Parameters
        ----------
        o : Observation 
           Current observation 
        guess : float 
           not used 
        
        Returns
        -------
        W : float 
            The step weight
        """
        v = o.v()
        return v / (v + o.vPrime() * (guess - o._x))**2

    @classmethod
    def stepOffset(cls,guess,o):
        r"""Calculate the step offset - bias 
        
        .. math::
            \delta = 1/2 v' (g - x)^2 / (v + v' (g - x))^2

        Parameters
        ----------
        o : Observation 
           Current observation
        guess : float 
           Current valie 
        
        Returns
        -------
        delta : float 
           The step offset
        """        
        vp = o.vPrime()
        d  = (guess - o._x)
        return 0.5 * vp * (d / (o.v() + vp * d))**2

    @classmethod
    def var(cls,guess,o):
        """Calculate the variance contribution

        .. math::
            V = v + v' (g - x)
        
        for observation 
        
        Parameters
        ----------
        o : Observation 
           Current observation 
        guess : float 
           Current guess 
        
        Returns
        -------
        V : float 
            The variance contribution
        """
        return o.v() + o.vPrime() * (guess - o._x)

    @classmethod
    def bias(cls,o):
        """Calculate the bias 

        .. math::
            b = (h - l) / 2

        """
        return (o._h - o._l) / 2

    @classmethod
    def biasVar(cls,o):
        """Calculate variance
        
        .. math::
            0.25 (h + l)^2 + 0.5 (h - l)^2

        """
        return 0.25 * (o._h + o._l)**2 + 0.5 * (o._h - o._l)**2

    @classmethod
    def skew(cls,o):
        """Calculate the skew
        
        .. math::
            0.75 (h + l)^3 + (h - l)^3

        """
        d = (o._h - o._l)
        return 0.75 * (o._h + o._l)**2 * d + d**3

    @classmethod
    def add(cls, n, sumb, sumv, sums):
        """For propagation of uncertainties 

        Parameters
        ----------
        n : int
            Number of iterations 
        sumb : float 
            Sum of biases 
        sumv : float 
            Sum of variances 
        sums : float 
            Sum of skews 
        
        Returns
        -------
        l : float
            low uncertainty 
        h : float 
            high uncertainty 
        x : float 
            Value
        """
        d1 = 0
        if math.fabs(sumv) < 1e-9:
            return 0,0,0
        
        for _ in range(n):
            d1 = sums / (6 * sumv - 4 * d1**2)

        d3 = math.sqrt(sumv - 2 * d1**2)
        d4 = sumb - d1
        d5 = d3 + d1
        d6 = d3 - d1

        return d6, d5, d4
    
    @classmethod
    def l(cls,guess,x,l,h):
        """Get the likelihood of `g` 

        .. math::
            L(x) = (g - x)^2 / (v + v' (g - x))

        where 
        
        .. math::
            V = h l 
            V' = h - l
        
        Parameters
        ----------
        guess : float 
            Current value 
        x : float 
            Position
        l : float 
            Lower bound 
        h : float 
            Upper bound 
        
        Returns
        -------
        l : float 
            likelihood 
        """
        d  = guess - x
        v  = h * l
        vp = e - l
        return d**2 / (v + vp * d)

#
# EOF
#
