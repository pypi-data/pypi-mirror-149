"""Linear sigma model 

Copyright 2019 Christian Holm Christensen 
"""
import math
from . observation import Observation

class LinearSigma:
    r"""Combiner linear in the standard deviation.

    A combiner that uses a linear sigma approximation.  This
    is to be used if the combined observations may be correlated,
    in which case this gives and upper bound on the combined
    uncertainty. I.e., in this combiner, we add uncertainties in a
    linear sum
      
    .. math::
         \delta = \sum_i \delta_i

    The method is documented in 

        https://arxiv.org/abs/physics/0306138
        https://arxiv.org/abs/physics/0401042
    
    See also 

        https://arxiv.org/abs/physics/0311105
    
    """
    SQRT_TWOPI = math.sqrt(2*math.pi)
    OFF = -0.6816898449511235
    
    @classmethod
    def w(cls,o):
        """Calculate the weight 

        .. math::
            w = 1 / W
        
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
        # return 1/cls.stepW(0,o)
        return .5 / cls.stepW(0,o)

    @classmethod
    def stepW(cls,guess,o):
        """Calculate the step weight for current value

        .. math::
            W = s / \mathrm{Var}[s]^3
        
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
        s = o.s()
        return s / (s + o.sPrime() * (guess - o._x))**3

    @classmethod
    def stepOffset(cls,guess,o):
        """Calculate the step offset - bias (always 0)

        Parameters
        ----------
        o : Observation 
            not used 
        guess : float 
            not used 
        
        Returns
        -------
        0 : float 
            The step offset
        """        
        return 0

    @classmethod
    def var(cls,guess,o):
        r"""Calculate the variance contribution

        .. math::
            V = \mathrm{Var}[s]^3
        
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
        s = o.s()
        return (s + o.sPrime() * (guess-o._x))**2
        # return o.sVar(guess)**2

    
    @classmethod
    def bias(cls,o):
        r"""Calculate the bias 

        .. math::
            b = (h + l) / \sqrt(2\pi)
        """
        return (o._h - o._l) / cls.SQRT_TWOPI

    @classmethod
    def biasVar(cls,o):
        r"""Calculate variance
        
        .. math::
            0.5 (h^2 + l^2) - b^2 

        """
        return 0.5 * (o._h**2 + o._l**2) - cls.bias(o)**2

    @classmethod
    def skew(cls,o):
        r"""Calculate the skew
        
        .. math::
            (2(h^3 - l^3)  - 1.5(h-l)(h^2+l^2)) / \sqrt(2\pi) + 2 b^3

        """
        l = o._l
        h = o._h
        return (2*(h**3 - l**3) - 1.5*(h - l)*(h**2 + l**2)) / \
            cls.SQRT_TWOPI + 2 * cls.bias(o)**3

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
        d2 = 0
        for _ in range(n):
            d2 = 2 * sumv + d1**2 / math.pi
            d1 = (cls.SQRT_TWOPI * sums - d1**3 * cls.OFF) * 2 / (3 * d2)

        d4 = sumb - d1 / cls.SQRT_TWOPI
        d3 = math.sqrt(2 * d2 - d1**2)
        d5 = 0.5 * (d3 + d1)
        d6 = 0.5 * (d3 - d1)

        return d6, d5, d4
    
    @classmethod
    def l(cls,guess,x,l,h):
        r"""Get the likelihood of `g`

        .. math::
            L(x) = (g - x)^2 / (s + s'(g - x))^2

        where 
        
        .. math::
            s = 2 h l / (h+l)
            s' = (h-l) / (h+l)
        
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
        d   = guess - x

        if math.fabs(d) < 1e-10:
            return 0
    
        tmp = Observation(x,l,h)
        t   = tmp.sVar(guess)
        return (d/t)**2

#
# EOF
#
