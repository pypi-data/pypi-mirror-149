"""Units database 

Copyright 2019 Christian Holm Christensen
"""
import yaml
from . pretty import Pretty
from . db import Db

class Unit(Db):
    """Class to hold constants for units types"""
    VAR_MAP = {}
    OBS_MAP = {}

    @classmethod
    def register(cls,name,value,pretty):
        """Register a unit
        
        Parameters
        ----------
            name : str
                Identifier to define 
            value : str 
                Value of identifier 
            pretty : str 
                Pretty print string 
        
        Returns
        -------
            cls : Unit
                Reference to this class 
        """
        setattr(cls,name,value)
        Pretty.register_unit(value,pretty)
        return cls
    
    @classmethod
    def _add(cls,x,units,m):
        """
        """
        m[x] = units

    @classmethod
    def add_var(cls,var,units):
        cls._add(var,units,cls.VAR_MAP)
        
    @classmethod
    def add_obs(cls,obs,units):
        cls._add(obs,units,cls.OBS_MAP)
        
    @classmethod
    def _lookup(cls,x,m,df=None):
        if x in m:
            return m[x]
        return df

    @classmethod
    def obs(cls,obs,df=None):
        return cls._lookup(obs,cls.OBS_MAP,df)
    
    @classmethod
    def var(cls,var,df=None):
        return cls._lookup(var,cls.VAR_MAP,df)

    @classmethod
    def pretty(cls,units):
        return Pretty.unit(units)
    
    @classmethod
    def load(cls,fnstr):
        """Read unit definitions from a YAML file


        Parameters
        ----------
            fnstr : str or stream
                The file to read in 
        """
        db = super(Unit,cls)._load(fnstr, 'Units')
        if db is None:
            return
        
        for e in db:
            cls.register(**e)

#
# EOF
#
