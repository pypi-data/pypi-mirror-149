"""A 'beautifier' of names (variables, observables, units, qualifiers)

This is the default implementation which just echos our the passed
strings with very little manipulation

Copyright 2019 Christian Holm Christensen
"""
from .. dependent import Dependent

class Beautifier:
    """A 'beautifier' of names (variables, observables, units, qualifiers)

    This is the default implementation which just echos our the passed
    strings with very little manipulation
    """
    def __init__(self):
        pass

    def _delatex(self,t):
        m = {r'\pm': '+/-',
             r'\ge': '>=',
             r'\le': '<=',
             r'\lt': '<',
             r'\gt': '>',
             r'\rm': '',
             r'\,':  ' ',
             r'\!':  '',
             '\\':   '',
             '$': ''
        }
        for k,v in m.items():
            t = t.replace(k,v)

        return t
             
    def variable(self,n,u=None,v=None):
        """Format a variable (abscissa labels)
        
        Parameters
        ----------
        n : str 
            Name 
        u : str 
            Units 
        v : str, float
            Value
        
        Returns
        -------
        r : str 
            Formatted string 
        """
        r = "{}".format(n)
        if u is not None and str(u) != '':
            r = r + " ({})".format(u)
        return self._delatex(r)
    
    def observable(self,n,u=None,v=None):
        """Format an observable (ordinate labels)
        
        Parameters
        ----------
        n : str 
            Name 
        u : str 
            Units 
        v : str, float
            Value
        
        Returns
        -------
        r : str 
            Formatted string 
        """
        r = "{}".format(n)
        if u is not None and str(u) != '':
            r = r + " ({})".format(u)
        return self._delatex(r)

    def qualifier(self,n,v=None,u=None):
        """Format a qualifier
        
        Parameters
        ----------
        n : str 
            Name 
        v : str or float
            Value 
        u : str 
            Units 
        
        Returns
        -------
        r : str 
            Formatted string 
        """
        r = n
        if v is not None:
            r += '={}'.format(v)
            if u is not None and str(u) != '':
                r += ' ({})'.format(u)
        return self._delatex(r)
    
    def qualifiers(self,qls=None):
        """Format a list of qualifier
        
        Parameters
        ----------
        ql : list 
            List of qualifier dictionaries 

            - name : str 
            - value : str or float
            - unit : str
        
        Returns
        -------
        r : str
            Formatted string 
        """
        if qls is None:
            return None
        l = []
        for q in qls:
            n = q.get(Dependent.NAME,'')
            if n.startswith('sys:'):
                n = n[4:]
            l.append(self.qualifier(n,
                                    q.get(Dependent.VALUE,None),
                                    q.get(Dependent.UNITS,None)))
        return ', '.join(l)

    def common(self,n):
        return self._delatex(n)

    def uncertainty(self,l,main):
        return self._delatex(l)

    def unit(self,l):
        return self._delatex(l)

    def qualifier_name(self,name):
        return self._delatex(name)

    qual = qualifier
    var = variable
    obs = observable
    qname = qualifier_name
    
#
# EOF
#
