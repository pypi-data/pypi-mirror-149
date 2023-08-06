"""Phrases 

Copytight 2019 Christian Holm Christensen
"""
import yaml
from . db import Db

class Phrase(Db):
    @classmethod
    def register(cls,name,value):
        """Register a phrase 

        Parameters
        ----------
        - name : str
          Constant to define 
        - value:
          Value of the constant 
        Returns
        -------
        - self : Phrase 
          Reference to the class 
        """
        setattr(cls,name,value)
        return cls

    @classmethod
    def load(cls,fnstr):
        """Read phrase definitions from a YAML file

        Parameters
        ----------
            fnstr : str or stream
                The file to read in 
        """
        db = super(Phrase,cls)._load(fnstr,'Phrases')
        if db is None:
            return
        for e in db:
            cls.register(**e)

#
# EOF
#
