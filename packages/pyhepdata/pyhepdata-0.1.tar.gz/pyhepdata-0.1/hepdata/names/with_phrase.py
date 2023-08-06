"""Base class for database entries that has associated phrases

Copyright 2019 Christian Holm Christensen
"""
from . phrase import Phrase
from .. utils import _ensureList

class WithPhrase:
    @classmethod
    def parse_phrases(cls,phrase):
        pl = _ensureList(phrase)
        pv = []
        if pl is None:
            return None
        
        for p in pl:
            if type(p) is dict:
                # If a dictionary, try to register new phrases
                for k,v in p.items():
                    Phrase.register(k,v)
                    pv.append(getattr(Phrase,k))
            elif p.startswith('Phrase.'):
                p = p.replace('Phrase.','')
                try:
                    pv.append(getattr(Phrase,p))
                except:
                    raise ValueError('Phrase {} not known'.format(p))
            else:
                pv.append(p)

        return pv
#
# EOF
#
