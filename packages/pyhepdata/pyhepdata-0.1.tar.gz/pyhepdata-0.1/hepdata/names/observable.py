"""Database of observables 

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

class Observable(WithPhrase,WithUnit,Db):    
    """Class to hold constants for observables"""
    PHRASE_MAP = {}
    
    @classmethod
    def register(cls,name,value,pretty,units=None,phrases=None,asvar=False):
        """Register an observable 

        Parameters
        ----------
            name : str
                Constant to define  
            value : str 
                Value of constant 
            pretty : str
                Pretty print string 
            units : Unit constant (optional)
                Unit of observables 
            phrases : str or list of Phrases constant
                List of phrases associated with observable 

        Returns
        -------
            cls : Observable 
                Reference to this class 
        """
        p = cls.parse_phrases(phrases)
        u = cls.parse_unit(units)
        
        setattr(cls,name,value)
        Pretty.register_obs(value,pretty)

        if p is not None:
            cls.PHRASE_MAP[value] = p

        if u is not None:
            Unit.add_obs(value,u)

        if asvar:
            Variable.register(name,value,pretty,units,phrases,False)
            
        return cls
    
    @classmethod
    def ratio(cls,p1,p2):
        """Encode a ratio observable 

        Parameters
        ----------
            p1 : Particle constant 
                 First particle constant 
            p2 : Particle constant 
                 Second particle constant 
        
        Returns
        -------
             ratio : str
                 Encoded ratio
        """
        return '{}/{}'.format(p1,p2)
    
    @classmethod
    def phrases(cls,obs):
        """Get phrases associated with observable(s)
        
        Parameters
        ----------
            obs : (list of) Observable constant 
                One or more constants 
        
        Returns
        -------
            pl : list 
                 List of phrases 
        """
        ol = _ensureList(obs)
        pl = []
        for o in ol:
            if o in cls.PHRASE_MAP:
                pl += cls.PHRASE_MAP[o]
        return pl

    @classmethod
    def units(cls,obs):
        """Get unit of obserbable
        
        Parameters
        ----------
            obs : identifier 
                The observable 
        
        Returns
        -------
             unit : str 
                  The unit of the observable (may None)
        """
        return Unit.obs(obs)

    @classmethod
    def pretty(cls,obs):
        """Get pretty-print string of observable
        
        Parameters
        ----------
            obs : identifier 
                The observable 
        
        Returns
        -------
             pretty : str 
                  The pretty-print of the observable (may obs)
        """
        return Pretty.obs(obs)

    @classmethod
    def pretty_units(cls,obs):
        """Get pretty-print string of the unit of the observable
        
        Parameters
        ----------
            obs : identifier 
                The observable 
        
        Returns
        -------
             pretty : str 
                  The pretty-print of the observable units (may None)
        """        
        return Pretty.unit(cls.units(obs))
    
    @classmethod
    def load(cls,fnstr):
        """Read observable definitions from a YAML file

        Parameters
        ----------
            fnstr : str or stream
                The file to read in 
        """
        db = super(Observable,cls)._load(fnstr,'Observables')
        if db is None:
            return
        for e in db:
            cls.register(**e)

#
# EOF
#
