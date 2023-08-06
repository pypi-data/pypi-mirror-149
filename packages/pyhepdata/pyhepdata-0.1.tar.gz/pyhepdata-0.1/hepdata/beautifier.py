"""A simple beautifier class for pretty-printing names 

This class doesn't do any actual pretty-printing.  It is here to have
sane defaults for various arguments elsewhere

Copyright 2019 Christian Holm Christensen

"""

from hepdata.singleton import Singleton

class Beautifier(metaclass=Singleton):
    """Beautifier for plotting. 
    
    This implementation doesn't do much, except format strings
    """
    def qualifier(self,name,value=None,units=None):
        """Beautify a qualifier 
        
        Parameters
        ----------
            name : str 
                Name of the qualifier 
            value : str 
                Value of qualifier 
            units : str or None 
                Optional unit of value
        
        Returns
        -------
            ret : str
                Formatted qualifier 
        """
        if value is None:
            return '{}'.format(name)
        
        return '{}={}{}'.format(name,value,
                                units if units is not None else '')

    
    def variable(self,name,units=None):
        """Beautify a variable  
        
        Parameters
        ----------
            name : str 
                Name of the variable
            units : str or None 
                Optional unit of variable
        
        Returns
        -------
            ret : str
                Formatted variable 
        """
        ret = '{}'.format(name)
        if units is not None:
            ret += ' ({})'.format(units)
        return ret

    
    def observable(self,name,units=None):
        """Beautify an observable  
        
        Parameters
        ----------
            name : str 
                Name of the observable
            units : str or None 
                Optional unit of observable
        
        Returns
        -------
            ret : str
                Formatted observable 
        """
        ret = '{}'.format(name)
        if units is not None:
            ret += ' ({})'.format(units)
        return ret
    
    def unit(self,name):
        return '{}'.format(name)

    def qualifier_name(self,name):
        return '{}'.format(name)
        
    qual = qualifier
    var = variable
    obs = observable
    qname = qualifier_name
    
#
# EOF
#
