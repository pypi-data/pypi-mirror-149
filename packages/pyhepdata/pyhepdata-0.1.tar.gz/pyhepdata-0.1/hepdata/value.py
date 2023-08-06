"""A single dependent value with uncertainties

Copyright 2019 Christian Holm Christensen
"""
import math
from . rounder import Rounder
from . accepts import accepts
from . utils import _ensureList
from . propagator import Propagator

class Value:
    """A single dependent value
    Initialize value with v.

    Parameters
    ----------
        v : float 
            Value of dependent variable 
    """
    #: Value field name
    VALUE = 'value'
    #: Errors field name
    ERRORS = 'errors'
    #: Symerror field name
    SYMERROR = 'symerror'
    #: Asymerror field name
    ASYMERROR = 'asymerror'
    #: Plus field name
    PLUS = 'plus'
    #: Minus field name
    MINUS = 'minus'
    #: Label field name
    LABEL = 'label'
    
    @accepts(v=(float,str))
    def __init__(self,v):
        self._d = {self.VALUE: v, 
                   self.ERRORS: [] }

    def y(self): 
        """Return value"""
        from math import nan
        try:
            return float(self._d[self.VALUE])
        except:
            pass

        return nan

    value = y

    def e(self,calc=None,**kwargs):
        """Return the uncertainties or calculated uncertainty(ies) if calc is
        given.

        Parameters
        ----------
        calc : callable (optional)
        
            A callabable to calculate the final uncertainty on
            each data point.  
            
            The calc callable must have the prototype  

                calc(errors,value,**kwargs) -> ret,dx 

            where 
        
            - ret is the returned uncertainty either as a scalar 
              value, as a tuple of lower and upper bounds, or a 
              list of such values (scalar or 2-tuple)
            
            - dx is the possible offset on the value from the 
              uncertainties 

            This can for example sum uncertainties in quadrature
            
            >>> sum_quad(errors,value):
            >>>     def sqsym(e):
            >>>         return e.get('symerror',0)**2
            >>>     return math.sqrt(sum(map(sqsym,errors))),0
            
            If one wants to filter the values, one can do
            something like

            >>> sum_quad_nonstat(errors,value):
            >>>     def sqsym(e):
            >>>         return e.get('symerror',0)**2
            >>>     def nonstat(e):
            >>>         return e.get('label','') != 'stat'
            >>>     return math.sqrt(sum(map(sqsym,filter(nonstat,errors))))

             If no calc argument is given, we simply return a list
             of lists of uncertainties (symmetric and asymmetric).
 
        **kwargs : Keyword arguments to pass on to calculator
            - alwaystuple : bool
                 If true, always return a 2-tuple for each uncertainty
            - delta : bool 
                 If true, also return off-set on value
        
        Returns
        -------
        e : array-like, float or tuple
            array of uncertainties. If the uncertainty is an asymmetric 
            uncertainty, then we get an array of pairs, otherwise an 
            array of values.
        """
        if calc is None:
            calc = Propagator.asis

        delta       = kwargs.pop('delta',False)
        alwaystuple = kwargs.get('alwaystuple',False)
        
        r,d = calc(self._d.get(self.ERRORS,[{}]),
                   self._d.get(self.VALUE,0),
                   **kwargs)

        if alwaystuple:
            if type(r) is list:
                r = [(-rr,rr) if type(rr) is not tuple else rr for rr in r]
            elif type(r) is not tuple:
                r = (-r,r)
        if delta:
            return r,d
        return r

    def ye(self,calc=None,**kwargs):
        """Get value and uncertainty (uncertainties)
        
        Parameters
        ----------
        calc : callable 
            See the Value.e method description 
        **kwargs : other arguments 
            See also the :meth:`Value.e` method description 

        Returns
        -------
        y : float 
            The value 
        e : float, (float,float) or list of float or (float,float)
            The uncertainties
        """
        kwargs['delta'] = True
        bounds = kwargs.get('bounds',False)
        center = kwargs.pop('center',False)
        if bounds or center:
            kwargs['alwaystuple'] = True
            
        e,d = self.e(calc,**kwargs)
        y   = self.y() + d

        if bounds:
            if type(e) is list:
                return y, [(y+ee[0],y+ee[1]) for ee in e]
            return y, (y+e[0],y+e[1])

        if center:
            l = y + e[0]
            h = y + e[1]
            y = (h + l) / 2
            e = h - y
        
        return y, e
        
    @accepts(sym=(float,str),label=str)
    def symerror(self,sym,label=None):
        """Define a symmetric error

        Parameters
        ----------
        sym : float 
            The uncertainty
        label : str (optiona)
            Uncertainty name 

        Returns
        -------
        self : Value 
            Reference to this object 
        """
        e = {self.SYMERROR: sym}
        if label is not None:
            e[self.LABEL] = label
        self._d[self.ERRORS].append(e)
        return self

    @accepts(down=(float,str),up=(float,str),label=str)
    def asymerror(self,down,up,label=None):
        """Define an asymmetric error
        
        If down and up are equal, we define a symmetric error instead.

        Parameters
        ----------
        up : float 
            The 'plus' (or upward) uncertainty (normally positive)
        down : float 
            The 'minus' (or downward) uncertainty (normally negative)
        label : str (optiona)
            Uncertainty name 

        Returns
        -------
        self : Value 
            Reference to this object
        """
        if math.fabs(up - down) < 1e-9:
            return self.symerror(up,label)
        
        e = {self.ASYMERROR: {self.PLUS:up,self.MINUS:down}}
        
        if label is not None:
            e[self.LABEL] = label
            
        self._d[self.ERRORS].append(e)

        return self

    @accepts(n=int)
    def round(self,n):
        """Round value and uncertainties to `n` digits

        Parameters
        ----------
        n : int, positive 
            Number of digits
        
        Returns
        -------
         self : Value 
             Reference to self 
        """
        self._d[self.VALUE] = round(self._d[self.VALUE],n)
        for e in self._d.get(self.ERRORS,[]):
            if self.ASYMERROR in e:
                e[self.ASYMERROR][self.PLUS]  = \
                    round(e[self.ASYMERROR][self.PLUS], n)
                e[self.ASYMERROR][self.MINUS] = \
                    round(e[self.ASYMERROR][self.MINUS],n)
            else:
                e[self.SYMERROR] = round(e[self.SYMERROR])

        return self

    @accepts(n=int)
    def roundNsig(self,n):
        """Round smallest uncertainty to n significant digits and 
        give the rest of the values to the same precision

        Parameters
        ----------
        n : int, positive 
            Number of siginificant digits 
        
        Returns
        -------
        self : Value 
            Reference to self 
        """
        from math import isnan, nan
        try:
            x = float(self._d[self.VALUE])
        except:
            x = nan
        if isnan(x):
            return

        
        d = []
        m = []
        for e in self._d.get(self.ERRORS,[]):
            if self.ASYMERROR in e:
                d.append(e[self.ASYMERROR][self.PLUS])
                d.append(e[self.ASYMERROR][self.MINUS])
            else:
                d.append(e[self.SYMERROR])

        rx, rd = Rounder.roundResult(x,d,n)
        rd     = _ensureList(rd)
        # tx, td = Rounder.textResult(x,d,n)
        # td     = _ensureList(td)
        self._d[self.VALUE] = rx
        i = 0
        for e in self._d.get(self.ERRORS,[]):
            if self.ASYMERROR in e:
                e[self.ASYMERROR][self.PLUS]  = rd[i]
                e[self.ASYMERROR][self.MINUS] = rd[i+1]
                i += 1
            else:
                e[self.SYMERROR] = rd[i]
            i += 1

        return self

    def sync(self):
        """Synchronise value and text representations"""
        pass
    
    # Some aliases for propagator functions
    asis      = Propagator.asis
    sumsq     = Propagator.sumsq
    linvar    = Propagator.linvar
    linstd    = Propagator.linstd
    withlabel = Propagator.withlabel
    stack     = Propagator.stack

class ValueList:
    def __init__(self,vs):
        self._values = vs

    @accepts(sym=(float,list),label=str,missing=(float,str))
    def symerror(self,sym,label=None,missing=math.nan):
        """Set symmetric uncertainty on values. 

        Parameters
        ----------
        sym : list 
            Symmetric uncertainties. If length of sym is smaller than
            the number of values, fill in with the value missing
        label : str 
            Label on symmetric uncertainties 
        missing : float, str 
            Value to set on missing entries 
        
        Returns
        -------
        self : ValueList 
            Reference to self 
        """
        s = _ensureList(sym)
        if len(s) < len(self._values):
            s += [missing] * (len(self._values)-len(s))
        for sy,v in zip(s,self._values):
            v.symerror(sy,label=label)

        return self

    @accepts(down=(float,list),up=(float,list),label=str,missing=(float,str))
    def asymerror(self,down,up,label=None,missing=math.nan):
        """Set asymmetric uncertainty on values. 

        Parameters
        ----------
        down : list 
            Down uncertainties. If length of sym is smaller than
            the number of values, fill in with the value missing
        up : list 
            Up uncertainties. If length of sym is smaller than
            the number of values, fill in with the value missing
        label : str 
            Label on symmetric uncertainties 
        missing : float, str 
            Value to set on missing entries 
        
        Returns
        -------
        self : ValueList 
            Reference to self 
        """
        sd = _ensureList(down)
        if len(sd) < len(self._values):
            sd += [missing] * (len(self._values)-len(sd))
        su = _ensureList(up)
        if len(su) < len(self._values):
            su += [missing] * (len(self._values)-len(su))
        for asd, asu, v in zip(sd,su,self._values):
            v.asymerror(asd,asu,label=label)
        
        return self
#
# EOF
#
