"""Module to import information from inspirehep.net

Copyright 2019 Christian Holm Christensen
"""

import json

# ====================================================================
class Search:
    """Class to search inspire for paper information. 

    This class uses journal information, such as 

    - Phys.Lett.,B772,567
    - Phys.Rev.,C83,044906 
    - Phys.Rev.Lett.,88,042001

    to query inspirehep.net for information.   

    Note, inSpire takes the journal letter as part of the volume
    number.  That is in 

      Physics Letters B 772 

    the journal name is "Phys.Lett." while the volume is "B772".

    Test case
    ---------
    - ``test_search.py``
    """
    def __init__(self):
        """Constructor"""
        # OLD
        # self._url = 'http://inspirehep.net/search?'
        # New
        self._url = 'https://inspirehep.net/api/literature?'

    def format(self,query):
        """Format the query

        Parameters
        ----------
        query : str 
            The journal reference.  Note format that inSpire expects. 

        Returns
        -------
        url : str 
            The URL for the query 
        """
        from urllib.parse import urlencode

        fields = ['publication_info',                    # OK
                  'preprint_date',                       # OK
                  'arxiv_eprints.value',                 # OK
                  'dois',                                # OK
                  'control_number', #'recid',            # OK 
                  'abstracts',                           # OK 
                  'external_system_identifiers',         # OK    
                  'collaborations',                      # OK
                  'license'] 		                 # OK

        if query.startswith('find '):
            query = query[5:]

        # OLD
        # opts = {'action_search':'Search',
        #         'rg':1,
        #         'of':'recjson',
        #         'ln':'en',
        #         'p':query,                
        #         'jrec':0,
        #         'ot':','.join(fields) }
        # NEW
        opts = {#'format': 'json',
                'size': 1, 
                'fields': ','.join(fields),
                'q':      query}

        
        return self._url + urlencode(opts)
                
    def query(self,q):
        """Query inSpire for information
        
        Parameters
        ----------
        query : str 
            The journal reference.  Note format that inSpire expects. 

        Returns
        -------
        result : dict 
            Dictionary of results 
        """
        from urllib.request import urlopen

        try:
            u = self.format(q)
            # print(f'URL of query: {u}')
            f = urlopen(u)
            d = f.read()
            j = json.loads(d.decode('utf-8'))
            if 'hits' not in j:
                raise RuntimeError('No hits!')
            if 'hits' not in j['hits']:
                raise RuntimeError('No hits in hits!')

            r = j['hits']['hits']
            return r
        except IOError as e:
            print(e)

        return None

#
# EOF
#
