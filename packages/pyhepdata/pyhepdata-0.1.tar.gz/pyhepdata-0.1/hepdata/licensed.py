"""Base class for licensed objects 

Copyright 2019 Christian Holm Christensen
"""
class Licensed:
    #: Name field name 
    NAME = 'name'
    #: URL field name 
    URL = 'url'
    #: Description field name 
    DESCRIPTION = 'description'
    #: License field name 
    LICENSE = 'license'
    
    """Base class for things with a license

    Test case
    ---------
        test_licensed
    """
    def __init__(self,key='license'):
        """Set-up 

        Parameters
        ----------
        key : str 
            Key to use for license 
        """
        self._license_key = key

    def _license(self,name=None,url=None,description=None):
        """Format license

        Parameters 
        ----------
        name : str (optional)
            Name of the license (e.g. CC-BY-4.0)
        url : str  (optional)
            URL to find license text 
        description : str  (optional)
            Short description of license 

        Returns
        -------
        d : dict 
            Dictionary of license 
        """ 
        d = dict()
        if name is not None:
            d[self.NAME] = name
        if url is not None:
            d[self.URL] = url
        if description is not None:
            d[self.DESCRIPTION] = description
        return d

#
# EOF
#
