"""Collision system database 

Copyright 2019 Christian Holm Christensen
"""
import yaml
from . pretty import Pretty
from . particle import Particle
from . db import Db

class System(Db):
    """Class to hold constants for Collision types"""

    #: Map of AA-like collision systems 
    AA_MAP = []
    
    @classmethod
    def register(cls,name,value=None,pretty=None,
                 projectile=None,target=None,aa=False):
        """Register a collision type 
        
        If second is given, assume that value is projectile and second
        is target.  If second is not given, assume that value has both 
        target and projectile type.   

        If pretty is not given, try to encode it from the target and
        projectile particle types. In that case, if second is not
        given assume that the projectile and target is separated by
        spaces in value. If the deduction failes, raise an exception. 

        Parameters
        ----------
            name : str
                Identifier to define 
            value : str 
                Value of identifier 
            second : str (optional)
                Second value of identifier 
            pretty : str (optional)
                Pretty print string 
        
        Returns
        -------
            cls : System 
                Reference to this class 
        """
        if value is None and (projectile is None or target is None):
            raise ValueError('Value or projectile,target-pair not given')
        
        if projectile is None:
            projectile,target = value.split()

        if projectile.startswith('Particle.'):
            projectile = projectile.replace('Particle.','')
            projectile = getattr(Particle,projectile)
            
        if target.startswith('Particle.'):
            target = target.replace('Particle.','')
            target = getattr(Particle,target)
            
        if pretty is None:
            pp = Pretty.part(projectile,False)
            tt = Pretty.part(target,False)
            if pp is None or tt is None:
                raise ValueError('Cannot deduce pretty string for collision '
                                 'partners {} and {}'.format(projectile,target))

            sep = '-' if aa else ''
            pretty = sep.join([pp,tt])

        
            
        val = ' '.join([projectile,target])
        setattr(cls,name,val)
        if aa:
            cls.AA_MAP.append(val)

        # print(f'Register collision system {val}: {aa}')
        Pretty.register_col(val,pretty)
        return cls

    @classmethod
    def pretty(cls,s):
        """Get pretty print string of a system

        Parameters
        ----------
            s : identifier 
                 System identifier 
        
        Returns 
        -------
            prt : str 
                Pretty print version of system
        """
        return Pretty.sys(s)
    
    @classmethod
    def isAA(cls,value):
        # print(f'Check for {value} in {cls.AA_MAP}')
        return value in cls.AA_MAP

    @classmethod
    def load(cls,fnstr):
        """Read system definitions from a YAML file


        Parameters
        ----------
            fnstr : str or stream
                The file to read in 
        """
        db = super(System,cls)._load(fnstr,'Systems')
        if db is None:
            return
        for e in db:
            cls.register(**e)
#
# EOF
#
