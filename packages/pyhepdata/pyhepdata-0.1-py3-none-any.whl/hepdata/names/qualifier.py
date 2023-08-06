"""Database of qualifiers 

Copyright 2019 Christian Holm Christensen
"""
import yaml
from . with_phrase import WithPhrase
from . with_unit import WithUnit
from . unit import Unit
from . pretty import Pretty
from . variable import Variable
from . db import Db
from .. utils import _ensureList

class Qualifier(Db):    
    """Class to hold constants for qualifiers"""
    PHRASE_MAP = {}
    
    @classmethod
    def register(cls,name,value,pretty):
        """Register an qualifier 

        Parameters
        ----------
            name : str
                Constant to define  
            pretty : str
                Pretty print string 

        Returns
        -------
            cls : Qualifier 
                Reference to this class 
        """
        setattr(cls,name,value)
        Pretty.register_qual(value,pretty)

        return cls
    
    
    @classmethod
    def pretty(cls,qual):
        """Get pretty-print string of qualifier
        
        Parameters
        ----------
            qual : identifier 
                The qualifier 
        
        Returns
        -------
             pretty : str 
                  The pretty-print of the qualifier (may qual)
        """
        return Pretty.qual(qual)

    @classmethod
    def load(cls,fnstr):
        """Read qualifier definitions from a YAML file

        Parameters
        ----------
            fnstr : str or stream
                The file to read in 
        """
        db = super(Qualifier,cls)._load(fnstr,'Qualifiers')
        if db is None:
            return
        for e in db:
            cls.register(**e)

#
# EOF
#
