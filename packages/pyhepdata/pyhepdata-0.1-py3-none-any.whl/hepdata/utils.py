"""Various utilities 

Copyright 2019 Christian Holm Christensen
"""
# ====================================================================
def _ensureList(v):
    """Utility to ensure a list"""
    if v is None:
        return None

    if type(v) in [list,tuple]:
        return v

    return [v]

#
# EOF
#
