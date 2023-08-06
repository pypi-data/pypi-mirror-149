"""Database base class 

Copyright 2019 Christian Holm Christensen
"""
import yaml

class Db:
    """Base class for databases """
    @classmethod
    def _load(cls,fnstr,section):
        """Load section from file (either by name or stream)

        Parameters
        ----------
            fnstr : str or stream
                The file to read in 
            section : str 
                The section to read in
        
        Returns
        -------
            sec : dict or None
                The read section or None 
        """
        if isinstance(fnstr,str):
            with open(fnstr,'r') as inp:
                db = yaml.load(inp,Loader=yaml.SafeLoader)
        else:
            fnstr.seek(0)
            db = yaml.load(fnstr,Loader=yaml.SafeLoader)

        
        if db is None or section not in db:
            return None

        return db[section]

#
# EOF
#

        
