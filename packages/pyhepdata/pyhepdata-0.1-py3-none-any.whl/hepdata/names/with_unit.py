"""Base class for entries with units

Copyright 2019 Christian Holm Christensen
"""
from . unit import Unit

class WithUnit:
    @classmethod
    def parse_unit(cls,units):
        if units is None:
            return None
        
        if type(units) is dict:
            assert len(units) == 1, \
                'Cannot give multiple units for variable'
                
            for k,v in units.items():
                Unit.register(k,v,v)
                unit = getattr(Unit,k)
                units = unit

        elif units.startswith('Unit.'):
            units = units.replace('Unit.','')
            try:
                units = getattr(Unit,units)
            except:
                raise ValueError('Unit {} not known'.format(units))

        return units

#
# EOF
#
