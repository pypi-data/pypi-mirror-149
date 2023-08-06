"""A resource object attached to other stuff 

Copyright 2019 Christian Holm Christensen
"""
from . licensed import Licensed
from . accepts import accepts
import mimetypes

class Resource(Licensed):
    """A resource

    "Create a resource
    
    Parameters
    ----------
    location : str 
        Location - for example a URL or local file 
    description : str 
        A short description of the resource 
    tpe : str (optional)
        Resource type 

    Test case
    ---------
    - `test_resource.py` 

    """
    #: Location field name
    LOCATION = 'location'
    #: Description field name 
    DESCRIPTION = 'description'
    #: Type field name 
    TYPE = 'type'
    
    def __init__(self,location,description,tpe=None):
        super(Resource,self).__init__()        
        self._d = {self.LOCATION: location,
                   self.DESCRIPTION: description}
        if tpe is None:
            tpe = mimetypes.guess_type(location)[0]
        if tpe is not None:
            self._d[self.TYPE] = tpe

    def location(self):
        return self._d.get(self.LOCATION,None)
    
    def description(self):
        return self._d.get(self.DESCRIPTION,None)

    def type(self):
        return self._d.get(self.TYPE,None)

    @accepts(name=str,url=str,description=str)
    def license(self,name=None,url=None,description=None):
        """Set license of the resource

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
        self : Resource 
            Reference to this object 
        """
        self._d[self._license_key] = self._license(name,url,description)
        return self
#
# EOF
#
