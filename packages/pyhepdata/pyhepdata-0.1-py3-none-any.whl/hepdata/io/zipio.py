"""Input/output from file system files

Copyright 2019 Christian Holm Christensen
"""
import zipfile
import os 
from . io import IO
from .. submission import Submission
from .. resource import Resource

class ZipIO(IO):
    """Class to read submission data from filesystem files

    Parameters
    ----------
    v : Validator 

        If not None, it must be a validator class for the schemas
        used.  If set, we will use this object to validate entries
        before or after output or input, respectively
    """
    def __init__(self,v,verbose=False,**kwargs):
        super(ZipIO,self).__init__(v,verbose)
        if v:
            v._check_res = False
        self._ensureStream = None

    class _ensureZip:
        """Context manager to open a zip file and tie _ensureStream to that
        zip file.
        """

        def __init__(self,moth,filename,mode):
            if moth._verbose:
                print('Opening zip file {} in mode {}'
                      .format(filename,mode))
                
            self._mother = moth
            self._zip    = zipfile.ZipFile(filename,mode)
            self._mother._ensureStream = lambda filename, mode : \
                self._mother._ensureZStream(self._zip,filename,mode)

            if moth._verbose:
                print('Set _ensureStream to {}'
                      .format(self._mother._ensureStream))

        def __enter__(self):
            """Called upon context entry
        
            Returns
            -------
            s : stream 
                Our stream 
            """
            return self._zip

        def __exit__(self,tpe,val,tb):
            """Called upon leaving context 
            
            We close the file if we were the ones to open it 

            Parameters
            ----------
            tpe : Excption type 
                Possible exception type 
            val : Exception value 
                Possible exception value 
            tb : Traceback 
                Possible traceback 
            
            Returns 
            -------
            False : 
                We do not process the exceptions 
            """
            # print('Finished with {}'.format(self._s.name))
            self._zip.close()
            self._mother._ensureStream = None

    def _ensureZStream(self,z,filename,mode):
        _stream = z.open(filename,mode)
        setattr(_stream,'name',filename)
        return _stream

    def _extRes(self,z,d,filename,ext):
        """Extract additional reources from zip archive"""
        l = d.get(Submission.ADDITIONAL_RESOURCES,None)
        if l is None:
            return

        for ll in l:
            loc = ll.get(Resource.LOCATION,'')
            if len(loc) <= 0 or loc.startswith('http'):
                continue

            if loc not in z.namelist():
                print('{} is not a member of {}'.format(loc,filename))
                continue 

            if ext:
                tgt = os.path.dirname(filename)
                z.extract(loc,tgt)

    def load(self,filename='submission.zip',**kwargs):
        """Read all data from files.  

        Parameters
        ----------
        filename : str 
            File name of the master submission file
        **kwargs : dict
            Additional arguments 

            member : str 
                Name of file in archive to load 
            resources : bool 
                If true, extract all additional resources

        Returns
        -------
        sub : Submission 
            Read submission (including meta and table objects)
        """
        subfn = kwargs.pop('submission','submission.yaml')
        ext   = kwargs.pop('resources',False)
        with self._ensureZip(self,filename,'r') as z:
            sub = self._loadAll(subfn,**kwargs)

            self._extRes(z,sub._d,filename,ext)
            for m in sub._t.values():
                self._extRes(z,m._d,filename,ext)
        return sub
            

    def _addRes(self,z,d,filename):
        """Add additional resources to zip archive"""
        l = d.get(Submission.ADDITIONAL_RESOURCES,None)
        if l is None:
            return

        for ll in l:
            loc = ll.get(Resource.LOCATION,'')
            if len(loc) <= 0 or loc.startswith('http'):
                continue

            src = os.path.join(os.path.dirname(filename),loc)
            if os.path.isfile(src):
                z.write(src,loc)
            else:
                print('Additional resource {} not found'.format(src))
            
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

            meta : bool 
                If true, also write out meta information
            table : bool 
                If true, also write out table (separate file or same)
        """
        subfn = kwargs.pop('member','submission.yaml')
        if self._verbose:
            print('Write submission {} into {}'
                  .format(subfn, filename))

        meta = kwargs.get('meta',False)
        with self._ensureZip(self,filename,'w') as z:
            super(ZipIO,self).dumpSubmission(sub,subfn,**kwargs)

            self._addRes(z,sub._d,filename)
            if meta: 
                for m in sub._t.values():
                    self._addRes(z,m._d,filename)
            
    def dumpMeta(self,mta,filename,**kwargs):
        """Write a meta information to a file 

        Parameters
        ----------
        mta : Meta
            Meta information to write 
        filename : str 
            Name of file to write to 
        **kwargs : dict 
            Additional arguments 
            
            table : bool 
                If true, also write out table (separate file or same)
        """
        mtafn = kwargs.pop('member','submission.yaml')
        if self._verbose:
            print('Write meta {} into {}'
                  .format(mtafn, filename))
            
        with self._ensureZip(self,filename,'w') as z:
            super(ZipIO,self).dumpMeta(mta,mtafn,**kwargs)
            self._addRes(z,mta._d,filename)
            
    def dumpTable(self,tab,filename,**kwargs):
        """Write a table information to a file 

        Parameters
        ----------
        tab : Table
            Table information to write 
        filename : str 
            Name of file to write to 
        **kwargs : dict 
            Additional arguments 
        """
        tabfn = kwargs.pop('member','submission.yaml')
        if self._verbose:
            print('Write table {} into {}'
                  .format(tabfn, filename))
            
        with self._ensureZip(self,filename,'w') as z:
            super(ZipIO,self).dumpTable(tab,tabfn,**kwargs)
            
    def dump(self,sub,filename='submission.zip',**kwargs):
        """Write out all data to archive 

        Parameters
        ----------
        sub : Submission
            Submission to write out 
        filename : str 
            File to write main information to 
        **kwargs : dict 
            Additional arguments 
        """
        kwargs['table'] = kwargs.get('table',True)
        kwargs['meta']  = kwargs.get('meta',True)
        return self.dumpSubmission(sub,filename,**kwargs)

#
# EOF
#
        
