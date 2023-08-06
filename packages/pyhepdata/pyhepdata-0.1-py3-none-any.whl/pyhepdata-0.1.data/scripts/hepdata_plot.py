#!python 
"""Example to read in a submission and plot all tables in the submission 

Copyright 2019 Christian Holm Christensen
"""
import math
import re
import sys
sys.path.append('..')
sys.path.append('.')

import matplotlib.pyplot as plt
import hepdata as hd
import hepdata.io as hi
import hepdata.plot as hp
import hepdata.names as hn
from pprint import pprint

class All:
    """Open file, read in the submission, and plot all tables in the
    submission.
        
    Parameters
    ----------
    filename : str 
        File to read

    """
    def __init__(self,filename,names=None):
        self._sub = hi.load(filename,validator=True)
        if names is not None:
            #print(len(names))
            for n in names:
                hn.load(n)

    def plot(self,tables=None,location=True,beauty=True,calc_kw={},**kwargs):
        """Plot all tables in submission 
    
        Parameters
        ----------
        tables : list
            List of strings to match tables against, or None
        calc_kw : dict 
            Keyword arguments for uncertainty propagation 
        **kwargs : dict
            Additional arguments 
        """
        if 'calc' not in calc_kw:
            calc_kw = dict(calc=hd.Value.stack,
                           stack_calc=hd.Value.linvar)

        if beauty:
            kwargs['beautifier'] =  hn.Beautifier()

        if tables is not None:
            todraw = "(" + ")|(".join(tables)+")"
        else:
            todraw = '.*'

        #print(f'plot: Print options are {kwargs}')
        if not location:
            for i,m in enumerate(self._sub.metas()):
                if not re.match(todraw, m.name):
                    continue

                self._plotOne(m,i+1,calc_kw,**kwargs)

        else:
            for i,(t,m) in enumerate(self._sub.metas(True).items()):
                self._plotMany(m,i+1,t,todraw,calc_kw,**kwargs)
                

    def _checkScale(self,l,ax):
        for ll in l:
            ydat = ll.get_ydata()
            ymin = min(ydat)
            ymax = max(ydat)

            if ymin > 0 and math.log10(ymax) > math.log10(ymin)+2:
                ax.set_yscale('log')

            xdat = ll.get_xdata()
            xmin = min(xdat)
            xmax = max(xdat)

            if xmin > 0 and math.log10(xmax) > math.log10(xmin)+2:
                ax.set_xscale('log')

    def _figax(self,fig,ax,no,nind,ndep,same):
        if ax is not None:
            return fig, ax

        if nind == 1 and same:
            # Either one dependent, or all the same units.  Put on
            # same plot
            fig, ax = plt.subplots(ncols=1,num=no)
            return fig, [ax]

        if nind == 1:
            return plt.subplots(nrows=ndep,num=no, sharex=True,
                                gridspec_kw=dict(wspace=0,hspace=0))
            
        if nind == ndep:
            return plt.subplots(ncols=nind,num=no)
        
        # print('Got {} independent, and {} dependent variables'
        #       .format(nind,ndep))
        return None, None
        
    def _plotOne(self,meta,no,calc_kw={},**kwargs):
        #print(f'_plotOne: Print options are {kwargs}')
        fig, ax = self._plotMeta(meta,no,None,None,calc_kw,**kwargs)
        self._endPlot(fig,ax,meta.name)

    def _plotMany(self,metas,no,title,todraw,calc_kw={},**kwargs):
        fig = None
        ax  = None

        #print(f'_plotMany: Print options are {kwargs}')
        for m in metas:
            if not re.match(todraw, m.name):
                continue
            
            fig, ax = self._plotMeta(m,no,fig,ax,calc_kw,**kwargs)

        self._endPlot(fig,ax,title)

    def _endPlot(self,fig,ax,title):
        """Finalise the plot"""
        if ax is None:
            return
        
        for a in ax:
            h, l = a.get_legend_handles_labels()
            if h is not None and len(h) > 0:
                a.legend()

        fig.tight_layout()
        fig.suptitle(title)
        fig.show()

    def _plotMeta(self,meta,no,fig=None,ax=None,calc_kw={},**kwargs):
        """Plot a single table 
        
        Parameters
        ----------
        meta : Meta 
            Table meta information 
        no : int 
            Figure number 
        beauty : hepdata.plot.Beautifier 
            A beautifier 
        calc_kw : dict 
            Keyword arguments for uncertainty propagation 
        **kwargs : dict
            Additional arguments 
        """
        tab = meta.table()
        ind = tab._x
        dep = tab._y

        nind = len(ind)
        ndep = len(dep)
        same = len(set([d.units for d in dep])) == 1

        fig, ax = self._figax(fig, ax, no, nind, ndep, same)
        if fig is None or ax is None:
            return None, None

        #print(f'_plotMeta: Print options are: {kwargs}')
        if nind == 1:
            if same:
                # All the same units.  Put on same plot
                for d in dep:
                    la = hp.plotXY(ind[0],d,calc_kw=calc_kw,axes=ax[0],**kwargs)
                    self._checkScale(la,ax[0])

            else:
                for d, a in zip(dep,ax):
                    la = hp.plotXY(ind[0],d,calc_kw=calc_kw,axes=a,**kwargs)
                    self._checkScale(la,a)
                
        elif nind == ndep:
            for i, d, a in zip(ind,dep,ax):
                la = hp.plotXY(i,d,calc_kw=calc_kw,axes=a,**kwargs)
                self._checkScale(la,a)

        return fig, ax
        

if __name__ == "__main__":
    import argparse as ap
    import matplotlib.pyplot as plt

    p = ap.ArgumentParser(description='Plot data from file')
    p.add_argument('input',
                   help='Input filename',
                   type=ap.FileType('r'),
                   nargs='?',
                   default='data/1512299.zip')
    p.add_argument('-o','--options',type=str,nargs='+',
                   help='Options to pass on to plotter function, e.g., '
                   '-o fmt o type fill error_alpha .5')
    p.add_argument('-n','--names',type=ap.FileType('r'),nargs='+',
                   help='Additional file(s) to read names from')
    p.add_argument('-t','--tables',type=str,nargs='+',
                   help='Regular expression of table names to draw')
    p.add_argument('-l','--location',action='store_true',
                   help='If given, draw by location (if set)')
    p.add_argument('-p','--plain',action='store_false',
                   help='If set, do not use beautifier')
    args = p.parse_args()

    #print(f'__main__: Plot options are {args.options}')
    if args.options is not None:
        i = iter(args.options)
        # i is generator, so zip will pop pairs from the list (key,value)
        args.options = dict(zip(i,i))
    else:
        args.options = dict()
        
    plt.ion()

    #print(f'__main__: Plot options are {args.options}')
    a = All(args.input.name,args.names)
    a.plot(args.tables,args.location,args.plain,**args.options)


    import code
    code.interact(local=locals())

#
# EOF
#
