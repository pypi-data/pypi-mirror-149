"""Module for plotting HEPData using matplotlib

Copyright 2018 Christian Holm Christensen
"""
from . beautifier import Beautifier 
from . plotter import Plotter

#: Alias for :meth:`Plotter.plotXY`
def plotXY(*args,**kwargs):
    """An 'alias' for :meth:`Plotter.plotXY`.  

    This internally creates a Plotter object.  The beautifier can be
    set through the keyword argument ``beautifier``
    
    Parameters
    ---------- 
    See :meth:`Plotter.plotXY`

    Returns
    -------
    See :meth:`Plotter.plotXY`

    """
    beaut = kwargs.pop('beautifier',Beautifier())

    plotter = Plotter(beaut)
    return plotter.plotXY(*args,**kwargs)


#
# EOF
#
