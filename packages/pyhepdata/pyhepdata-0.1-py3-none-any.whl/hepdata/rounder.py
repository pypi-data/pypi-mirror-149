"""Module to do rounding of values 

Copyright 2019 Christian Holm Christensen
"""
import math
from . utils import _ensureList

class Rounder:
    """Utility class to round results

    Test case
    ---------
    - ``test_rounder.py``

    """
    @classmethod
    def round(cls,v,n=0,no_v_exponent=False):
        """Round all values in v to n significant digits"""
        if v is None:
            return None

        vv   = _ensureList(v)
        nn   = _ensureList(n)
        if len(nn) == 1:
            nn *= len(vv)
        elif len(nn) != len(vv):
            raise ValueError('Inconsistent sizes of values {} and '
                             'number of significant digits {}'
                             .format(len(vv),len(nn)))

        vexp = [0]*len(vv) if no_v_exponent else \
            [int(math.floor(math.log10(math.fabs(v)))+1)
             if math.isfinite(v) and v > 0 else 0 for v in vv]
        tens = [math.pow(10.,-int(n)+ve) for n,ve in zip(nn,vexp)]
        ww   = [0 if math.isnan(v) else math.floor(100*math.fabs(v)/ten+0.00001)
                for v,ten in zip(vv,tens)]
        mm   = [w // 100 for w in ww]
        nxt  = [int(w) % 100 for w in ww]
        mm   = [m+1 if (nx>50) or (nx==50 and (m%2)==1) else m
                for m,nx in zip(mm,nxt)]
        ret  = [math.nan if math.isnan(v) else
                # Extra stdlib round to kick off extra digits
                round(math.copysign(m,v) * ten, -int(math.log10(ten)))
                for m,v,ten in zip(mm,vv,tens)]
        if len(ret) == 1:
            return ret[0]
        return ret

    @classmethod
    def _flatten(cls,v):
        """Could probably be done with a generator"""
        if v is None:
            return None

        try:
            rr = []
            for e in iter(v):
                rr += cls._flatten(e)

            return rr
        except:
            return [v]
                
    
    @classmethod
    def roundResult(cls,x,dx,n=2,alsoPrec=False):
        """Round lowest uncertainty to n significant digits and 
        give remaining values to the same precision

        Parameters
        ----------
        x : float, or collection of float 
            Value 
        dx : float, or collection of float or pairs of floats 
           Uncertainties 
        n : int or list of int 
           How many significant digits to round to 
        alsoPrec : bool 
           If true, also returns precision rounded to 
        
        Returns
        -------
        rx : float or collection of float 
            Rounded value 
        rd : float or collection of float
            Rounded uncertainties 
        exp : int or list of int
            Precision rounded to if `alsoPrec` is `True` 
        
        """
        eps = 1e-15
        dd  = cls._flatten(dx)
        if dd is None or len(dd) <= 0:
            dd = _ensureList(x)

        def _inner(xx,ee,nsign=n):
            ll = [math.ceil(math.log10(math.fabs(e))+eps)
                  for e in ee if e != 0 and math.isfinite(e)]
            if len(ll) <= 0:
                return xx,n
            mm = int(min(ll))-nsign
            return cls.round(xx,-mm,True),mm

        rd,md = _inner(dd,dd)
        rx,mm = _inner(x, _ensureList(rd))
        rd,mm = _inner(rd,_ensureList(rd))  # Re-round uncertainties as we might
                               # have rounded up

        if alsoPrec:
            return rx, rd, mm
        
        return rx, rd

    @classmethod
    def textResult(cls,x,dx,n=2,):
        """Rounds result to given number of significant digits on the least
        significant uncertainty and gives the value and other
        uncertainties with the same precision.  Then the numbers are
        formatted as string with the given precision.  This allows for
        somewhat exact representation on output

        Parameters
        ----------
        x : float, or collection of float 
            Value 
        dx : float, or collection of float or pairs of floats 
           Uncertainties 
        n : int or list of int 
           How many significant digits to round to 
        
        Returns
        -------
        rx : float or collection of float 
            Rounded value 
        rd : float or collection of float
            Rounded uncertainties 
        """

        rx, rd, rp = cls.roundResult(x,dx,n,True)

        rp = _ensureList(rp)
        rx = _ensureList(rx)
        rd = _ensureList(rd)
        if len(rp) == 1:
            rp *= len(rx)+len(rd)

        print(rp);
        tt = [f'{v:.{max(-p,0)}f}' for v,p in zip(rx+rd,rp)]
        tx = tt[:len(rx)]
        td = tt[len(rx):]
        if len(tx) == 1:
            tx = tx[0]
        if len(td) == 1:
            td = td[0]

        return tx, td
#
# EOF
#
