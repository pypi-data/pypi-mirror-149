"""Input/output from file system files

Copyright 2019 Christian Holm Christensen
"""
import os 
from .. meta import Meta
from . io import IO

class FileIO(IO):
    """Class to read submission data from filesystem files

    Parameters
    ----------
    v : Validator 
        If not None, it must be a validator class for the schemas
        used.  If set, we will use this object to validate entries
        before or after output or input, respectively
    """
    def __init__(self,v=None,verbose=False,**kwargs):
        super(FileIO,self).__init__(v,verbose)
        self._ensureStream = None
        
    class _ensureTop:
        """Context manager to ensure top-level file is kept 
        """
        def __init__(self,moth,filename):
            assert moth._ensureStream is None,\
                "Ensure top has already been called in this context!"
            self._mother = moth
            self._top    = filename
            self._mother._ensureStream = lambda filename, mode : \
                self._mother._ensureDStream(self._top,filename,mode)
            if self._mother._verbose:
                print('Top is set to {}'.format(self._top))

        def __enter__(self):
            """Called upon context entry
        
            Returns
            -------
            s : stream 
                Our stream 
            """
            return os.path.basename(self._top)

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
            self._mother._ensureStream = None

    def _ensureDStream(self,top,filename,mode):
        """Ensure we have a stream opened in the right directory"""
        real = os.path.join(os.path.dirname(top),filename)
        if self._verbose:
            print('Opening stream {} in mode {}'.format(real,mode))
        return open(real,mode)

    def load(self,filename='submission.yaml',**kwargs):
        """Load evertying from given file"""
        with self._ensureTop(self,filename) as fn:
            return self._loadAll(fn,**kwargs)

    def dump(self,sub,filename='submission.yaml',**kwargs):
        """Dump everything to given file"""
        kwargs['table'] = kwargs.get('table',True)
        kwargs['meta']  = kwargs.get('meta',True)
        return self.dumpSubmission(sub,filename,**kwargs)

    def dumpSubmission(self,sub,filename='submission.yaml',**kwargs):
        """Dump submission information to file 
        
        Parameters
        ----------
        mta : Submission 
            Submission information to write out
        filename : str 
            File to write to
        **kwargs : dict 
            Additional arguments 
        """
        with self._ensureTop(self,filename) as fn:
            super(FileIO,self).dumpSubmission(sub,fn,**kwargs)
       
    def dumpMeta(self,mta,filename='submission.yaml',**kwargs):
        """Dump meta information to file 
        
        Parameters
        ----------
        mta : Meta 
            Meta information to write out
        filename : str 
            File to write to
        **kwargs : dict 
            Additional arguments 
        """
        with self._ensureTop(self,filename) as fn:
            super(FileIO,self).dumpMeta(mta,fn,**kwargs)

    def dumpTable(self,tab,filename='table.yaml',**kwargs):
        """Dump table information to file 
        
        Parameters
        ----------
        mta : Table 
            Table information to write out
        filename : str 
            File to write to
        **kwargs : dict 
            Additional arguments 
        """
        with self._ensureTop(self,filename) as fn:
            super(FileIO,self).dumpTable(tab,fn,**kwargs)
#
# EOF
#
        
