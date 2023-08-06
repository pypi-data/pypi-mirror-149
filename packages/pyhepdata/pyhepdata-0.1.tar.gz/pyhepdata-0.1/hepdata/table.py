"""A single data table of columns of independent and dependent values 

Copyright 2019 Christian Holm Christensen
"""
from . accepts import accepts
from . dependent import Dependent
from . independent import Independent

class Table:
    """A table of data
    
    A container of columns - separately for `independent` and
    `dependent` variables.

    Independent variables (see :class:`hepdata.Independent`) are what
    we normally put on the abscissa - the quantity by which we
    categorise our measurement.  Independent variables are typically
    `binned` or can be single values (with no uncertainties).

    Dependent variables (see :class:`hepdata.Dependent`) are what we
    typically put on the ordinate - the quantity which we have
    measured.  Dependent variables take on multiple values, one for
    each bin or value of the independent variable, and have associated
    uncertainties (statistical, systematic).  One can associate as
    many uncertainties as needed, keeping in mind the significance of
    each.

    The data-extraction (see :meth:`hepdata.Dependent.ye`) and
    plotting subsystem (:mod:`hepdata.plot`) can propagate
    uncertainties correctly, including asymmetric uncertainties (see
    :mod:`hepdata.combiner`).

    Parameters
    ----------
    name : str (optional)
        Reference to meta data

    """
    #: Header field name
    HEADER = 'header'
    #: Independent_Variables field name
    INDEPENDENT_VARIABLES = 'independent_variables'
    #: Dependent_Variables field name
    DEPENDENT_VARIABLES = 'dependent_variables'
    #: Name field name
    NAME = 'name'
    #: Units field name
    UNITS = 'units'
    #: Values field name
    VALUES = 'values'
    #: Value field name
    VALUE = 'value'
    #: Low field name
    LOW = 'low'
    #: High field name
    HIGH = 'high'

    @accepts(name=str)
    def __init__(self,name=None):
        self._x = []
        self._y = []
        self._d = {
            self.INDEPENDENT_VARIABLES: [],
                #{ self.HEADER: {self.NAME: var },
                #  self.VALUES: self._x } ], 
            self.DEPENDENT_VARIABLES: [] }
        if name is not None:
            self._d[self.NAME] = name

    @accepts(name=str,unit=str)
    def dependent(self,name,unit=None):
        """Add a dependent column to the table

        Parameters
        ----------
        name : str 
             Name of dependent variable (observable)
        unit : str (optional)
             Unit of values 
        
        Returns
        -------
        c : Dependent
            New column object 
        """
        c = Dependent(name,unit)
        self._d[self.DEPENDENT_VARIABLES].append(c._d)
        self._y.append(c)
        return c

    @accepts(name=str,unit=str)
    def independent(self,name,unit=None):
        """Add a independent column to the table

        Parameters
        ----------
        name : str 
             Name of independent variable 
        unit : str (optional)
             Unit of values 
        
        Returns
        -------
        c : Independent
            New column object 
        """
        c = Independent(name,unit)
        self._d[self.INDEPENDENT_VARIABLES].append(c._d)
        self._x.append(c)
        return c
        
    @accepts(ny=int,nx=int)
    def roundNsig(self,ny,nx=None):
        """Round to ny(nx) significant digits"""
        if nx is None:
            nx = ny

        if ny >= 1:
            for c in self._y:
                c.roundNsig(ny)

        if nx >= 1:
            for c in self._x:
                c.roundNsig(nx)

        return self

    @accepts(ny=int,nx=int)
    def round(self,ny,nx=None):
        """Round to ny(nx) decimal places"""
        if nx is None:
            nx = ny

        if ny >= 1:
            for c in self._y:
                c.round(ny)
        
        if nx >= 1:
            for c in self._x:
                c.round(nx)

        return self

    def _independentSelect(self,select=None):
        """Get independent columns that meet a criteria 
        
        Get a list of independent columns that meet a certain
        criteria. For more, see Independent.select.

        Parameters
        ----------
        select : str, list of str, or callable (optional)
            Selection criteria.  See also Independent.select 
            If None, return all independent columns 
        
        Returns
        -------
        cols : list or None 
            Selected columns 

        """
        if select is None:
            return self._x

        return [x for x in self._x if x.select(select) is not None]
    
    def _dependentSelect(self,names=None,qualifiers=None):
        """Get dependent columns that meet a criteria 
        
        Get a list of dependent columns that meet a certain
        criteria. For more, see Dependent.select.

        If both names and qualifiers are None, return all dependent
        columns

        Parameters
        ----------
        names : str, list of str, or callable (optional)
            Selection criteria.  See also Dependent.select 
        qualifiers : dict, list of dict, or callable (optional)
            Selection criteria.  See also Dependent.select 

        Returns
        -------
        cols : list or None 
            Selected columns
        """
        if names is None and qualifiers is None:
            return self._y

        return [y for y in self._y if y.select(names,qualifiers) is not None]

    def select_independent(self,select=None):
        """Select independent columns 

        Returns a list of independent columns.  If no columns are
        selected None is returned.

        Parameters
        ----------
        select : str, list of str, or callable (optional)
            Selection criteria.  See also :meth:`Independent.select`
            If None, return all independent columns

        Returns
        -------
        cols : list or None 
            Selected independent columns 
        """
        return self._independentSelect(select)

    def select_dependent(self,names=None,qualifiers=None):
        """Select dependent columns 

        Returns a list of dependent columns.  If no columns are
        selected None is returned.

        Parameters
        ----------
        names : str, list of str, or callable (optional)
            Selection criteria.  See also :meth:`Dependent.select` 
        qualifiers : dict, list of dict, or callable (optional)
            Selection criteria.  See also :meth:`Dependent.select` 

        Returns
        -------
        cols : list or None 
            Selected independent columns 
        """
        return self._dependentSelect(names,qualifiers)
    
    def select(self,indep_select=None,dep_names=None,dep_qualifiers=None):
        """Select independent and dependent columns 
        
        Returns a two tuple of lists of independent and dependent
        columns.  If none are selected, the tuple holds the value
        None.

        Parameters
        ----------
        indep_select : str, list of str, or callable (optional)
            Selection criteria.  See also :meth:`Independent.select`
            If None, return all independent columns
        dep_names : str, list of str, or callable (optional)
            Selection criteria.  See also :meth:`Dependent.select` 
        dep_qualifiers : dict, list of dict, or callable (optional)
            Selection criteria.  See also :meth:`Dependent.select` 

        Returns
        -------
        indep_cols : list or None 
            Selected independent columns 
        dep_cols : list or None 
            Selected dependent columns 
        """
        return (self._independentSelect(indep_select),
                self._dependentSelect(dep_names,dep_qualifiers))
                
    
    def assertSizes(self):
        """Check that all sizes match"""
        len_indep = [len(i) for i in self._x if len(i) > 0]
        len_dep   = [len(d) for d in self._y]

        # Less-than to allow for empty table 
        assert len(set(len_indep+len_dep)) <= 1,\
            'Inconsistent lengths of independent variables ({}) '\
            'and dependent variables ({}) -> {}'\
            .format(len_indep,len_dep,set(len_indep+len_dep))

    @classmethod
    def fromDict(cls,d):
        """Construct a Table object from a dictionary

        Parameters
        ----------
        d : dict 
            Dictionary to construct from.  This could be read from a
            YAML/JSON file.
        
        Returns
        -------
        t : Table 
            Newly constructed Table object 
        """
        # if not d.get(cls.INDEPENDENT_VARIABLES,False):
        #     pprint(d)
        # assert d.get(cls.INDEPENDENT_VARIABLES,False),\
        #     "No {} in dictionary".format(cls.INDEPENDENT_VARIABLES)
        assert d.get(cls.DEPENDENT_VARIABLES,False),\
            "No {} in dictionary".format(cls.DEPENDENT_VARIABLES)

        t = cls()
        t._d = d;

        for di in d[cls.INDEPENDENT_VARIABLES]:
            i = Independent.fromDict(di)
            t._x.append(i)

        for di in d[cls.DEPENDENT_VARIABLES]:
            i = Dependent.fromDict(di)
            t._y.append(i)

        return t

    def data(self,x_kw={},y_kw={}):
        '''Extract data (x,y) from the table.  This returns a list of all
        independent values (one list per variable) and all dependent
        values (one list per variable).

        The independent and dependent values are extracted using the
        keywords `x_kw` and `y_kw`.  For example, to add get total
        uncertainties, do for example 

            table.data(y_kw={'calc':Propagator.center,
                             'center_calc':Propagator.linvar})

        Parameters
        ----------
        x_kw : dict 
            Dictionary of keywords to extract independent variables.  
            See also Independent.e 
        y_kw : dict 
            Dictionary of keywords to extract dependent variables. 
            See also Dependent.ye 
        
        Returns 
        ------- 
        data : list 
            A list of independent and dependent variables.  Each
            variable is a list where each element is a tuple of value
            and uncertainties.  Note that the uncertainties may be a
            list or tuple on it's own.  Exactly how these are returned
            depend on the parameters x_kw and y_kw.  In BNF

                return              ::= variables
                variables           ::= variable
                                    |   variable variables
                variable            ::= entry 
                                    |   entry variable
                variable_entry      ::= value uncertainties 
                uncertainties       ::= 
                                    |    uncertainty 
                                    |    uncertainty uncertainties
                uncertainty         ::= value
                                    |   value value 
                value               ::= A number

        '''
        i = [[(xx,ee) for xx,ee in zip(x.x,x.e(**x_kw))] for x in self._x]
        d = [[(yy,ee) for yy,ee in y.ye(**y_kw)] for y in self._y]
        return i + d

    use_beautifier = {'text/html': True,
                      'text/latex': True,
                      'text/markdown': True }
    '''Class option for whether to use the names interface to
    beautify names.  This is a dictionary that maps from mime 
    representation to a boolean option.  If a mimetype isn't 
    present in the dictionary then beautification isn'tr used'''

    def _beautifier(self,mime):
        '''Get the beautifier depending on the mime type and the setting 
        in use_beautifier'''
        if Table.use_beautifier.get(mime,False):
            from . names import Beautifier
            return Beautifier()
        return None
        
    def _repr_html_(self):

        '''Get HTML representation of this table'''
        def sym(v):
            return f'&plusmn;{v}'

        def asym(v):
            return f'<sup>+{v[1]}</sup><sub>{v[0]}</sub>'
        
        def cell(v,head=False,n=None):
            m = f' colspan={n}' if n is not None else ''
            if head:
                return f'    <th{m}>{v}</th>\n'
            return f'    <td{m}>{v}</td>\n'

        def line(cells,odd):
            return f'  <tr class="{"odd" if odd else "even"}">\n'+\
                ''.join(cells)+'  </tr>\n'

        o = "<table>\n";
        o += self._repr_x_(cell,line,sym,asym,None,
                           self._beautifier('text/html'))
        o += "</table>\n"

        return o

    def _repr_markdown_(self):
        '''Get Markdown representation of this table'''
        def sym(v):
            '''Symmetric uncertainty

            Parameters
            ----------
            v : float 
                Value

            Returns
            -------
            s : str 
                 Formatted uncertainty
            '''
            return fr'\pm{v}'

        def asym(v):
            '''A-symmetric uncertainty
            
            Parameters
            ----------
            v : float,float
                Value

            Returns
            -------
            s : str 
                 Formatted uncertainty
            '''
            return f'{{}}^{{+{v[0]}}}_{{-{v[1]}}}'
        
        def cell(v,head=False,n=None):
            '''A single cell. 
            
            Parameters
            ----------
            v : str
                If head is True, then the header (str).
                Otherwise, the formatted value 
            n : int or None
                Column span or None 

            Returns
            -------
            s : str 
                 Formatted cell 
            '''
            m = '' if n is None else '|'*n
            if head:
                return f'{v}'+m
            return f'${v}$'+m

        def line(cells,odd):
            '''A line of output 
            
            Parameters
            ----------
            cells : sequence 
                A sequence of formatted cells 
            odd : bool 
                True if this is an odd numbered line 

            Returns
            -------
            s : str 
                 Formatted line
            '''
            return '|'+'|'.join(cells)+'|\n'

        def top(n):
            '''Top row (below possible headers)
            
            Parameters
            ----------
            n : int 
                Number of cells 
            
            Returns 
            -------
            s : str 
                 Formatted top row 
            '''
            return '|'+'|'.join([':---' for _ in range(n)])+'|\n'

        return self._repr_x_(cell,line,sym,asym,top,
                             self._beautifier('text/markdown'))
        
    def _repr_latex_(self):
        '''Get LaTeX representation of this table'''
        def sym(v):
            return fr'\pm{v}'

        def asym(v):
            return f'{{}}^{{+{v[0]}}}_{{-{v[1]}}}'
        
        def cell(v,head=False,n=None):
            if head:
                t = f'{v}'
            t = f'${v}$'
            
            if n is None:
                return t

            return fr'\multicolumn{{{n}}}{{{"c" if head else "l"}}}{{{t}}}'

        def line(cells,odd):
            return '    '+'\n    &'.join(cells)+'\n'+r'    \\'+'\n'

        def top(n):
            return r'  \hline'+'\n'

        d = self.data()
        o =  r'\begin{tabular}{|'+('c'*len(d))+'|}\n'+r'  \hline'+'\n'
        o += self._repr_x_(cell,line,sym,asym,top,
                           self._beautifier('text/latex'))
        o += r'  \hline'+'\n'+r'\end{tabular}'+'\n'

        return o
    
    def _repr_text_(self):
        '''Get text representation of this table'''
        def sym(v):
            return fr'+/-{v}'

        def asym(v):
            return f'(+{v[0]},-{v[1]})'
        
        def cell(v,head=False,n=None):
            return f'{v}'

        def line(cells,odd):
            return '\t'.join(cells)+'\n'

        def top(n):
            return ''

        return self._repr_x_(cell,line,sym,asym,top,None)
        
    def _repr_x_(self,cell,line,sym,asym,top=None,beautifier=None):
        """Get A representation of this table

        Parameters
        ---------- 
        cell : callable 
            A function to format a cell 
        line : callable 
            A function to format a line 
        sym : callable 
            A function to format symmetric uncertainties 
        asym : callable 
            A function to format a-symmetric uncertainties 
        top : callable 
            A function to format the cells of the top line 
        beautifier : hepdata.Beautifier 
            Beautifier to use 
        """
        from . utils import _ensureList
        from . beautifier import Beautifier
        b = Beautifier() if beautifier is None else beautifier;
        
        o = ''
        o += line([cell(b.var(c.name),  True) for c in self._x] + 
                  [cell(b.obs(c.name),  True) for c in self._y],False)
        o += line([cell(b.unit(c.units),True) for c in self._x + self._y],True)

        q = set.union(*[{q[Dependent.NAME] for q in y.qualifiers()}
                        for y in self._y])
        for qq in q:
            cx = [cell(b.qname(qq),True,len(self._x)-1)]
            cy = []
            for y in self._y:
                qqq = y.qualifiers(qq)
                txt = ''
                if qqq and len(qqq) > 0:
                    txt = ', '.join([b.qual(qqqq.get(Dependent.NAME,''),
                                            qqqq.get(Dependent.VALUE,''),
                                            qqqq.get(Dependent.UNITS,''))
                                     for qqqq in qqq])

                cy += [cell(txt,False)]

            o += line(cx+cy,True)
        

        d = self.data()
        if top is not None:
            o += top(len(d))

        for i,c in enumerate(zip(*d)):
            l = []
            for v in c:
                try:
                    vv = v[0]
                    ee = _ensureList(v[1:][0])
                except:
                    vv = v
                    ee = []

                s = f'{vv}'+''.join([asym(eee) if isinstance(eee,tuple) else
                                    sym(eee) for eee in ee])
                l.append(cell(s,False))

            o += line(l, i % 2 == 1)

        
        return o        

    def _repr_mimebundle_(self,include=None,exclude=None):
        '''Get mime representation of this table'''
        return {'text/html':     self._repr_html_(),
                'text/markdown': self._repr_markdown_(),
                'text/latex':    self._repr_latex_() }
        

        
            
#
# EOF
#
