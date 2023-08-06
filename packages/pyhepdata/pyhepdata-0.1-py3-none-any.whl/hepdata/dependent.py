"""A container for dependent values in a data table 

Copyright 2019 Christian Holm Christensen
"""
import math
from hepdata.accepts import accepts
from hepdata.value import Value, ValueList
from hepdata.column import Column

class Dependent(Column):
    """A single column of dependent variables

    Dependent variables is what we typically put in the ordinate.  It
    is the quantity of our measurements.  Dependent variables take on
    a single value per independent variable value (or bin) and can be
    assigned multiple uncertainties (statistical, systematic). 

    We create an dependent variable column in a data table by
    calling the method :meth:`Table.dependent`

    >>> y = table.dependent('Observable', 'Units')

    The `Observable` and `Units` should preferably be strings recognised
    by `HEPData <https://hepdata.net>`_ (see also :mod:`hepdata.names`
    for an easier way to ensure proper variable names and units).  

    Data can be filled into the table one-by-one, such as 

    >>> for yval, ystat, ysys in zip(ys,stats,syss):
    ...     y.value(yval).symerror(ystat,'stat').symerror(ysys,'sys')

    or directly from arrays 

    >>> y.value(ys).symerror(stats,'stat').symerror(syss,'sys') 

    Uncertainties can be symmetric (see
    :meth:`hepdata.Value.symerror`) or a asymmetric (see
    :meth:`hepdata.Value.asymerror`).  The value retrieval (see
    :meth:`hepdata.Dependent.ye`) and plotting (see
    :mod:`hepdata.plot`) subsystems can correctly propagate
    uncertainties in all cases.
   
    Initialize column with variable name and optional unit

    Parameters
    ----------
    name : str 
        Name of dependent variable 
    unit : str (optional)
        Unit of qualifier 

    Test case
    ---------
    - `test_dependent.py`

    """
    #: Value field name
    VALUE = 'value'
    #: Qualifiers field name 
    QUALIFIERS = 'qualifiers'

    @accepts(var=str,unit=str)
    def __init__(self,var,unit=None):
        super(Dependent,self).__init__(var,unit)
        self._d[self.QUALIFIERS] = []

    @accepts(name=str,value=(float,str),unit=str)
    def qualifier(self,name,value,unit=None):
        """Add a qualifer to the column
        
        Parameters
        ----------
        name : str 
            Name of qualifier 
        value : any 
            Value of qualifier 
        unit : str (optional)
            Unit of qualifier 

        Returns
        -------
        self : Depedendent
            Reference to this object 

        """
        q = {self.NAME: name, self.VALUE: value}
        if unit is not None:
            q[self.UNITS] = unit
        
        self._d[self.QUALIFIERS].append(q)
        
        return self

    @accepts(value=(float,list,tuple,str))
    def value(self,value):
        """Add a value to the column
        
        Parameters
        ----------
        val : float, str, list
            Dependent variable value 

            If a list, then add all values in list and return a
            ValueList object to add uncertainties to 

        Returns
        -------
        r : Value, or Valuelist 
            The added value object or list of values 

        """
        if type(value) in [list,tuple]:
            l = ValueList([])
            for v in value:
                vv = Value(v)
                l._values.append(vv)
                self._append(vv)
            return l
        
        return self._append(Value(value))

    def qualifiers(self,select=None):
        """Get the qualifiers of the column as a list of dictionaries 
        
        Parameters
        ----------
        select : callable, list of str (optional)
            A callable or list of strings to select which
            qualifiers to return
        
        Returns
        -------
        qualifiers : list 
            List of qualifiers (each a dictionary)

        """
        if select is None:
            return self._d.get(self.QUALIFIERS,[])

        if type(select) is str:
            select = [select]
            
        if type(select) in [list,dict,set,tuple]:
            l1 = [q for q in self._d.get(self.QUALIFIERS,[])
                  if q[self.NAME] in select]
            ls = [s.lower() for s in select]
            if 'name' in ls:
                n = {self.NAME:self.name,
                     self.VALUE:None,
                     self.UNITS:self.units}
                try:
                    l1.insert(ls.index('name'),n)
                except:
                    l1.append(n)
            
            return l1

        assert callable(select), "Passed selector is not callable"

        return [q for q in self._d.get(self.QUALIFIERS,[]) if select(q)]

    @property 
    def y(self):
        """Extract an array of values

        Returns
        -------
        y : array-like, float 
             Array of dependent values (some possibly NaN)

        """
        return [e.y() for e in self._v]

    def e(self,calc=None,**kwargs):
        """Extract an array of uncertainties
        
        Parameters
        ----------
        calc : callable (optional)
            A callabable to calculate the final uncertainty on
            each data point.  This can for example sum
            uncertainties in quadtrature

            >>> sum_quad(errors,value):
            ...     def sqsym(e):
            ...         return e.get('symerror',0)**2
            ...     return math.sqrt(sum(map(sqsym,errors)))

            If one wants to filter the values, one can do
            something like

            >>> sum_quad_nonstat(errors,value):
            ...     def sqsym(e):
            ...         return e.get('symerror',0)**2
            ...     def nonstat(e):
            ...         return e.get('label','') != 'stat'
            ...     return math.sqrt(sum(map(sqsym,filter(nonstat,errors))))

             If no calc argument is given, we simply return a list
             of lists of uncertainties (symmetric and asymmetric).
        kwargs : dict 
            Additional keyword arguments to pass to calculation function
        
        Returns
        -------
        e : array-like, float or tuple
            array of uncertainties. If the uncertainty is an asymmetric 
            uncertainty, then we get an array of pairs, otherwise an 
            array of values.

        """
        return [v.e(calc,**kwargs) for v in self._v]

    @classmethod
    def _sysqual(cls,q):
        """Select a qualifier if it's name starts with "sys:" 
        
        Parameters
        -----------
        q : dict 
            Qualifier dictionary 
        
        Returns
        -------
        q or None: 
            Returns the qualifier dict if it matches, otherwise None 
        """
        n = q.get(Dependent.NAME, None)
        v = q.get(Dependent.VALUE,None)
        if n is None or v is None:
            return None

        if n.startswith('sys:'):
            return q;

        return None
        

    def ce(self,rel=1,calc=None,**kwargs):
        """Extract common uncertainties. 

        Common uncertainties are expected to be encoded as qualifiers
        that start with the string "sys:",

        Parameters
        ----------
        calc : callable (optional)
            A callabable to calculate the final uncertainty on
            each data point.  This can for example sum
            uncertainties in quadtrature

            >>> sum_quad(errors,value):
            ...     def sqsym(e):
            ...         return e.get('symerror',0)**2
            ...     return math.sqrt(sum(map(sqsym,errors)))

            If one wants to filter the values, one can do
            something like

            >>> sum_quad_nonstat(errors,value):
            ...     def sqsym(e):
            ...         return e.get('symerror',0)**2
            ...     def nonstat(e):
            ...         return e.get('label','') != 'stat'
            ...     return math.sqrt(sum(map(sqsym,filter(nonstat,errors))))

             If no calc argument is given, we simply return a list
             of lists of uncertainties (symmetric and asymmetric).

        """
        cml = self.qualifiers(Dependent._sysqual)
        if cml is None or len(cml) <= 0:
            return None

        vals    = [c[Dependent.VALUE] *
                   (rel / 100
                    if c.get(Dependent.UNITS,'') in ['PCT','%']
                    else 1) for c in cml]
        pais    = [{Value.SYMERROR: v} for v in vals]
        lbls    = [c[Dependent.NAME] for c in cml]
        calc    = Value.asis if calc is None else calc
        errs,dy = calc(pais,rel,**kwargs)

        return errs,dy,lbls
        
    def ye(self,calc=None,**kwargs):
        """Extract values and uncertainties 
        
        Parameters
        ----------
        calc : callable 
            See the :meth:`Dependent.e` and :meth:`Value.e` method
            descriptions
        **kwargs : Additional arguments 
            See the :meth:`hepdata.Dependent.e` and
            :meth:`hepdata.Value.e` method descriptions
        
        Returns
        -------
        y : list 
           A list of values 
        e : list 
           A list of uncertainties

        """
        if not kwargs.pop('columns',False):
            return [v.ye(calc,**kwargs) for v in self._v]

        defval = kwargs.get('default',math.nan)
        header = kwargs.get('header',False)
        y = []
        e = []
        h = []
        if header:
            h.append((self.name,self.units))
            
        for i,v in enumerate(self._v):
            yy, ee = v.ye(calc,**kwargs)
            y.append(yy)  # This is easy!

            for j,eee in enumerate(ee):
                col = None
                if len(e) <= j:
                    # No column, create it
                    if type(eee) is tuple:
                        col = [(defval,defval)] * i
                    else:
                        col = [defval] * i
                    e.insert(j,col)
                else:
                    col = e[j]
                    
                if header and len(h)-1 <= j:
                    # No header yet, assign it
                    err = v._d.get(Value.ERRORS,[])
                    if len(err) > j:
                        h.append(err[j].get(Value.LABEL,''))
                    else:
                        h.append('')
                    
                # Append value to column
                col.append(eee)

            # Fill-in in case this point has no uncertainties 
            if len(ee) <= 0 and len(e) > 0:
                n = len(e)  # Num columns
                for c in e:
                    if type(c[-1]) is tuple:
                        c.append((defval,defval))
                    else:
                        c.append(defval)

        if header:
            return [y,*e], h
        return [y,*e]

    def ne(self,select=None):
        """Count number of errors defined

        Parameters
        ----------
        select : callable (optional)
            Callable to select which uncertainties to count 

        Returns
        -------
        Number of uncertainties defined 

        """
        return max([v.ne(select) for v in self._v])

    def _qualifierSelect(self,select):
        """Return reference to this column if the qualifiers of this column
        meets the requirements of select.

        Select can be one of 

        - dict or list of dict 

          If select is a list (or single value) of dictionaries that
          the qualifiers must match (exactly) at least once.

          Each dict in the list should have the form 
        
              {NAME1: VALUE1,
               NAME2: VALUE2
               ...}

          where NAME<N> is the name of a qualifier and VALUE<N> is the
          value to match against. If VALUE<N> is the empty string,
          then it serves as a wildcard and any value of a qualifier is
          matched.

          So to criteria 
                
              [{'A': 'a', 'B': '', 'C': 'c'}] 
                 
          will match columns that have the qualifiers A, B, and C,
          where qualifer A must have the value 'a' and C must have the
          value 'c', but B can have any value (but must be defined).

          To select columns that does not have specific qualifier
          defined,m specify None for the value. The criteria

               [{'A': 'a', 'B': '', 'C': 'c'},
                {'A': None}] 
         
          Will match the same columns as before, as well as the
          columns that do not have the qualifier A defined.

        - a callable 

          If select is a callable and it returns true for this columns
          qualifiers, then the column is selected and we return a
          reference to it.  The callable must have the prototype 

              select(dict) -> bool 

          where dict is the collected dictionary of all qualifiers 

              {QUALIFIER1: VALUE1,
               QUALIFIER2: VALUE2,
               ...}

        Parameters
        ----------
        select : dict, list of dict, or callable 
            The criteria 
        
        Returns
        -------
        self : Column 
            Reference to this if selected, or None

        """
        if select is None:
            return self

        # If qualifiers are given, check that if we have a match
        # Flatten all qualifiers to a single dictonary 
        ql = {q[self.NAME]: q[self.VALUE] for q in self.qualifiers()}

        if callable(select) and select(ql):
            return True

        if type(select) not in [list,tuple]:
            return None
        
        for w in select:
            # Get dictonaries of key,values where
            # - value is not None and not the empty string (wildcard)
            nn = {k:v for k,v in w.items() if v is not None and v != ''}
            # - value the empty string (wildcard)
            an = {k:v for k,v in w.items() if v is not None and v == ''}
            # - value is none (exclusion)
            no = {k:v for k,v in w.items() if v is None}
            if (len(nn.items() & ql.items()) == len(nn) and
                len(an.keys()  & ql.keys())  == len(an) and
                len(no.keys()  & ql.keys())  == 0):
                # We match all criteria!
                return self

        return None

    def select(self,names=None,qualifiers=None):
        """Return self if this column meets the requirements. 

        The first requirement (if not None) is given by
        Column.headerSelect.

        The second requirement (if not None) is if the qualifiers of
        this column are selected by qualifierSelect.

        If the column does not meet the requirements, return None 
        
        Parameters
        ----------
        names : str, list, or callable (optional)
            The argumnt `names` can be either 

            - A single string.  If the string matches the name of this
              column, then the column is selected and we return a
              reference to it.
    
            - A list of strings.  If the name of the column is in this
              list, then the column is selected and we return a
              reference to it.
    
            - A callable. If the callable returns True for this
              column, then the column is selected and we return a
              reference to it.
    
              The callable must have the signature 
    
                  select(name,unit=None) -> bool 
    
              where the name and possible unit is passed as the first
              and second argument, respectively.  One can use this to
              match columns with for example a regular expression.
    
              >>> col.select(lambda n,u: re.search('sys.*',n) is not None)
    
            
        qualifiers : dict, list of dict, or callable (optional)
            A list (or single value) of dictionaries that the
            qualifiers must match (exactly) at least once, or a
            callable.

            - dict or list of dict 
    
              If qualifiers is a list (or single value) of
              dictionaries that the qualifiers must match (exactly) at
              least once.
    
              Each dict in the list should have the form 
            
                  {NAME1: VALUE1,
                   NAME2: VALUE2
                   ...}
    
              where NAME<N> is the name of a qualifier and VALUE<N> is
              the value to match against. If VALUE<N> is the empty
              string, then it serves as a wildcard and any value of a
              qualifier is matched.
    
              So to criteria 
                    
                  >>> [{'A': 'a', 'B': '', 'C': 'c'}] 
                     
              will match columns that have the qualifiers A, B, and C,
              where qualifer A must have the value 'a' and C must have
              the value 'c', but B can have any value (but must be
              defined).
    
              To select columns that does not have specific qualifier
              defined,m specify None for the value. The criteria
    
                   >>> [{'A': 'a', 'B': '', 'C': 'c'},
                   ...  {'A': None}] 
             
              Will match the same columns as before, as well as the
              columns that do not have the qualifier A defined.
    
            - a callable 
    
              If qualifiers is a callable and it returns true for this
              columns qualifiers, then the column is selected and we
              return a reference to it.  The callable must have the
              prototype
    
                  qualifiers(dict) -> bool 
    
              where dict is the collected dictionary of all qualifiers 
    
                  {QUALIFIER1: VALUE1,
                   QUALIFIER2: VALUE2,
                   ...}
    
        Returns
        -------
        self : Dependent 
            Reference to this column if requirements are met,
            otherwise None

        """
        # If names are given but this columns name is not in the list,
        # return None
        if self._headerSelect(names) is None:
            return None
        
        # If qualifiers are not given, return ourselves (success)
        if self._qualifierSelect(qualifiers) is None:
            return None

        return self

    @classmethod
    def fromDict(cls,d):
        """Construct a Dependent object from a dictionary

        Parameters
        ----------
        d : dict 
            Dictionary to construct from.  This could be read from a
            YAML/JSON file.
        
        Returns
        -------
        i : Dependent 
            Newly constructed Dependent object 
        """
        assert d.get(cls.VALUES,False),\
            "No {} in dictionary".format(cls.VALUES)
        assert d.get(cls.HEADER,False),\
            "No {} in dictionary".format(cls.HEADER)
        assert d[cls.HEADER].get(cls.NAME,False),\
            "No {}.{} in dictionary".format(cls.HEADER,cls.NAME)

        c = cls(d[cls.HEADER][cls.NAME],
                d[cls.HEADER].get(cls.UNITS,None))
        c._d = d
        
        for dv in d[cls.VALUES]:
            v = Value(dv[Value.VALUE])
            v._d = dv
            c._v.append(v)

        assert len(c._v) == len(d[cls.VALUES]),\
            "Mismatch in number of extracted values"

        return c
        
#
# EOF
# 
