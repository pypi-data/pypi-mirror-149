"""Database of (independent) variables 

Copyright 2019 Christian Holm Christensen 
"""
import yaml
from . with_phrase import WithPhrase
from . with_unit import WithUnit
from . unit import Unit
from . db import Db
from . pretty import Pretty
from .. utils import _ensureList

class Variable(WithPhrase,WithUnit,Db):
    """Class to hold constants for variables"""
    PHRASE_MAP = {}

    @classmethod
    def register(cls,name,value,pretty,units=None,phrases=None,asobs=False):
        p = cls.parse_phrases(phrases)
        u = cls.parse_unit(units)
        
        setattr(cls,name,value)
        Pretty.register_var(value,pretty)

        if p is not None:
            cls.PHRASE_MAP[value] = p

        if u is not None:
            Unit.add_var(value,u)

        if asobs:
            from . observable import Observable
            
            Observable.register(name,value,pretty,units,phrases,False)
            
        return cls

    @classmethod
    def phrases(cls,var):
        vl = _ensureList(var)
        pl = []
        for v in vl:
            if v in cls.PHRASE_MAP:
                pl += cls.PHRASE_MAP[v]
        return pl

    @classmethod
    def units(cls,var):
        return Unit.var(var)

    @classmethod
    def pretty(cls,var):
        return Pretty.var(var)

    @classmethod
    def pretty_units(cls,var):
        return Pretty.unit(cls.units(var))

    @classmethod
    def load(cls,fnstr):
        """Read variable definitions from a YAML file

        Parameters
        ----------
            fnstr : str or stream
                The file to read in 
        """
        db = super(Variable,cls)._load(fnstr,'Variables')
        if db is None:
            return
        for e in db:
            cls.register(**e)
#
# EOF
#
