"""Container of a submission 

Copyright 2019 Christian Holm Christensen
"""
from . accepts import accepts
from . meta import Meta
from . table import Table 
from . search import Search
from . utils import _ensureList
from . resource import Resource

class Submission:
    """Container of submission
    
    Objects of this class acts as a container for the full submission,
    including auxiliary files, table meta data, table data, references
    to journal, arXiv, inSpire and so on.  To start, one can create an
    object of this class

    >>> import hepdata as hd
    >>> submission = hd.submission()
    
    Various fields can be specified, such as auxiliary files,
    references to jounral, preprint, databases, and so on, either by
    hand or via an `inSpire <https://inspirehep.net>`_ look-up using
    the method Submission.fill()

    Tables are created in the submission via the methods
    Submission.meta() to create the meta data from which we can obtain
    the data table

    >>> meta = submission.meta('Name','Description',Data file')
    >>> table = meta.table()

    or more directly using the method Submission.table() 

    >>> table = submission.table('Description','System','Sqrt s',
    ...                          'Independent variable(s),
    ...                          'Dependent varibable(s)',
    ...                          'Particle(s)',
    ...                          'Phrases',
    ...                          Number, 'Sub-number')

    Once all data tables have been filled, we can round the values to
    `n` significant digits using the method Submission.roundNsig()

    >>> submission.roundNsig(2) 
    
    Submissions can be written and read from disk (including from Zip
    or Tar - possibly compressed - archives) using the hepdata.io
    subsystem.  This allows one to easily prepare a submission, or
    import a full submission from the `HEPData <https://hepdata.net>`_
    web-site.

    """
    
    #: Url field name
    URL = 'url'
    #: Description field name
    DESCRIPTION = 'description'
    #: Comment field name
    COMMENT = 'comment'
    #: Additional_Resources field name
    ADDITIONAL_RESOURCES = 'additional_resources'
    #: Record_Ids field name
    RECORD_IDS = 'record_ids'
    #: Type field name
    TYPE = 'type'
    #: Identifier field name
    IDENTIFIER = 'identifier'
    #: Id field name
    ID = 'id'
    #: Preprintyear field name
    PREPRINTYEAR = 'preprintyear'
    #: Publicationyear field name
    PUBLICATIONYEAR = 'publicationyear'
    
    def __init__(self):
        self._d = {
            self.ADDITIONAL_RESOURCES: [],
            self.RECORD_IDS: [],
        }
        self._t = {}
        self._l = None

    @accepts(name=str,description=str,filename=str)
    def meta(self,name,description=None,filename=None):
        """Add a table to the submission

        Parameters
        ----------
        name : str 
             Name of table 
        description : str 
             Description of the table 
        filename : str 
             File name of file to write data to
        
        Returns
        -------
        t : Meta 
            Newly created table object 

        """
        if name in self._t:
            print('Returning existing meta {}'.format(name))
            return self._t[name]

        assert name is not None,'Name cannot be None'
        assert description is not None,'Description cannot be None'
        
        t = Meta(name,description,filename)
        self._t[name] = t

        if self._l is not None:
            t.license(self._l.get('license',''),
                      self._l.get('url',''))

        return t

    def metas(self,byloc=False):
        """Get list of all meta data
        
        Parameters
        ----------
        byloc : bool 
            If true, return dict with lists of locations.  Metas
            without a location field are assigned to the key "-".

        Returns
        -------
        metas : generator or dict 
            List of metas, or dict (if byloc is true) of lists of
            metas by location.
        """
        if not byloc:
            return self._t.values()
        
        ret = dict()
        for m in self._t.values():
            loc = m.getLocation()
            if loc is None:
                loc = m.name

            if not loc in ret:
                ret[loc] = []

            ret[loc].append(m)

        return ret

    @accepts(description=str,
             sys=(list,tuple,float,str),
             sqrts=(list,tuple,float,str),
             var=str,
             obs=(str,list),
             parts=(str,list),
             phrases=(str,list),
             num=int,
             subnum=None,
             name=str,
             filename=str,
             loc=str,
             same=bool,
             both=bool)
    def table(self,
              description,
              sys,
              sqrts,
              var,
              obs,
              parts=[],
              phrases=[],
              num=None,
              subnum='',
              name=None,
              filename=None,
              loc=None,
              same=False,
              both=False):
        """Add a data table with meta information to the submission 

        This method allows one to quickly set-up a data table.

        Note, the argument sets name,filename,loc and num,subnum are
        mutually exclusive.  That is num (and optionally subnum) will
        override the name, filename, and loc arguments.

        Parameters
        ----------
        description : str 
            A description 
        sys : str or list 
            Collision system
        sqrts : float or list 
            Collision energy 
        var : str
            Independent variable name
        obs : str or list 
            Dependent variable name(s)
        parts : str or list  (optional)
            Produced particle(s).  If scalar (a str) it will be
            combined with all collision systems (sys) to from the
            reactions.
        
            If a list of string, each element (str) is combined
            with all entries in the collision system to form the
            reactions.

            If a list of lists of strings, then the list must have
            equal length to the collision systems, and each element in
            sublists are combined with the collision systems (sys) to
            from the reactions.

            If the value None is specified assume X
        phrases : str or list (optional)
            Phrases keywords 
        num : int (optional)

            Table number.  Sets the data name.  Mutually exclusive
            with name, filename, and loc arguments
        subnum : any type  (optional)
            Table sub-number. Sets the data name.  Mutually exclusive
            with name, filename, and loc arguments
        name : str  (optional)
            Name of table.  Mutually exclusive with arguments 
            num and subnum            
        filename : str  (optional)
            Name of file to write data to. Mutually exclusive with
            arguments num and subnum
        loc : str (optional)
            Location. Mutually exclusive with
            arguments num and subnum
        same : bool (optional)
            If true, then we will put the data table into the same
            file as the submission it self.
        both : bool (optional)
            If true, return (table,meta) instead of just the table 

        Returns
        -------
        table, meta : Table (optionally Meta)
            Data table and if both is true also the meta object

        """
        grp = None
        if num is not None:
            name = 'Table {}{}'.format(num,subnum)
            filename = 'tab{}{}.yaml'.format(num,subnum)
            loc = 'Table {}'.format(num)
            if subnum is not None and str(subnum) != '':
                grp = 'Table {}'.format(num)
            
        if name is None:
            raise ValueError('No name given')

        if parts is None:
            parts = 'X'
        
        reactions = []
        sl        = _ensureList(sys)
        if type(parts) not in [list,tuple]:
            reactions = ['{} --> {}'.format(s,parts) for s in sl]
        else:
            if any([type(p) in [list,tuple] for p in parts]):
                if len(parts) != len(sl):
                    raise ValueError('List of list of particles not as '
                                     'long ({}) as list of systems ({})'
                                     .format(len(parts),len(sl)))

                for s,pl in zip(sl,parts):
                    reactions += ['{} --> {}'.format(s,p)
                                  for p in _ensureList(pl)]
            else:
                reactions += ['{} --> {}'.format(s,p)
                              for p in parts for s in sl]

        # Why set(...)
        meta = self.meta(name,description,filename)\
            .reactions(reactions)\
            .observables(obs)\
            .cmenergies(sqrts)\
            .phrases(phrases)\
            .location(loc)\
            .group(grp)
        tab = meta.table(same)

        if both:
            return  tab, meta
        return tab

    @property 
    def comment(self):
        return self._d.get(self.COMMENT,None)

    @comment.setter
    @accepts(comment=str)
    def comment(self,comment):
        """Add comment (abstract) to submission
        
        Parameters
        ----------
        comment : str 
            Comment of the submission 

        Returns
        -------
        self : Submission 
            Reference to this object 
        """
        self._d[self.COMMENT] = comment
        return self 

    abstract = comment
    """Alias definition"""
    
    def ids(self,select=None):
        if select is None:
            return self._d.get(self.RECORD_IDS,[])

        if callable(select):
            return [r for r in self._d.get(self.RECORD_IDS,[])
                    if select(r)]
        
        if type(select) not in [list,tuple]:
            select = [select]

        return [r for r in self_d.get(self.RECORD_IDS,[])
                if r[self.TYPE] in select]
    
    @accepts(type=str,id=(str,int))
    def id(self,type,id):
        """Add a record ID to this submission

        Parameters
        ----------
        type : str 
            Type of record (inspire,spires,cds)
        id : str or in 
            Identifier
        
        Returns
        -------
        self : Submission 
            Reference to this object
        """
        self._d[self.RECORD_IDS].append({self.TYPE:type,self.ID:id})
        return self

    @property
    def preprinted(self):
        return self._d.get(self.PREPRINTYEAR,None)

    @preprinted.setter
    @accepts(year=str)
    def preprinted(self,year):
        """Set year of preprint

        Parameters
        ----------
        year : str 
            Year of first preprint 
        
        Returns
        -------
        self : Submission 
            Reference to this object

        """
        self._d[self.PREPRINTYEAR] = str(year)
        return self

    @property
    def published(self):
        return self._d.get(self.PUBLICATIONYEAR,None)

    @published.setter
    @accepts(year=str)
    def published(self,year):
        """Set year of publication

        Parameters
        ----------
        year : str 
            Year of first preprint 
        
        Returns
        -------
        self : Submission 
            Reference to this object

        """
        self._d[self.PUBLICATIONYEAR] = str(year)
        return self

    @property
    def url(self):
        return self._d.get(self.URL,None)

    @url.setter
    @accepts(url=str)
    def url(self,url):
        self._d[self.URL] = url
        return self

    @property
    def type(self):
        return self._d.get(self.TYPE,'')

    @type.setter
    @accepts(type=str)
    def type(self,type):
        self._d[self.TYPE] = type
        return self

    @property
    def description(self):
        return self._d.get(self.DESCRIPTION,'')

    @description.setter
    @accepts(description=str)
    def description(self,description):
        self._d[self.DESCRIPTION] = description
        return self
    
    
    def resources(self,select=None):
        if select is None:
            return self._d.get(self.ADDITIONAL_RESOURCES,[])

        if callable(select):
            return [r for r in self._d.get(self.ADDITIONAL_RESOURCES,[])
                    if select(r)]
        
        if type(select) not in [list,tuple]:
            select = [select]

        return [r for r in self._d.get(self.ADDITIONAL_RESOURCES,[])
                if r[Resource.LOCATION] in select]
    
    @accepts(location=str,description=str,type=str)
    def resource(self,location,description,type=None):
        """Add an additional resource

        Parameters
        ----------
        location : str 
            Location - for example a URL or local file 
        description : str 
            A short description of the resource 
        
        Returns
        -------
        r : Resource 
            Newly created resource object 
        """
        r = Resource(location,description,type)
        self._d[self.ADDITIONAL_RESOURCES].append(r._d)
        return r

    @accepts(publ=str)
    def fill(self,publ):
        """Queries inspire and fill in information 

        Parameters
        ----------
        publ : string 
            Publication to search for 
        
        Returns
        -------
        self : Submission 
            Reference to this object

        """
        from re import sub
        from pprint import pprint
        
        s = Search()
        data = s.query('find j '+publ)[0]
        if data is None:
            raise RuntimeError('Query for information on '
                               +publ+' failed')

        meta = data.get('metadata',{})
        exp = meta.get('collaborations',[{}])[0].get('value','')
        if exp != '':
            exp += '. '
        abs = meta['abstracts']
        # pprint(abs)
        if type(abs) is list:
            # Prefer arXiv suggestion
            xabs = [x.get('value','') for x in abs
                    if x.get('source','') == 'arXiv']
            abs = xabs[0] if len(xabs) > 0 else abs[0].get('value','')

        abs = sub(r'\t+',' ',abs)
            

        self.comment    = exp+abs
        self.preprinted = meta['preprint_date']
        self.id('inspire',data['id'])\
            .id('arxiv',  meta['arxiv_eprints'][0]['value'])

        if 'publication_info' in meta:
            self.published  = meta['publication_info'][0]['year']
        if 'doi' in meta:
            self.id('doi', meta['dois'][0]['value'])
            
        old = [e.get('value','NONE')
               for e in meta.get('external_system_identifiers',{})
               if e['schema'] == 'SPIRES']
        if old is not None and len(old) > 0:
            sysno = old[0].split('-')
            self.id(sysno[0],sysno[1])

        self._l = meta.get('license',None)

    def clean(self,**kwargs):
        """Clean-up unused entries"""
        
        if len(self._d[self.ADDITIONAL_RESOURCES]) <= 0:
            del self._d[self.ADDITIONAL_RESOURCES]
        if len(self._d[self.RECORD_IDS]) <= 0:
            del self._d[self.RECORD_IDS]

        for t in self._t.values():
            t.clean(**kwargs)
        

    @accepts(ny=int,nx=int)
    def roundNsig(self,ny,nx=None):
        """Round to ny(nx) significant digits"""
        if isinstance(self._t,dict):
            for t in self._t.values():
                t.roundNsig(ny,nx)
        elif isinstance(self._t,list):
            for t in self._t:
                t.roundNsig(ny,nx)
            

        return self

    def _repr_html_(self):
        '''Get HTML representation of this meta
        data (and table)'''
        o = '<div>\n'+\
            f'  <div>{self.description}</div>'+'\n' + \
            f'  <div>{self.type}</div>'+'\n' + \
            f'  <div>{self.abstract}</div>'+'\n' + \
            '  <table>\n'
        for id in self.ids():
            o += '    <tr>\n' + \
                 f'      <td>{id[self.TYPE]}</td>'+'\n' + \
                 f'      <td>{id[self.ID]}</td>'+'\n' + \
                 '    </tr>\n'

        o += '  </table>\n'
        for m in self._t.values():
            o += m._repr_html_()
            
        o += '</div>\n'

        return o

    def _repr_markdown_(self):
        '''Get Markdown representation of this meta data (and table)'''

        o = '---\n' + \
            f'{self.description}'+'\n\n' + \
            f'{self.type}'+'\n\n' + \
            f'{self.abstract}'+'\n\n' + \
            '| Type | Reference |\n' + \
            '|------|-----------|\n'
        for id in self.ids():
            o += f'|{id[self.TYPE]}|{id[self.ID]}|'+'\n'

        o += '\n'
        for m in self._t.values():
            o += m._repr_html_() + '\n'
            
        return o

    def _repr_mimebundle_(self,include=None,exclude=None):
        '''Get mime representation of this table
        '''

        return {'text/html':  self._repr_html_(),
                'text/markdown': self._repr_markdown_() }
    
    
# ====================================================================
#
# EOF
#
