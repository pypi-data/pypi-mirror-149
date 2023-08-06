"""Input/output from file system files

Copyright 2019 Christian Holm Christensen
"""
import tarfile
import os 
from . io import IO
from io import BytesIO
from .. submission import Submission
from .. resource import Resource

class TarIO(IO):
    """Class to read submission data from filesystem files

    Parameters
    ----------
    v : Validator 

        If not None, it must be a validator class for the schemas
        used.  If set, we will use this object to validate entries
        before or after output or input, respectively
    """
    def __init__(self,v,verbose=False,**kwargs):
        super(TarIO,self).__init__(v,verbose)
        if v:
            v._check_res = False
        self._ensureStream = None
        self._base = None
        
    class _ensureTar:
        """Context manager to open a zip file and tie _ensureStream to that
        zip file.
        """

        def __init__(self,moth,filename,mode):
            if moth._verbose:
                print('Opening tar file {} in mode {}'
                      .format(filename,mode))
            # Figure out the true mode
            if mode == 'w':
                _, ext = os.path.splitext(filename)
                comp = {
                    # gz
                    '.gz': 'gz',
                    '.tgz': 'gz',
                    # xz
                    '.xz': 'xz',
                    '.txz': 'xz',
                    # bz2
                    '.bz2': 'bz2',
                    '.tbz': 'bz2',
                    '.tbz2': 'bz2',
                    '.tb2': 'bz2',
                }
                mode = 'w:'+ comp[ext] if ext in comp else 'w'
            
            self._mother = moth
            self._tar    = tarfile.open(filename,mode)
            base         = os.path.splitext(os.path.basename(filename))[0]
            if base.endswith('.tar'):
                base     = os.path.splitext(os.path.basename(base))[0]
            self._mother._base = base
            self._mother._ensureStream = lambda filename, mode : \
                self._mother._ensureTStream(self._mother,self._tar,
                                            filename,mode)

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
            return self._tar

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
            self._tar.close()
            self._mother._ensureStream = None
            self._mother._base = None
            
    class _ensureTStream:
        def __init__(self,m,t,filename,mode):
            self._tar    = t
            self._mode   = mode
            fn = os.path.join(m._base,filename)
            self._stream = BytesIO() if mode == 'w' else t.extractfile(fn)
            if mode == 'w':
                setattr(self._stream,'name',fn)

        def __enter__(self):
            """Called upon context entry
        
            Returns
            -------
            s : stream 
                Our stream 
            """
            return self._stream

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
            if self._mode == 'r':
                return False
            
            self._stream.seek(0)
            tf = tarfile.TarInfo(self._stream.name)
            tf.size = len(self._stream.getvalue())
            self._tar.addfile(tf,self._stream)

            return False


    def _extRes(self,t,d,filename,ext):
        """Extract additional reources from zip archive"""
        l = d.get(Submission.ADDITIONAL_RESOURCES,None)
        if l is None:
            return

        for ll in l:
            loc = ll.get(Resource.LOCATION,'')
            if len(loc) <= 0 or loc.startswith('http'):
                continue

            src = os.path.join(self._base,loc)
            if src not in t.getnames():
                print('{} is not a member of {}'.format(src,filename))
                continue 

            if ext:
                tgt = os.path.dirname(filename)
                t.extract(src,tgt,set_attrs=False)

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
        with self._ensureTar(self,filename,'r') as t:
            sub = self._loadAll(subfn,**kwargs)

            self._extRes(t,sub._d,filename,ext)
            for m in sub._t.values():
                self._extRes(t,m._d,filename,ext)
        return sub
            

    def _addRes(self,t,d,filename):
        """Add additional resources to zip archive"""
        l = d.get(Submission.ADDITIONAL_RESOURCES,None)
        if l is None:
            return

        for ll in l:
            loc = ll.get(Resource.LOCATION,'')
            if len(loc) <= 0 or loc.startswith('http'):
                continue

            tgt = os.path.join(self._base,loc)
            src = os.path.join(os.path.dirname(filename),loc)
            if os.path.isfile(src):
                t.add(src,tgt,recursive=False)
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
        with self._ensureTar(self,filename,'w') as t:
            super(TarIO,self).dumpSubmission(sub,subfn,**kwargs)

            self._addRes(t,sub._d,filename)
            if meta: 
                for m in sub._t.values():
                    self._addRes(t,m._d,filename)
            
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
            
        with self._ensureTar(self,filename,'w') as t:
            super(TarIO,self).dumpMeta(mta,mtafn,**kwargs)
            self._addRes(t,mta._d,filename)
            
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
            
        with self._ensureTar(self,filename,'w') as t:
            super(TarIO,self).dumpTable(tab,tabfn,**kwargs)
            
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
        
