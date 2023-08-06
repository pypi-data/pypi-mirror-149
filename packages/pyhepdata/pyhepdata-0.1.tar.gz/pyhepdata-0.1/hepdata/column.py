"""Base class for dependent and independent columns in a table 

Copyright 2019 Christian Holm Christensen
"""
from hepdata.accepts import accepts


class Column:
    """A single column of dependent variables

    Parameters
    ----------
    name : str 
        Name of dependent variable 
    unit : str (optional)
        Unit of qualifier 

    Test case
    ---------
    - `test_column.py`

    """
    #: Header field name 
    HEADER = 'header'
    #: Name field name 
    NAME = 'name'
    #: Units field name 
    UNITS = 'units'
    #: Values field name 
    VALUES = 'values'

    @accepts(var=str,unit=str)
    def __init__(self,var,unit=None):
        self._v = []  # List of value objects 
        self._d = {
            self.HEADER: {self.NAME: var},
            self.VALUES: [] }
        self._r = False  # Not rounded yet
        if unit is not None:
            self._d[self.HEADER][self.UNITS] = unit
            
    
    def _append(self,v):
        """Appends a value to internal list and the dictionary 
        of the value to the internal dictionary 

        Parameters 
        ----------
        v : object 
            Object to append to the list and dictionary 

        Returns
        -------
        v : object 
            The appended value 
        """
        self._d[self.VALUES].append(v._d)
        self._v.append(v)
        return v

    def __len__(self):
        """Get the number of variables in this column
        
        This simply counts the nubmer of values, irrespetive of their
        value (e.g., NaN's are also counted).
        """
        return len(self._d[self.VALUES])

    @property
    def header(self):
        """Get the header as a dictionary

        Returns
        -------
        header : dict 
            The header information or empty dictonary 
        """
        return self._d[self.HEADER]
    
    @property
    def name(self):
        """Get the name of the column 
        
        Returns
        -------
        name : str 
            Name of the column or empty string 
        """
        return self.header[self.NAME]

    @property
    def units(self):
        """Get the units of the column 
        
        Returns
        -------
        units : str 
            Units of the column or empty string 
        """
        return self.header.get(self.UNITS,None)

    @property
    def values(self):
        """Get the values of the column as a list of dictionaries 

        This returns a list of dictionaries where the each element
        contains a value and a possible list of uncertainties (called
        errors [sic]). 

        Returns
        -------
        values : list 
            List of values (each a dictionary) 
        """
        return self._d[self.VALUES]

    @accepts(n=int)
    def round(self,n):
        """Round all values (and uncertainties) to n decimal digits

        Parameters
        ----------
        n : int 
            Number of decimal places to round to.  T his can be
            negative, which means we round of -n digits before the
            decimal point
        
        Returns
        -------
        self : Column
            Reference to this object 
        """
        from warnings import warn 
        if self._r:
            warn(f'Column {self.name} already rounded')
            return
        
        for v in self._v:
            v.round(n)

        self._r = True
        
        return self
    
    @accepts(n=int)
    def roundNsig(self,n):
        """Round all values (and uncertainties) to n significant digits
        
        This is done by selecting at the smallest uncertainty and then
        rounding that off to the number of significant digits.  The
        remainding uncertainties and the value is then rounded to the
        same precision as the least uncertainty.

        Parameters
        ----------
        n : int 
            Number of significant digits to round to 
        
        Returns
        -------
        self : Column
            Reference to this object 
        """
        from warnings import warn 
        if self._r:
            warn(f'Column {self.name} already rounded')
            return
        
        for v in self._v:
            v.roundNsig(n)

        self._r = True
        
        return self
        
        
    def _headerSelect(self,select):
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
        select : str, list of str, or callable 
            Selection criteria 

        Returns
        -------
        self : Column 
            Reference to this if selected, or None
        """
        if select is None:
            return self

        if type(select) is str and self.name == select:
            return self

        if type(select) in [list,tuple] and self.name in select:
            return self
        
        if callable(select) and select(self.name,self.unit):
            return self

        return None
#
# EOF
#
