"""A container for dependent values in a data table 

Copyright 2019 Christian Holm Christensen
"""
import math
from . accepts import accepts
from . bin import Bin
from . column import Column
from . utils import _ensureList

class Independent(Column):
    """A single column of independent variables

    Independent variables is what we typically put in the abscissa.
    It is the quantity by which we categorise our measurements.
    Independent variables can take on a single value (without
    uncertainties), or be `binned`.  

    We create an independent variable column in a data table by
    calling the method :meth:`Table.independent`

    >>> x = table.independent('Variable', 'Units')

    The `Variable` and `Units` should preferably be strings recognised
    by `HEPData <https://hepdata.net>`_ (see also :mod:`hepdata.names`
    for an easier way to ensure proper variable names and units).  

    Data can be filled into the table one-by-one, such as 

    >>> for xlow, xhigh in zip(bins[:-1],bins[1:]):
    ...     x.value(low=xlow,high=xhigh) 

    for binned data, or 

    >>> for xi in xs:
    ...     x.value(value=xi) 

    for unbinned data, or in a single go from arrays like 

    >>> x.value(bins[:-1],bins[1:)
    
    or 

    >>> x.value(value=xs)

    Initialize column with variable name and optional units

    Parameters
    ----------
    name : str 
        Name of independent variable 
    unit : str (optional)
        Unit of variable  

    Test case
    ---------
    - `test_indepedendent.py`

    """
    
    @accepts(var=str,unit=str)
    def __init__(self,var,unit=None):
        super(Independent,self).__init__(var,unit)
            
    @accepts(low=(list,tuple,float),
             high=(list,tuple,float),
             value=(list,tuple,float,str))
    def value(self,low=None,high=None,value=None):
        """Add an independent value.

        Either both of low and high should be given, or value should be given. 
        
        Parameters
        ----------
        low : float (optional)
            Lower bound 
        high  : float (optional)
            Upper bound 
        value : float or str (optional)
            'Centre' value

        Returns
        -------
        self : Independent
            Reference to this object
        """
        if low is None and high is None and value is None:
            raise ValueError('Neither low,high or value given')
        if low is not None and high is None:
            raise ValueError('Low bound given, but no high bound')
        if high is not None and low is None:
            raise ValueError('Low bound given, but no high bound')
        if type(low)   in [list,tuple] or \
           type(high)  in [list,tuple] or \
           type(value) in [list,tuple]:
            ll = _ensureList(low)
            lh = _ensureList(high)
            lv = _ensureList(value)

            if ll is not None and len(ll) != len(lh):
                raise ValueError('Size of lower and upper bounds do not match')
            if ll is not None and lv is not None and len(lv) != len(lh):
                raise ValueError('Size of values and bounds do not match')
            n = len(lv) if lv is not None else len(ll)

            if ll is None:
                ll = [None]*n
            if lh is None:
                lh = [None]*n
            if lv is None:
                lv = [None]*n

            for il, ih, iv in zip(ll,lh,lv):
                b = Bin(il,ih,iv)
                self._append(b)

            return self
            
        b = Bin(low,high,value)
        self._append(b)
        return self

    @property
    def x(self):
        """Extract an array of values

        Returns
        -------
        y : array-like, float 
             Array of dependent values (some possibly NaN)
        """
        return [b.x() for b in self._v]

    def e(self,**kwargs):
        """Extract an array of uncertainties
        
        Parameters
        ----------
        **kwargs : keyword argumens
            - alwaystuple : bool 
                If true, uncertainties are always returned as 2-tuples 

        Returns
        -------
        e : array-like, float or tuple
            array of uncertainties. If the uncertainty is an asymmetric 
            uncertainty, then we get an array of pairs, otherwise an 
            array of values.
        """
        return [b.e(**kwargs) for b in self._v]

    def xe(self,**kwargs):
        """Get midpoints and uncertainties 

        Parameters
        ----------
        **kwargs : keyword argumens 
            Various keyword arguments.  See the
            :meth:`hepdata.Dependent.e` and :meth:`hepdata.Value.e`
            method descriptions
        
        Returns
        -------
        x : list 
           A list of values 
        e : list 
           A list of uncertainties
        """
        if not kwargs.pop('columns',False):
            return [b.xe(**kwargs) for b in self._v]

        defval = kwargs.get('default',math.nan)
        header = kwargs.get('header',False)
        x = []
        e = []
        for i,v in enumerate(self._v):
            xx, ee = v.xe(**kwargs)
            x.append(xx)  # This is easy!
            e.append(ee)

        if kwargs.get('header',False):
            return [x,e], (self.name,self.units)
        return [x,e]
        
           
    def select(self,names):

        """Return this column if the select requirement is met, or return
        None. 
        
        Select can be either 

        - A single string.  If the string matches the name of this
          column, then the column is selected and we return a
          reference to it.

        - A list of strings.  If the name of the column is in this
          list, then the column is selected and we return a reference
          to it.

        - A callable. If the callable returns True for this column,
          then the column is selected and we return a reference to it.

          The callable must have the signature 

              select(name,unit=None) -> bool 

          where the name and possible unit is passed as the first and
          second argument, respectively.  One can use this to match
          columns with for example a regular expression.

          >>> col.select(lambda n,u: re.search('sys.*',n) is not None)
        
        Parameters
        ----------
        names : str, list of str, or callable 
            Selection criteria on column name 

        Returns
        -------
        self : Column 
            Reference to this if selected, or None
        """
        return self._headerSelect(names)

    @classmethod
    def fromDict(cls,d):
        """Construct a Independent object from a dictionary

        Parameters
        ----------
        d : dict 
            Dictionary to construct from.  This could be read from a
            YAML/JSON file.
        
        Returns
        -------
        i : Independent 
            Newly constructed Independent object 
        """
        if d is None or len(d) == 0:
            return cls('','')

        assert d.get(cls.VALUES,False),\
            "No {} in dictionary".format(cls.VALUES)
        assert d.get(cls.HEADER,False),\
            "No {} in dictionary".format(cls.HEADER)
        assert d[cls.HEADER].get(cls.NAME,False),\
            "No {}.{} in dictionary".format(cls.HEADER,cls.NAME)

        i = cls(d[cls.HEADER][cls.NAME],
                d[cls.HEADER].get(cls.UNITS,None))
        i._d = d
        
        for db in d[cls.VALUES]:
            b = Bin(0,0)
            b._d = db
            i._v.append(b)
                    
        assert len(i._v) == len(d[cls.VALUES]),\
            "Mismatch in number of extracted values"

        return i
        
        
#
# EOF
# 
