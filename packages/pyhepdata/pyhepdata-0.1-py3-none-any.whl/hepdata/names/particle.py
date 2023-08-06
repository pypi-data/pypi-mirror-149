"""Particle database 

Copyright 2019 Christian Holm Christensen 
"""
import yaml
from . pretty import Pretty
from . db import Db

class Particle(Db):
    """Class to hold constants for Particle types"""
    @classmethod
    def register(cls,name,value,pretty):
        """Register a particle type 
        
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
            cls : Particle 
                Reference to this class
        """
        setattr(cls,name,value)
        Pretty.register_part(value,pretty)
        return cls

    @classmethod
    def pretty(cls,p):
        """Get pretty print string of a particle

        Parameters
        ----------
            p : identifier 
                 Particle identifier 
        
        Returns 
        -------
            prt : str 
                Pretty print version of particle
        """
        return Pretty.part(p)
    
    @classmethod
    def load(cls,fnstr):
        """Read particle definitions from a YAML file

        Parameters
        ----------
            fnstr : str or stream
                The file to read in 
        """
        db = super(Particle,cls)._load(fnstr,'Particles')
        if db is None:
            return
        for e in db:
            cls.register(**e)

#
# EOF
#
