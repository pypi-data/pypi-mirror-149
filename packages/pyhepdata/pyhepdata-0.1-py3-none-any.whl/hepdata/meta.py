"""Table meta information 

Copyright 2019 Christian Holm Christensen
"""
from hepdata.accepts import accepts
from hepdata.table import Table
from hepdata.licensed import Licensed
from hepdata.resource import Resource
from hepdata.utils import _ensureList

class Meta(Licensed):
    r"""Meta information on a table

    Initialize with name, description, and (possibly) the filename

    The meta information of a data table contains 

    - Qualifiers, such as :math:`p_{\mathrm{T}}` cut offs, particle
      ids, rapidity ranges, centrality classes and so on.
    - References to auxiliary files 
    - Keywords to classify the data 
        - ``reactions`` - like the specification of process e.g.,
            :math:`\mathrm{K}^{0}_{S}\rightarrow \mathrm{\pi}^{+}+\mathrm{\pi}^{-}`
        - ``observables`` - such as :math:`E\mathrm{d}^3\sigma/dp^3`
        - ``cmenergies`` - the centre-of-mass energy (or energies) in GeV 
        - ``phrases`` - a list of more or less free form strings that
            enables easier discovery of the data via searches.

    Use the method :meth:`Submission.meta` to create the meta information 

    >>> import hepdata as hd
    >>> submission = hd.submission()
    >>> meta       = submission.meta('Name','Description','File name')
    
    and then use the method :meth:`Meta.table` to get the data table
    of this meta data to fill in with values or manipulate

    >>> table = meta.table()

    Alternatively use :meth:`Submission.table` for simpler creation of
    both meta data and table in one go with automatic fill-in of many
    fields.

    Parameters
    ----------
    name : str 
        Name of the table 
    description : str 
        Description of data 
    filename : str or None 
        File to write the data to.  If none, then the data table will
        be written to the same document as the meta data.

    """
    #: Name field name 
    NAME = 'name'
    #: Decription field name 
    DESCRIPTION = 'description'
    #: Data_File field name
    DATA_FILE = 'data_file'
    #: Keywords field name
    KEYWORDS = 'keywords'
    #: Additional resources field name
    ADDITIONAL_RESOURCES = 'additional_resources'
    #: Location field name
    LOCATION = 'location'
    #: Group field name
    GROUP = 'group'
    #: Centre of mass energies keyword name
    CMENERGIES = 'cmenergies'
    #: Observables keyword name
    OBSERVABLES = 'observables'
    #: Phrases keyword name
    PHRASES = 'phrases'
    #: Reactions keytword name
    REACTIONS = 'reactions'
    #: Type field name
    TYPE = 'type'
    #: Identifier field name
    IDENTIFIER = 'identifier'
    #: Values field name
    VALUES = 'values'
    #: Data License field name
    DATA_LICENSE = 'data_license'

    @accepts(name=str,description=str,filename=str)
    def __init__(self,name,description,filename=None):
        super(Meta,self).__init__(self.DATA_LICENSE)
        self._d = {self.NAME: name,
                   self.DESCRIPTION: description,
                   self.KEYWORDS: [],
                   self.ADDITIONAL_RESOURCES: [],
        }
        if filename is not None:
            self._d[self.DATA_FILE] = filename
        self._t = None  # the data table
        
    @property 
    def name(self):
        return self._d.get(self.NAME,'')

    @name.setter
    @accepts(n=str)
    def name(self,n):
        self._d[self.NAME] = n
        return self
    
    @property 
    def description(self):
        return self._d.get(self.DESCRIPTION,'')

    @description.setter
    @accepts(desc=str)
    def description(self,desc):
        self._d[self.DESCRIPTION,''] = desc
        return self
    
    @accepts(name=str,url=str,description=str)
    def license(self,name=None,url=None,description=None):
        """Set license of the data

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
        self : Meta
            Reference to this object 
        """
        self._d[self._license_key] = self._license(name,url,description)
        return self

    def licenseName(self):
        return self._d.get(self._license_key,{}).get(Licensed.NAME,[])
    def licenseUrl(self):
        return self._d.get(self._license_key,{}).get(Licensed.Url,[])
    def licenseDescription(self):
        return self._d.get(self._license_key,{}).get(Licensed.DESCRIPTION,[])
        
    
    @accepts(name=str,values=(list,tuple,float,str),replace=bool)
    def keyword(self,name,values=None,replace=True):
        """Add a keyword to the meta data.  

        Parameters
        ----------
        name : str 
            Name of keyword (cmenergies,reaction,observables,phrases)
        values : any 
            Value(s) of keyword.  If None, remove the keyword altogether. 
        replace : bool 
            If the keyword is already set, replace with new value, 
            otherwise append

        Returns
        -------
        self : Meta
            Reference to this object 
        """
        match = next((k for k in self._d[self.KEYWORDS]
                      if k[self.NAME] == name), None)
        values = _ensureList(values)
        if values is None or len(values) < 1:
            if match is not None:
                self._d[self.KEYWORDS].remove(match)
            return self
        
        if match is None:
            self._d[self.KEYWORDS].append({self.NAME:name,
                                           self.VALUES:values})
        else:
            if replace is not None and replace:
                match[self.VALUES] = values
            else:
                match[self.VALUES] += values
        
        return self

    def keywords(self,select=None):
        l = self._d.get(self.KEYWORDS,[])
        if select is None:
            return l

        if callable(select):
            return [k for k in l if select(k)]

        if type(select) not in [list,tuple]:
            select = [select]

        return [k for k in l if k[self.NAME] in select]

    @property
    def the_keywords(self):
        return self._d.get(self.KEYWORDS,[])

    @accepts(values=(list,tuple,float,str),replace=bool)
    def cmenergies(self,values,replace=True):
        """Set center of mass energies

        Parameters
        ----------
        values : value or list 
            List of values

        Returns
        -------
             self : Meta 
                 Reference to self
        """
        return self.keyword(self.CMENERGIES,values,replace)

    @property
    def the_cmenergies(self):
        return self.keywords(self.CMENERGIES)
    
    @accepts(values=(list,tuple,str),replace=bool)
    def observables(self,values,replace=True):
        """Set center of mass energies

        Parameters
        ----------
        values : value or list 
            List of values

        Returns
        -------
        self : Meta 
            Reference to self
        """
        return self.keyword(self.OBSERVABLES,values,replace)
    
    @property
    def the_observables(self):
        return self.keywords(self.OBSERVABLES)

    @accepts(values=(list,tuple,str),replace=bool)
    def phrases(self,values,replace=True):
        """Set the reactions of mass energies

        Parameters
        ----------
        values : value or list 
            List of values

        Returns
        -------
        self : Meta 
            Reference to self
        """
        return self.keyword(self.PHRASES,values,replace)

    @property
    def the_phrases(self):
        return self.keywords(self.PHRASES)

    @accepts(values=(list,tuple,str),replace=bool)
    def reactions(self,values,replace=True):
        """Set center of mass energies

        Parameters
        ----------
        values : value or list 
            List of values

        Returns
        -------
        self : Meta 
            Reference to self
        """
        return self.keyword(self.REACTIONS,values,replace)

    @accepts(location=str,description=str,tpe=str)
    def resource(self,location,description,tpe=None):
        """Add an additional resource
        
        Parameters
        ----------
        location : str 
            Location - for example a URL or local file 
        description : str 
            A short description of the resource 
        type : str 
            Resource type 
        
        Returns
        -------
        r : Resource 
            Newly created resource object 
        """
        r = Resource(location,description,tpe)
        self._d[self.ADDITIONAL_RESOURCES].append(r._d)
        return r

    @property
    def the_resources(self):
        return self._d.get(self.ADDITIONAL_RESOURCES,None)

    @accepts(loc=str)
    def location(self,loc):
        """Add a location to the table

        Parameters
        ----------
        loc : str 
            Location (e.g. Figure 1) of data
        
        Returns
        -------
        self : Meta 
            Reference to this object
        """
        self._d[self.LOCATION] = loc
        return self

    def getLocation(self):
        """Get location field"""
        return self._d.get(self.LOCATION,None)

    @property
    def the_location(self):
        return self._d.get(self.LOCATION,None)

    @accepts(g=(int,str))
    def group(self,g=None):
        """Add a group to the table
        
        DEPRECATED 

        Parameters
        ----------
        g : str or int
            Group (e.g. Figure 1) of data
        
        Returns
        -------
        self : Meta 
            Reference to this object
        """
        # if g is not None:
        #    self._d[self.GROUP] = g
        return self

    @property
    def the_group(self):
        return self


    @accepts(same=bool)
    def table(self,same=False):
        """Get the data
        
        Parameters
        ----------
        same : bool (optional)
            If true, then we will put the data table into the same
            file as the submission it self.

        Returns
        -------
        t : Data 
             The data of this table

        """
        if self._t is None:
            self._t = Table(self._d[self.NAME] if same else None)
        return self._t

    @property
    def the_table(self):
        '''Get the data'''
        return self._t
    
    def allInOne(self):
        """Check if we should write the data table to the same file as the
        meta information.

        Returns
        -------
        ret : bool
            True if the data table should be written to the same
            file as the meta data
        """
        if self._t is None:
            raise RuntimeError('No data table defined for this Meta object: {}'
                               .format(self._d['name']))        
        return (self._t._d.get(Table.NAME,'') == self._d[self.NAME]
                or self.DATA_FILE not in self._d)

    def dataFile(self):
        """Get name of data file to write to, or None if all should 
        go in the same file

        """
        if self.allInOne():
            return None

        return self._d.get(self.DATA_FILE,None)

    @accepts(ny=int,nx=int)
    def round(self,ny,nx=None):
        """Round independent and dependent variables to nx and ny decimal
        digits.

        Parameters
        ----------
        ny : int, positive 
            Number of decimal digits to round dependent
            variables to
        nx : int, positive (optional)
            Number of decimal digits to round independent
            variables to.  If not specified, default to value of ny 
        
        Returns
        -------
        self : Meta 
             Reference to self

        """ 
        if self._t is None:
            return self

        self._t.round(ny,nx)
        return self

    @accepts(ny=int,nx=int)
    def roundNsig(self,ny,nx=None):
        """Round independent and dependent variables to nx and ny significant
        digits.

        Parameters
        ----------
        ny : int, positive 
            Number of significant digits to round dependent
            variables to
        nx : int, positive (optional)
            Number of significant digits to round independent
            variables to.  If not specified, default to value of ny 
        
        Returns
        -------
        self : Meta 
             Reference to self
        """ 
        if self._t is None:
            return self

        self._t.roundNsig(ny,nx)
        return self

    @classmethod
    def fromDict(cls,d,t=None):
        """Construct a Meta object from a dictionary

        Parameters
        ----------
        d : dict 
            Dictionary to construct from.  This could be read from a
            YAML/JSON file.
        t : dict or Table (optional
            Table object or dictionary to construct Table object from 
        
        Returns
        -------
        m : Meta 
            Newly constructed Meta object 
        """
        assert d.get(cls.NAME,False),\
            "No {} in dictionary".format(cls.NAME)
        assert d.get(cls.DESCRIPTION,False),\
            "No {} in dictionary".format(cls.DESCRIPTION)
        #assert d.get(cls.DATA_FILE,False),\
        #    "No {} in dictionary".format(cls.DATA_FILE)

        m = Meta(d[cls.NAME],
                 d[cls.DESCRIPTION],
                 d.get(cls.DATA_FILE,None))
        m._d = d

        if t is not None:
            if type(t) is Table:
                m._t = t
            else:
                tt = Table.fromDict(t)
                m._t = tt

        return m
        
    def clean(self,**kwargs):
        """Clean up the dictionary for empty lists"""
        if len(self._d[self.ADDITIONAL_RESOURCES]) <= 0:
            del self._d[self.ADDITIONAL_RESOURCES]
        if len(self._d[self.KEYWORDS]) <= 0:
            del self._d[self.KEYWORDS]
        
        return self

    use_beautifier = {'text/html': True,
                      'text/latex': True,
                      'text/markdown': True }
    '''Class option for whether to use the names interface to beautify
    names.  This is a dictionary that maps from mime representation to
    a boolean option.  If a mimetype isn't present in the dictionary
    then beautification isn'tr used'''

    show_tables = {'text/html': False,
                   'text/latex': False,
                   'text/markdown': False }
    
    def _beautifier(self,mime): 
        '''Get the beautifier depending on the mime type and the setting 
        in use_beautifier'''
        if Table.use_beautifier.get(mime,False):
            from . names import Beautifier
            return Beautifier()
        return None
    
    def __repr__(self):
        return self._d[self.NAME] + ': '+self._d[self.DESCRIPTION]
    
    def _repr_html_(self):
        '''Get HTML representation of this meta data (and table)
        '''

        b = self._beautifier('text/html')
        
        o = f'<div><div><b>{self._d[self.NAME]}</b></div>'+'\n'

        if self.DATA_FILE in self._d:
            o += f'<div><tt>{self._d[self.DATA_FILE]}</tt></div>'+'\n'

        o += f' <div>{self._d[self.DESCRIPTION]}</div>'+'\n'

        if len(self._d[self.KEYWORDS]) > 0:
            o += ' <dl>\n'
            o += '\n'.join([f' <dt>{k[self.NAME]}</dt><dd>' +
                            ','.join([f'{b.qual(k[self.NAME],v)}'
                                      for v in set(k[self.VALUES])])
                            + '</dd>' for k in self._d[self.KEYWORDS]])
            o += ' </dl>\n'

        if Meta.show_tables.get('text/html',False):
            if self._t is not None: o += self._t._repr_html_()

        o += '</div>'

        return o

    def _repr_markdown_(self):
        '''Get Markdown representation of this meta data (and table)

        '''
        b = self._beautifier('text/markdown')

        o = f'## {self._d[self.NAME]}'+'\n\n'

        if self.DATA_FILE in self._d:
            o += f'{self._d[self.DATA_FILE]}`'+'\n'

            o += f'{self._d[self.DESCRIPTION]}'+'\n\n'

        o += '\n'.join([f'- {k[self.NAME]}: '+
                        ','.join([f'{b.qual(k[self.NAME],v)}'
                                  for v in set(k[self.VALUES])])
                        for k in self._d[self.KEYWORDS]])


        if Meta.show_tables.get('text/markdown',False):
            if self._t is not None:
                o += self._t._repr_markdown_()

        return o

    def _repr_latex_(self):
        if not Meta.show_tables.get('text/latex',False):
            return
        
        o = r'\begin{table}\centering'

        if self._t is not None:
            o += self._t._repr_latex_() + '\n'

        o += fr' \caption{{{self._d[self.DESCRIPTION]}}}'+'\n'
        o += r'\end{table}'

        return o

    def _repr_mimebundle_(self,include=None,exclude=None):
        '''Get mime representation of this table'''
        return {'text/html': self._repr_html_(),
                'text/markdown': self._repr_markdown_(),
                'text/latex': self._repr_latex_() }
    
#
# EOF
# 
