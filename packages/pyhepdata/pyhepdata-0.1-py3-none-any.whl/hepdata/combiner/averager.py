"""Combine results 

Copyright 2019 Christian Holm Christensen
"""
import math
from . combiner import Combiner
from . result import Result

class Averager(Combiner):
    """Combine (average) measurments"""
    def __init__(self,model):
        """Constructor"""
        super(Averager,self).__init__(model)

    def res(self,guess,r):
        """Get the residual contribution from a single term 

        Parameters
        ----------
            guess : float 
                Current guess 
            r : Observation 
                Current observation 
        
        Returns
        -------
            chi2 : float 
                Chi-square contribution
        """
        var = self._m.var(guess,r)
        if var < 0:
            return -1000

        return (guess - r._x)**2 / var

    def f(self,guess,chi2):
        """Get change in chi-square 

        Parameters
        ----------
            guess : float 
                Current guess 
            chi2 : float 
                current chi-square 

        Returns
        -------
            change : float 
                Change in chi-square from guess 
        """
        if len(self._d) == 1:
            return 1

        return sum([self.res(guess,r) for r in self._d])-chi2

    def e(self,n,sign,best,chi2,s):
        """Calculate the one-sided uncertainty 
        
        Parameters
        ----------
            n : int 
                Number of iterations 
            sign : int 
                direction to get error in 
            best : float 
                Current best guess at value 
            chi2 : float 
                Current chi-square 
            s : float 
        
        Returns
        -------
            e : float 
                Estimate of uncertainty 
        """
        if len(self._d) == 1:
            return self._d[0]._l if sign < 0 else self._d[1]._h

        delta = 0.1 * sign * s

        for i in range(n):
            got = self.f(best + sign * s, chi2)

            if math.fabs(got-1) < 1e-7:
                break

            guess = self.f(best + sign * s + delta, chi2)

            if (got-1) * (guess - 1) > 0:
                if (got-1) / (guess - 1) < 1:
                    delta *= -1
                else:
                    s += sign * delta

                continue

            s += sign * delta * (1-got) / (guess - got)
            delta /= 2

        return s

    def x(self,n,lowest,highest):
        """Calculate the value
        
        Parameters
        ----------
            n : int 
                Number of iterations 
            lowest : float 
                Lowest value 
            highest : float 
                Highest value 
        
        Returns
        -------
            x : float 
                Estimate of value
        """
        if len(self._d) == 1:
            return self._d[0]._x

        x = (highest+lowest)/2
        oldx = -1e33

        for i in range(n):
            sumx = 0
            sumw = 0
            off  = 0

            w    = [self._m.stepW(x, o) for o in self._d]
            off  = sum([self._m.stepOffset(x, o) for o in self._d])
            sumx = sum([ww * o._x for ww,o in zip(w,self._d)])
            sumw = sum(w)

            x = (sumx - off) / sumw if math.fabs(sumw) > 1e-9 else 0

            if math.fabs(x-oldx) < (highest-lowest) * 1e-9:
                break

            oldx = x

        return x

    def __call__(self,n=50,detail=False):
        """Perform the calculations 
        
        Parameters
        ----------
            n : int 
               number of iterations 
            details : bool 
               If true, return full details 
        
        Returns
        -------
             result : tuple or Result 
                 If details is true, return the full result object.  
                 Otherwise return found value and uncertainties 
        """
        lowest   = min([o.low()  for o in self._d])
        highest  = max([o.high() for o in self._d])
        sumLow   = sum([1/o._l**2  for o in self._d if o._l > 1e-10])
        sumHigh  = sum([1/o._h**2  for o in self._d if o._h > 1e-10])
        sLow     = 1/math.sqrt(sumLow)  if sumLow  > 1e-10 else 0
        sHigh    = 1/math.sqrt(sumHigh) if sumHigh > 1e-10 else 0

        bestX    = self.x(n,lowest,highest)
        bestChi2 = self.f(bestX,0)
        bestLow  = math.fabs(self.e(n,-1,bestX,bestChi2,sLow))
        bestHigh = math.fabs(self.e(n,+1,bestX,bestChi2,sHigh))

        if detail:
            return Result(bestX,bestLow,bestHigh,bestChi2,lowest,highest)
        return bestX,bestLow,bestHigh



#
# EOF
#
