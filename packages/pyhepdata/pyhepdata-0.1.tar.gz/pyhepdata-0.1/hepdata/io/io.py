"""Base class for I/O classes. 

Provides services

Copyright 2019 Christian Holm Christensen
"""
import yaml
from .. meta import Meta
from .. table import Table
from .. submission import Submission
from . validator import Validator
from . messages import Message
from pprint import pprint

class IO:
    def __init__(self,v=None,verbose=False):
        self._v = v
        self._tables = {}
        self._verbose = verbose
        
    def _ensureData(self,stream,data,**kwargs):
        """Ensure that we have data 

        Parameters
        ----------
        stream : stream 
            Possible input stream to read from 
        data : list or dict
            Possibly already read data or None
            
        Returns
        -------
        data : list 
            Possibly read data, or existing data 
        """
        if data is not None:
            if type(data) is dict:
                return [data]
            return list(data)

        if self._verbose:
            print('Loading YAML from {}'.format(stream.name))

        tables = kwargs.pop('table',None)
        metas = kwargs.pop('meta',None)
        kwargs['Loader'] = yaml.SafeLoader
        data = list(yaml.load_all(stream,**kwargs))
        if not tables:
            return data
            
        # Now loop over all documents and extract tables
        # First, read in all tables there might be in the file.
        # This includes possible validation of those files.  We do
        # this, so that we can later on cleanly define our meta
        # objects with the already defined table object.
        for doc in data:
            if not self._isTable(doc) or Table.NAME not in doc:
                continue 

            # Read in the data table. Note, we need to pass in the
            # self.FILENAME key again
            if self._verbose:
                print('TABLE from {}'.format(stream.name))
            # pprint(doc)
            t = self._loadTable(stream,doc,**kwargs)
            if not Table.NAME in t._d:
                print('No name in read table from {} with {}: '
                      .format(stream.name,tables))
            self._tables[t._d[Table.NAME]] = t
            
        return data

    def _dumpYaml(self,doc,stream,**kwargs):
        if self._verbose:
            print('Dumping dictionary to {}'.format(stream.name))
            
        kwargs['allow_unicode'] = True
        kwargs['encoding'] = 'utf-8'
        kwargs.pop('table',None)
        kwargs.pop('meta',None)
        yaml.safe_dump(doc, stream,  **kwargs)
        
    def _isTable(self,doc):
        """Check if read-in document is a table 
        
        Parameters
        ----------
        doc : dict 
            Read in document 
        
        Returns
        -------
        istable : bool 
            True if document is a data table 
        """
        return ((Table.INDEPENDENT_VARIABLES in doc or
                 Table.DEPENDENT_VARIABLES in doc)
                and not Meta.DESCRIPTION in doc)
    
    def _isMeta(self,doc):
        """Check if read-in document is table meta information (a submission
        entry)
        
        Parameters
        ----------
        doc : dict 
            Read in document 
        
        Returns
        -------
        ismeta : bool 
            True if document is table meta information

        """
        return (doc.get(Meta.DATA_FILE,False) or
                (doc.get(Meta.KEYWORDS,False) and
                 doc.get(Meta.DESCRIPTION,False) and
                 doc.get(Meta.NAME,False)))

    def _validate(self,fn,data,norecurse=False):
        if self._v is None:
            return True

        # print('Validate data {} from {}'.format(data,fn))
        if not self._v.validate(filename=fn, data=data,
                                norecurse=norecurse):
            self._v.summarize(filename=fn,least=Message.INFO)
            self._v.printMessages(None,Message.INFO)
            raise RuntimeError('Failed to validate')
        if self._verbose:
            print('Dictionary from {} validated'.format(fn))
        return True

    def _dumpTable(self,tab,stream,**kwargs):
        """Dumps table to stream"""
        self._validate(stream.name, tab._d)

        if self._verbose:
            print('TABLE to {}'.format(stream.name))

        self._dumpYaml(tab._d, stream, **kwargs)

    def dumpTable(self,tab,filename,**kwargs):
        """Write a table to a file 

        Parameters
        ----------
        tab : Table
            Table to write 
        filename : str 
            Name of file to write to 
        **kwargs : dict 
            Additional arguments 
        """
        with self._ensureStream(filename,'w') as stream:
            self._dumpTable(tab,stream)

    def _dumpMeta(self,mta,stream,**kwargs):
        """Dumps meta data (and nothing else) to stream 
        after possible validation"""
        if self._verbose:
            print('META {} to {} ({})'
                  .format(mta._d[Meta.NAME], stream.name,
                          mta._d.get(Meta.DATA_FILE,'<>')))

        table = kwargs.get('table',False)
        out   = mta._d
        if out.get(Meta.DATA_FILE,None) is None:
            if self._verbose:
                print('META has no data_file field')
            # New style in-doc data table.  Make copy of dictionary
            # and append the table information to it
            out = dict(mta._t._d,**out)
            table = False
            
        self._validate(stream.name, out, True)
        
        kwargs['explicit_start'] = True        
        self._dumpYaml(out, stream, **kwargs)

        if table and mta.dataFile() is None:
            if self._verbose:
                print('TABLE to same file {} as META {}'.format(stream.name,
                                                                mta.name))
            self._dumpTable(mta._t, stream, **kwargs)

    def dumpMeta(self,mta,filename,**kwargs):
        """Write a meta information to a file 

        Parameters
        ----------
        meta : Meta
            Meta information to write 
        filename : str 
            Name of file to write to 
        **kwargs : dict 
            Additional arguments 
            - table : bool 
                 If true, also write out table (separate file or same)

        """
        table = kwargs.get('table',False)
        with self._ensureStream(filename,'w') as stream:
            self._dumpMeta(mta,stream)

        if not table:
            return
            
        with self._ensureStream(mta.dataFile(),'w') as stream:
            self._dumpTable(mta._t, stream)

    def _dumpSubmission(self,sub,stream,**kwargs):
        """Dumps the submission (and nothing else) to stream,
        after possible validation"""

        self._validate(stream.name,sub._d)
        
        kwargs['explicit_start'] = True
        self._dumpYaml(sub._d, stream, **kwargs)

    def dumpSubmission(self,sub,filename,**kwargs):
        """Write a submission information to a file 

        Parameters
        ----------
        sub : Submission
            Submission information to write 
        filename : str 
            Name of file to write to 
        **kwargs : dict 
            Additional arguments 
            - meta : bool 
                 If true, also write out meta information
            - table : bool 
                 If true, also write out table (separate file or same)

        """
        table = kwargs.get('table',False)
        meta  = kwargs.get('meta', False)
        with self._ensureStream(filename,'w') as stream:
            if self._verbose:
                print('SUBMISSION to {}'.format(stream.name))
                
            self._dumpSubmission(sub,stream)

            if not meta:
                if self._verbose:
                    print('Skipping Metas')
                    
                return

            for m in sub._t.values():
                self._dumpMeta(m,stream,**kwargs)

        if not table:
            # print('Skipping tables')
            return
        
        for m in sub._t.values():
            if m.dataFile() is not None:
                with self._ensureStream(m.dataFile(),'w') as stream:
                    if self._verbose:
                        print('META {} TABLE to {}'
                              .format(m._d[Meta.NAME],stream.name))
                        
                    self._dumpTable(m._t, stream)

    def _dumpAll(self,sub,filename='submission.yaml',**kwargs):
        """Write out all data to files 

        Parameters
        ----------
        sub : Submission
            Submission to write out 
        filename : str 
            File to write main information to 
        **kwargs : dict 
            Additional arguments 
        """
        kwargs['table'] = True
        kwargs['meta']  = True
        return self.dumpSubmission(sub,filename,**kwargs)
            
    def _loadTable(self,stream,data=None,**kwargs):
        """Load table (and only table) from stream"""
        data = self._ensureData(stream,data,**kwargs)
        if data is None or (type(data) in [list,tuple] and len(data) < 1):
            return None
        doc  = data[0]

        # Validate the entry.  Note, we do not want to recurse and
        # validate data tables, as we've already done that of
        # in-file data tables.
        self._validate(stream.name,doc,True)

        # print('Loading table from {} with'.format(stream.name))
        # pprint(doc)
        return Table.fromDict(doc)

    def loadTable(self,filename,**kwargs):
        """Load a table from a file (note, the meta information is not read)

        Parameters
        ----------
        filename : str 
            Name of file to read from 
        **kwargs : dict 
            Additional arguments

        Returns
        -------
        table : Table 
            Read table 
        """
        with self._ensureStream(filename,'r') as stream:
            return self._loadTable(stream,None,**kwargs)
        
    def _loadMeta(self,stream,data=None,**kwargs):
        """Load meta information (and nothing else) from stream or data"""
        # Make sure we have the data by possibly reading from stream
        data = self._ensureData(stream,data,**kwargs)
        doc  = data[0]

        # Validate the entry.  Note, we do not want to recurse and
        # validate data tables, as we've already done that of
        # in-file data tables.
        self._validate(stream.name,doc,True)

        # Check if we have the table already, and if so, set it
        # on the object
        t = self._tables.get(doc[Meta.NAME],None)
        if t is None and doc.get(Meta.DATA_FILE,None) is None:
            t = Table.fromDict({Table.INDEPENDENT_VARIABLES:
                                doc.pop(Table.INDEPENDENT_VARIABLES),
                                Table.DEPENDENT_VARIABLES:
                                doc.pop(Table.DEPENDENT_VARIABLES)})
        return Meta.fromDict(doc,t)

    def loadMeta(self,filename,**kwargs):
        """Read meta information from a file.  

        Notes
        -----
        It is assumed that the meta information is the first (and
        possibly only) document in the file.

        Parameters
        ----------
        filename : str 
            Name of file to read from 
        **kwargs : dict 
            Additional arguments
            - tables : bool 
               If true, also read in the data table 

        Returns
        -------
        meta : Meta 
            Read meta information 
        """
        tables = kwargs.get('table',False)
        with self._ensureStream(filename,'r') as stream:
            meta = self._loadMeta(stream,None,**kwargs)

        if tables and meta._t is None:
            if self._verbose:
                print('Reading table content from external file {}'
                      .format(meta[Meta.DATA_FILE]))
            with self._ensureStream(meta[Meta.DATA_FILE],'r') as stream:
                meta._t = self._loadTable(stream,None,**kwargs)

        return meta
            
    def _loadSubmission(self,stream,data=None,**kwargs):
        """Loads submission from stream (or data)""" 
        meta = kwargs.pop('meta',False)
        data = self._ensureData(stream,data,**kwargs)
        sub = Submission()

        if len(data) == 1 and self._isTable(data[0]):
            return self._loadTable(stream,data[0],**kwargs)
        if len(data) == 1 and self._isMeta(data[0]):
            return self._loadMeta(stream,data[0],**kwargs)
                                   
        for doc in data:
            if self._isTable(doc):
                if self._verbose:
                    print('TABLE from {}'.format(stream.name))
                # This has already been read
                continue
            if self._isMeta(doc):
                if self._verbose:
                    print('META from {}'.format(stream.name))
                if meta:
                    m = self._loadMeta(stream,doc,**kwargs)
                    sub._t[m.name] = m
                continue

            if self._verbose:
                print('ADDITIONAL from {}'.format(stream.name))
            # We got the submission information
            self._validate(stream.name,doc)
            sub._d = doc

        # Read in missing tables 
        for m in sub._t.values():
            if m._t is None:
                with self._ensureStream(m._d[Meta.DATA_FILE],'r') as stream:
                    m._t = self._loadTable(stream,None,**kwargs)
                
        return sub

    def loadSubmission(self,filename,**kwargs):
        """Read submission information from a file.  

        Notes
        -----
        It is assumed that the submission information is the first (and
        possibly only) document in the file.

        Parameters
        ----------
        filename : str 
            Name of file to read from 
        **kwargs : dict 
            Additional arguments
            - meta : bool 
               If true, also read in meta information 
            - table : bool 
               If true, also read in the data table 

        Returns
        -------
        sub : Submission 
            Read meta information 
        """
        with self._ensureStream(filename,'r') as stream:
            return self._loadSubmission(stream,None,**kwargs)

    def _loadAll(self,filename='submission.yaml',**kwargs):
        """Read all data from files.  

        Parameters
        ----------
        filename : str 
            File name of the master submission file
        **kwargs : dict
            Additional arguments 

        Returns
        -------
        sub : Submission 
            Read submission (including meta and table objects)
        """
        kwargs['table'] = True
        kwargs['meta']  = True
        return self.loadSubmission(filename,**kwargs)

                
            
#
# EOF
#

            
        
