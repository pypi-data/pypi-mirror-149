"""Package for Input/Output of data in this project

Copyright 2019 Christian Holm Christensen
"""
import os
from . fileio import FileIO
from . zipio import ZipIO
from . tario import TarIO
from . validator import Validator 
from .. submission import Submission
from .. meta import Meta
from .. table import Table

def _getio(filename,archive):
    arctype = {'zip': ZipIO,
               'tar': TarIO }
    if archive in arctype:
        return arctype[archive]

    _, ext = os.path.splitext(filename)
    
    tarext = ['.gz','.tgz',
              '.xz','.txz',
              '.bz2','.tbz','.tbz2','.tb2' ]
    if ext in tarext:
        return TarIO

    if ext in ['.zip', '.ZIP', '.Zip']:
        return ZipIO

    return FileIO
    
def dump(obj,filename,*,archive=False,validator=True,**kwargs):
    """Dump object `obj` (a Submission, Meta, or Table) to file `filename`. 
    
    If `filename` ends in ``.zip`` or the keyword argument ``archive`` is
    true, then write to a zip-archive. 

    Parameters
    ----------
    obj : object 
        The object to write 
    filename : str 
        The file to write to 
    archive : bool 
        Whether to write to a zip archive or not 
    validator : bool or Validator 
        Validator to use (or use validator if true)
    **kwargs : dict 
        Additional arguments 

        meta : bool 
            If false, do not write meta information or tables 
        table : bool 
            If false, do not write tables 
        member : str (zip-file only)
            Member to extract (e.g., ``submission.yaml``)
        resources : bool (zip-file only)
            If true, extract resources from zip file 
        archive : bool 
            Force zip archive, even if file name does not end on ``.zip``
        schemadir : str 
            Directory to load YAML schemas from 
        verbose : bool 
            Whether to be verbose 
        compat : bool 
            If true, operate in compatbility mode 
            (allow one-file submission, and associated_records)

    Returns
    -------
    Hmm 
    """
    v = validator
    verb = kwargs.pop('verbose',False)
    schdir = kwargs.pop('schemadir',None)
    compat = kwargs.pop('compat',False)
    if type(v) is bool:
        v = Validator(schdir,compat,verb) if v else None
    
    iocls = _getio(filename, kwargs.pop('archive',False))
    io    = iocls(v,verb)
    
    if type(obj) is Submission:
        kwargs['meta']  = kwargs.get('meta',True)
        kwargs['table'] = kwargs.get('table',True)
        return io.dumpSubmission(obj,filename,**kwargs)
    if type(obj) is Meta:
        kwargs['table'] = kwargs.get('table',True)
        return io.dumpMeta(obj,filename,**kwargs)
    if type(obj) is Table:
        return io.dumpTable(obj,filename,**kwargs)
    
    return None

def load(filename,*,archive=False,validator=True,**kwargs):
    """Load object(s) (a Submission, Meta, or Table) from file `filename`. 
    
    If `filename` ends in ``.zip`` or the keyword argument `'archive`` is
    true, then read from a zip-archive. 

    Parameters
    ----------
    obj : object 
        The object to write 
    filename : str 
        The file to write to 
    archive : bool 
        Whether to write to a zip archive or not 
    validator : bool or Validator 
        Validator to use (or use validator if true)
    **kwargs : dict 
        Additional arguments 

        meta : bool 
            If false, do not write meta information or tables 
        table : bool 
            If false, do not write tables 
        member : str (zip-file only)
            Member to extract (e.g., ``submission.yaml``)
        archive : bool 
            Force zip archive, even if file name does not end on ``.zip``
        schemadir : str 
            Directory to load YAML schemas from 
        verbose : bool 
            Whether to be verbose 
        compat : bool 
            If true, operate in compatbility mode 
            (allow one-file submission, and associated_records)

    Returns
    -------
    obj : Submission, Meta, or Table 
        Object read 
    """
    v = validator
    verb = kwargs.pop('verbose',False)
    schdir = kwargs.pop('schemadir',None)
    compat = kwargs.pop('compat',False)
    if type(v) is bool:
        v = Validator(schdir,compat,verb) if v else None

    iocls = _getio(filename, kwargs.pop('archive',False))
    io    = iocls(v,verb)

    return io.load(filename,**kwargs)

def load_from_web(iden,version=1,**kwargs):
    '''Loads a submission directly from hepdata.net if not 
    already downloaded 

    Parameters
    ----------
    ident : string 
        Submission identifier 
    version : int (optional) 
        Optional version of the submission (Defaults to 1)
    
    Returns
    -------
    submission : Submission 
        The retrieved submission or None 
    '''
    from pathlib import Path
    tgt = Path(f'HEPData-{iden}-v{version}-yaml.tar.gz')

    if not tgt.exists():
        from urllib.request import urlopen
        url = f'https://www.hepdata.net/download/submission/{iden}/{version}/yaml'
        
        with urlopen(url) as response:
            with open(tgt,'wb') as out:
                out.write(response.read())

        if not tgt.exists():
            raise 'Failed to download submission {iden} version {version} from␣{url}'

    return load(tgt,**kwargs)

 # # EOF #
