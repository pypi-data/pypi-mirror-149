"""Plotter module for HEPData

Copyright 2018 Christian Holm Christensen
"""
import matplotlib.pyplot as plt
import matplotlib.markers as markers
import math
from . beautifier import Beautifier
from .. dependent import Dependent
from .. value import Value
from .. utils import _ensureList
    
class Plotter:

    """A class to plot data from HEPData 

    Currently only supports 1D (xy) plots 
    
    Parameters
    ----------
    b : object 
        A beautifier to use when formatting variables, observables,
        units, qualifiers
    """
    def __init__(self,beautifier=Beautifier()):
        self._b = beautifier
        if self._b is None:
            self._b = Beautifier()

    @classmethod
    def _sysqual(cls,q):
        """Select qualifiers that start with the string 'sys:' 

        If a qualifier name starts with 'sys:' and that qualifier has
        a value, we return a new dict with the name and value in.
        """
        n = q.get(Dependent.NAME,None)
        v = q.get(Dependent.VALUE,None)
        u = q.get(Dependent.UNITS,None)
        if n is None or v is None:
            return None

        if n.startswith('sys:'):
            return q;
        
        return None

    def _plot(self,x,y,ex,ey,eh,axes,*,
              params=None,
              col=None,
              alp=None,
              fmt=None,
              lbl=None,
              **kwargs):
        """Loop over all defined uncertainties and plot them 
        
        Parameters
        ----------
        x : list 
            X (abscissa) values.
        y : list
            Y (ordinate) values.
        ex : list 
            X (abscissa) uncertainties.
        ey : list
            Y (ordinate) uncertainties.
        eh : list 
            Uncertainty headers.
        params : list 
            Keyword arguments per uncertainty.  See :meth:`Plotter.plot`.
        col : None or color 
            Color to use if not otherwise set. 
        alp : float or None 
            Alpha (opacity) level to use if not otherwise set.
        **kwargs : dict 
            Keyword arguments. .  See :meth:`Plotter.plot`.
        
        Returns
        -------
        c : color 
            Last color used 
        """
        # Ensure that params is a list and have as many entries as we
        # have uncertainties.
        params = self._ensureParams(params,len(ey))
        
        c = col
        for ee,pp,hh in zip(ey[::-1],params[::-1],eh[::-1]):
            # Calculate union of parameter and common keywords
            myc   = 'color' in pp
            rargs = dict(kwargs, **pp)
            
            if c is not None and 'color' not in rargs:
                rargs['color'] = c

            # Whether to add labels to uncertainties
            if  rargs.pop('labelled',False):
                if 'label' not in rargs:
                    rargs['label'] = self._b.uncertainty(hh,lbl)
            else:
                rargs['label'] = None
        

            # Alpha 
            if alp is not None and 'alpha' not in rargs:
                rargs['alpha'] = float(alp)
                
            # Get type of error bars 
            t = rargs.get('type','errorbar')

            # Note, we always get lower and upper limits on each point
            # in `ee`, and a negative lower limit corresponds to a
            # lower bound being smaller than the point.  However, the
            # matplotlib.pyplot routines expect a _positive_ lower
            # limit to correspond to a bound smaller than the value.
            # Thus, we massage the errors here.
            try:
                if isinstance(ee,tuple):
                    eee = (-ee[0],ee[1])
                else:
                    eee = [(-te[0],te[1]) for te in ee]
            except:
                eee = [(-ee,ee)]
            
            # print("{:10s} {:20s} {}".format(t,hh,c))
            if t == 'fill':
                newc = self._fill(x,y,ex,eee,axes=axes, **rargs)
            elif t == 'marker':
                newc = self._markerLines(x,y,ex,eee,True,axes=axes, **rargs)
            elif t == 'line':
                newc = self._markerLines(x,y,ex,eee,False,axes=axes, **rargs)
            else:
                if fmt is not None:
                    rargs['fmt'] = fmt
                newc = self._bars(x,y,ex,eee,axes=axes, **rargs)

            if not myc:
                c = newc

        return c

    def _ensureParams(self,params,ne):
        """Ensure that params is a list and have as many entries as we
        have uncertainties.  

        If we're missing entries, we repeate the last entry as many
        times as needed

        Parameters
        ----------
        params : None, dict, list of dict 
            Parameters 
        ne : int 
            Number or parameter sets we need 

        Return
        ------
        params : list 
            Padded list of parameters 
        """
        if params is None:
            params = [{}] * ne
        elif type(params) not in [list,tuple]:
            params = [params]
            
        if len(params) < ne:
            params += params[-1:] * (ne-len(params))

        return params

    def emptyParams(self,y,calc_kw={}):
        """Returns a dictionary of empty (safe for 'label') corresponding to
        the uncertainties on the dependent variable _y_ using the
        uncertainty calculation in _calc_kw_.

        See also :meth:`Dependent.e` for more on _calc_kw_. 

        Parameters
        ----------
        y : Dependent 
            Dependent variable (ordinate) column 
        calc_kw : dict 
            Keywords to pass to :meth:`Dependent.e` (see that method
            for more information)

        Returns
        -------
        p : dict
            A dictionary with entries for each uncertainty column,
            where the key is the label of the uncertainty.  If an
            uncertainty does not define a label, or the label is
            ambigius, we label the uncertainty by the index of the
            uncertainty (appended to label in case of ambigious
            labels).

            >>> params = \
            ...    plotter.emptyParams(y,calc_kw=dict(calc=Value.stack,\
            ...                                       stack_calc=Value.sumsq))
        
            The user can subseqnety fill in values on each dictonary
            element to set options 

            >>> params['stat']['type'] = 'bar'
            >>> params['sys']['type'] = 'bar'
            >>> params['sys']['elinewidth'] = 0
            >>> params['sys']['ecapsize'] = 10

            The parameters can be passed to the :meth:`Plotter.plotXY`
            method by getting the values as a list

            >>> plotter.plotXY(x,y,params=list(params.values()),...)

        """
        col_kw = {'columns':True,
                  'alwaystuple':True,
                  'header':True}
        col_kw = dict(calc_kw, **col_kw)
        import collections
        # Get Y values, errors, and header
        _, [_,*eh] = y.ye(**col_kw)
        ret = collections.OrderedDict()
        for n in eh:
            ret[n] = {'label':n }
        return ret

    def emptyCommonParams(self,y,select=None):
        """Returns a dictionary of empty (safe for 'label') corresponding to
        the common uncertainties on the dependent variable _y_ using
        the uncertainty selection criteria _select_

        See also :meth:`Dependent.qualifiers` for more on _select_. 

        Parameters
        ----------
        y : Dependent 
            Dependent variable (ordinate) column 
        select : str,list,callable
            Selector of qualifiers, see :meth:`Dependent.qualifers`

        Returns
        -------
        p : dict
            A dictionary with entries for each common uncertainty,
            where the key is the label of the uncertainty.  

            >>> params = plotter.emptyCommonParams(y)
        
            The user can subseqnety fill in values on each dictonary
            element to set options 

            >>> params['Centrality'].update(dirct(type='bar'))
            >>> params['Bla'].update(dict(type='fill',label='Whatever'))

            The parameters can be passed to the :meth:`Plotter.plotXY`
            method by getting the values as a list

            >>> plotter.plotXY(x,y,
            ...           common_kw=dict(params=list(params.values()),...),...)

        """
        import collections
        # Get Y values, errors, and header
        if select is None:
            select = Plotter._sysqual            
        cml = y.qualifiers(select)
        ret = collections.OrderedDict()
        for e in cml:
            ret[e[Dependent.NAME][4:]] = { 'label':e[Dependent.NAME] }
        return ret
    
    def plotXY(self,x,y,*,params=None,calc_kw={},common_kw={},**kwargs):

        """Plot dependent variable `y` (including uncertainties) versus
        independent variable `x` (possibly binned).

        Parameters
        ----------
        x : Independent
            Column of independent data 
        y : Dependent 
            Column of dependent data 
        params : list
            A list (or scalar) of the information on how to draw the
            errors bars.  Each element is a dictionary of the type of
            errorbar to draw and additional keyword arguments to the
            relevant function.

            To customize each uncertainty plot, one can give as many
            elements as there are uncertainties on the dependent
            values.  

            One can also give less, in which case the parameters of
            the last uncertainty will be reused for the remainding
            plots.

            The dictionary can contain keywords in addition to the
            keyword arguments used by the plotting functions
            (matplotlib.pyplot.fill_between and
            matplotlib.pyplot.errorbar).  These are 

            - type : str
                "fill" for ``matplotlib.pyplot.fill_between`` and 
                "bar" for ``matplotlib.pyplot.errorbar`` 
            - labelled : bool If true, label the plot (i.e., so that
                it will show up in a legend.  If this is true, and the
                dictionary specifies a ``label``, then that value is
                used.  Otherwise we take the label value from the
                declared label of the data uncertainty

        calc_kw : dict 
            Keywords to pass to :meth:`Dependent.e` (see that method
            for more information)
        common_kw : dict 
            Keywords for plotting common uncertainties 
        **kwargs : dict 

            - axes : matplotlib.pyplot.Axes (optional)
                Axes object to draw into 
            - calc : callable 
                Callable to calculate uncertainties on the dependent
                variable.  See also :meth:`hepdata.Value.e`

        Returns
        -------
            Hmm

        """
        axes = kwargs.pop('axes',       kwargs.pop('ax',plt.gca()))
        hdr  = kwargs.pop('header',     False)
        fmt  = kwargs.pop('fmt',        None)
        alp  = kwargs.pop('error_alpha',None)
        lbl  = kwargs.pop('label',      None)
        qls  = kwargs.pop('qualifiers', None)
        cmn  = kwargs.pop('common',     True)
        
        # Set label on data if not set already 
        if lbl is None and qls is not None:
            if qls == 'obs':
                lbl = self._b.observable(y.name)
            elif qls == 'var':
                lbl = self._b.variable(x.name)
            else:
                if qls == '*' or qls == 'all':
                    qls = None
                lbl = self._b.qualifiers(y.qualifiers(qls))

        if not lbl is None:
            lbl = lbl.replace(r'\text',r'\mathrm')
        # print(f'Label is {lbl}')
        
        # Get list of common uncertainties
        cml = []
        if cmn:
            cml = y.qualifiers(Plotter._sysqual)
            
        col_kw = {'columns':    True,  # Sort by columns
                  'alwaystuple':True,  # Both low and high 
                  'header':     True}
        col_kw = dict(calc_kw, **col_kw)


        # Get X values, errors, and header
        [vx,ex], (nx,ux)   = x.xe(**col_kw)
        [vy,*ey], [(ny,uy),*eh] = y.ye(**col_kw)
        c = self._plot(vx,vy,ex,ey,eh,
                       axes=axes,col=None,alp=alp,fmt=fmt,lbl=lbl,
                       params=params,**kwargs)

        # Plot common uncertainties
        cpars = common_kw.pop('params',None)
        cargs = dict(kwargs, **common_kw)
        c = self._plotCommon2(vx,vy,y,axes=axes,col=c,alp=alp,
                              lbl=lbl,calc_kw=calc_kw,params=cpars,
                              **cargs)
            
        # Insert color if not defined 
        if c is not None:
            if 'color' not in kwargs:
                kwargs['color'] = c
            
        # Remove type 
        kwargs.pop('type',None)
        kwargs.pop('labelled',None)
        
        # Set label on data if not set already 
        if lbl is not None:
            kwargs['label'] = lbl

        # Plot data points last
        if fmt is not None:
            args = (vx,vy,fmt)
        else:
            args = (vx,vy)

        ret = axes.plot(*args,**kwargs)
        axes.set_xlabel(self._b.variable(nx,ux))
        axes.set_ylabel(self._b.observable(ny,uy))
        
        return ret

    def _fill(self,vx,vy,ex,ey,axes,**kwargs):
        """Draw error as filled area

        Parameters
        ----------
        xx : list of float
            Independent variable values 
        yy : list of float 
            Dependent variable values 
        ee : list of (float,float)
            Uncertainty on dependent variable values 
        axes : matplotlib.pyplot.Axes 
            Where to draw 
        **kwargs : dict 
            Arguments passed to ``matplotlib.pyplot.fill_between` 
        
        Returns
        -------
            Hmm 
        """
        for c in ['type','fmt','markersize','markerfacecolor','markeredgecolor']:
            kwargs.pop(c,None)
        if type(vx) is float and type(vy) is float:
            vx = [vx-ex,vx+ex]
            vy = [vy,   vy]
            if type(ey) is float:
                ey = [ey, ey]
            ey = [ey,   ey]

        bound = list(map(tuple,zip(*map(lambda a: (a[0]-a[1][0],
                                                   a[0]+a[1][1]),
                                        zip(vy,ey)))))
        pc = axes.fill_between(vx,bound[0],bound[1],**kwargs)
        # PC is a poly-collection
        return pc.get_facecolor()[0][:3]                                     
        

    def _bars(self,xx,yy,ex,ey,axes,**kwargs):
        """Plot uncertainty as bars

        Parameters
        ----------
        xx : list of float
            Independent variable values 
        yy : list of float 
            Dependent variable values 
        ex : list of (float,float)
            Uncertainty on independent variable values 
        ey : list of (float,float)
            Uncertainty on dependent variable values 
        axes : matplotlib.pyplot.Axes 
            Where to draw 
        **kwargs : dict 
            Arguments passed to ``matplotlib.pyplot.fill_between` 
        
        Returns
        -------
            Hmm 
        """
        kwargs.pop('type',None)
        nox = kwargs.pop('nox',False)
        
        if type(ex) is not float:
            ex = list(map(tuple,zip(*ex)))
            if all([math.fabs(e)<1e-9 for e in ex[0]+ex[1]]):
                nox = True
        elif math.fabs(ex) < 1e-9:
            nox=True
            
        if type(ey) not in [float,tuple]:
            ey = list(map(tuple,zip(*ey)))
        elif type(ey) is tuple:
            ey = [[ey[0]],[ey[1]]]

        if nox:
            ex = None

        ebc = axes.errorbar(xx,yy,ey,ex,**kwargs)
        return ebc[2][0].get_color()[0][:3]

    def _markerLines(self,xx,yy,ex,ey,marker,axes,**kwargs):
        """Plot uncertainty using markers 

        Parameters
        ----------
        xx : list of float
            Independent variable values 
        yy : list of float 
            Dependent variable values 
        ex : list of (float,float)
            Uncertainty on independent variable values 
        ey : list of (float,float)
            Uncertainty on dependent variable values 
        marker : bool 
            If true, draw markers, otherwise lines 
        axes : matplotlib.pyplot.Axes 
            Where to draw 
        **kwargs : dict 
            - leftmarker : matplotlib.markers
                Marker to put on the left (e.g.,
                matplotlib.markers.CARETLEFT).  If not specified
                (i.e., None, '', or 'none') then horizontal
                uncertainties are not drawn
            - rightmarker : matplotlib.markers
                Marker to put on the right (e.g.,
                matplotlib.markers.CARETRIGHT).  If not specified
                (i.e., None, '', or 'none') then horizontal
                uncertainties are not drawn
            - upmarker : matplotlib.markers
                Marker to upward (e.g.,
                matplotlib.markers.CARETUP).  If not specified
                (i.e., None, '', or 'none') then vertical
                uncertainties are not drawn
            - downmarker : matplotlib.markers
                Marker to put downward (e.g.,
                matplotlib.markers.CARETDOWN).  If not specified
                (i.e., None, '', or 'none') then vertical
                uncertainties are not drawn

            Arguments passed to ``matplotlib.pyplot.fill_between` 
        
        Returns
        -------
            Hmm

        """
        kwargs.pop('type',None)
        nox   = kwargs.pop('nox',False)
        lmark = None
        rmark = None
        umark = None
        dmark = None
        if marker:
            lmark = kwargs.pop('leftmarker', None)
            rmark = kwargs.pop('rightmarker',None)
            umark = kwargs.pop('upmarker',   markers.CARETUP)
            dmark = kwargs.pop('upmarker',   markers.CARETDOWN)
        
        if lmark is None or str(lmark).lower() in ['','none']:
            nox = True
        if rmark is None or str(rmark).lower() in ['','none']:
            nox = True

        if type(ex) is not float:
            ex = list(map(tuple,zip(*ex)))
            if all([math.fabs(e)<1e-9 for e in ex[0]+ex[1]]):
                nox = True
        elif math.fabs(ex) < 1e-9:
            nox=True
            
        if type(ey) not in [float,tuple]:
            ey = list(map(tuple,zip(*ey)))
        elif type(ey) is tuple:
            ey = [[ey[0]],[ey[1]]]


        def _getColor(l,marker):
            if l is None:
                return None

            if marker:
                c = l[0].get_markeredgecolor()
            c = l[0].get_color()
            return c
        
        def _setColor(l,marker,kwargs):
            if l is None:
                return kwargs

            if 'color' not in kwargs:
                kwargs['color'] = _getColor(l,marker)

            return kwargs
        
        lbl = kwargs.pop('label',None)
        fmt = '.' if marker else '-'
        l   = None
        if not nox:
            l = axes.plot([x-e for x,e in zip(xx,ex[0])],yy,fmt,
                          marker=lmark,**kwargs)
            kwargs = _setColor(l,marker,kwargs)
            l = axes.plot([x+e for x,e in zip(xx,ex[1])],yy,fmt,
                          marker=rmark,**kwargs)

        kwargs = _setColor(l,marker,kwargs)
        l = axes.plot(xx,[y-e for y,e in zip(yy,ey[0])],fmt,marker=dmark,
                      **kwargs)

        if lbl is not None:
            kwargs['label'] = lbl
            
        kwargs = _setColor(l,marker,kwargs)
        l = axes.plot(xx,[y+e for y,e in zip(yy,ey[1])],fmt,marker=umark,
                      **kwargs)

        return _getColor(l,marker)

    def _loc2val(self,loc,vs,d=0):
        if type(loc) in [float,int]:
            return loc
        
        if type(loc) is str:
            if loc == 'left' or loc == 'min' or loc == 'bottom':
                return min(vs)-d
            if loc == 'right' or loc == 'max' or loc == 'top':
                return max(vs)+d
            if loc == 'center' or loc == 'middle':
                return (max(vs) - min(vs)) / 2
            else:
                return float(loc)

        raise ValueError('location={} unknown'.format(loc))

    def _plotCommon2(self,vx,vy,y,axes,col=None,alp=1,lbl=None,calc_kw={},
                     params=None,**kwargs):
        """Plot common uncertainties 
        
        Parameters
        ----------
        vx : list 
            X values 
        vy : list 
            Y values 
        y : Dependent 
            Depenendent column 
        axes : matplotlib.axes.Axes 
            Axes to plot in 
        col : color 
            Color of plot 
        alp : float or None 
            Alpha (opacity) level to use if not otherwise set.
        lbl : string 
            Label 
        calc_kw : dict 
            Dictionary of calculation keywords 
        params : list 
            Keyword arguments per uncertainty.  See :meth:`Plotter.plot`.
        kwargs : dict 
            Additional keyword arguments to pass to plotting 

            loc : 2-tuple 
                X,Y coordinates to put common error bar at.  If not 
                specified, take 
        
                    yloc = max(y)
                    xloc = max(x) + 2 * width 

            width : float 
                Width of common error bar 

                    width = max(delta x)

            
        
        Returns
        -------
        Hmmm
        """
        try:
            if len(vx) <= 1:
                return None
        except:
            return None
        
        fmt  = kwargs.pop('fmt',None)
        d    = kwargs.pop('width',max([xh-xl for xh,xl in zip(vx[1:],vx[:-1])]))
        loc  = kwargs.pop('loc',None)
        if loc is not None:
            kwargs['xloc'] = loc[0]
            kwargs['yloc'] = loc[1]
        xloc = self._loc2val(kwargs.pop('xloc',max(vx)+2*d),vx,2*d)
        yloc = self._loc2val(kwargs.pop('yloc',max(vy)),vy)

        calck = dict(**calc_kw)
        calc  = calck.pop('calc',Value.asis)
        cml   = y.ce(calc=calc,**calck)

        if cml is None: return None

        errs, dy, lbls =  cml
        yloc           += dy

        return self._plot(xloc,yloc,d,errs,lbls,axes,col=col,alp=alp,
                          lbl=lbl, params=params, **kwargs)
        
    def _plotCommon(self,x,y,cml,axes,col=None,alp=1,lbl=None,calc_kw={},
                    params=None,**kwargs):
        """Plot common uncertainties 
        
        Parameters
        ----------
        cml : list of dict 
            List of common systematic uncertainties 
        calc_kw : dict 
            Keywords to pass to :meth:`Dependent.e` (see that method
            for more information)
        **kwargs:
            Keywords for plotting common systematic uncertainties 
        
        Returns
        -------
        Hmm
        """
        if cml is None or len(cml) <= 0:
            return col
        

        fmt  = kwargs.pop('fmt',None)
        d    = kwargs.pop('width',max([xh-xl for xh,xl in zip(x[1:],x[:-1])]))
        loc  = kwargs.pop('loc',None)
        if loc is not None:
            kwargs['xloc'] = loc[0]
            kwargs['yloc'] = loc[1]
        xloc = self._loc2val(kwargs.pop('xloc',max(x)+2*d),x,2*d)
        yloc = self._loc2val(kwargs.pop('yloc',max(y)),y)
        vals = [c[Dependent.VALUE] * (yloc/100
                                      if c.get(Dependent.UNITS,'')
                                      in ['PCT','%']
                                      else 1) for c in cml]
        pais = [{Value.ASYMERROR: {Value.MINUS: v, Value.PLUS: v}}
                for v in vals]
        lbls = [c[Dependent.NAME][4:] for c in cml]
        
        calck   = dict(**calc_kw)
        calc    = calck.pop('calc',Value.asis)
        errs,dy = calc(pais,yloc,**calc_kw)
        yloc    += dy

        return self._plot(xloc,yloc,d,errs,lbls,axes,col=col,alp=alp,
                          lbl=lbl, params=params, **kwargs)

#
# EOF
#

                
