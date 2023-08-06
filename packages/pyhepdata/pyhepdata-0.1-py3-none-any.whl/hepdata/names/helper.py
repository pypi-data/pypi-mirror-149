"""Some class methods to easily define submission objects with the
assistance ofthe hepdata.names framework

Copyright 2019 Christian Holm Christensen
"""
from .. submission import Submission
from . phrase import Phrase 
from . particle import Particle
from . variable import Variable
from . observable import Observable
from . unit import Unit
from . pretty import Pretty
from .. utils import _ensureList

class Helper:
    """Collection of utilities"""
    
    @classmethod
    def table(cls,
              sub,
              desc,
              sys,
              sqrts,
              var,
              obs,
              parts=None,
              phrases=[],
              name=None,
              filename=None,
              loc=None,
              num=1,
              subnum='',
              same=False):
        """Utility function to easily define a data table.  
        
        This will fill in information based on the passed arguments,
        such as the units for variables and observables, phrases based
        on variables and observerables, and so on.

        >>> t = hepdata.names.Helper.table(sub,
        ...                                'Some data',
        ...                                System.PP,
        ...                                13000,
        ...                                Variable.PT,
        ...                                Varible.Y_INVARIANT_YIELD,
        ...                                [Particle.PI,Particle.K],
        ...                                ['More phrases'],
        ...                                num=1)

        >>> t = hepdata.names.Helper.table(sub,
        ...                                'Some data',
        ...                                System.PP,
        ...                                13000,
        ...                                Variable.PT,
        ...                                Varible.Y_INVARIANT_YIELD,
        ...                                [Particle.PI,Particle.K],
        ...                                name='My table',
        ...                                filename='mytable.yaml',
        ...                                loc='In the paper')
        

        Parameters
        ----------
        sub : Submission 
            Submission to add the data table to 
        desc : str 
            Free-form description of table 
        sys : System identifier 
            Collision system identifier 
        sqrts : float 
            Collision energy in centre of mass (in GeV)
        var : Variable indentifier 
            Independent variable 
        obs : Observable identifier(s)
            (List of) Observable 
        parts : Particle identifier(s)
            (List of) particles produced 
        phrases : List of Phrase identifiers 
            Additional phrases 
        num : int or str
            Data table (Location) identifier 
        sub : int or str 
            Data table (Location) sub identifier 
        name : str  (optional)
            Name of table.  Mutually exclusive with arguments 
            num and subnum            
        filename : str  (optional)
            Name of file to write data to. Mutually exclusive with
            arguments num and subnum
        loc : str (optional)
            Location. Mutually exclusive with
            arguments num and subnum
        same : bool (optional)
            If true, then we will put the data table into the same
            file as the submission it self.

        Returns
        -------
        table : Table 
            A data table to be filled
        meta : Meta 
            The meta data of the table 

        """
        pl = _ensureList(parts)
        ol = _ensureList(obs)
        sl = _ensureList(sys)
        tl = _ensureList(sqrts)
        op = Observable.phrases(ol)
        vp = Variable  .phrases(var)
        if pl is None:
            pl = [Particle.X]

        if desc is None:
            desc = cls.description(sys,sqrts,var,obs,parts)

        return sub.table(desc,sl,tl,var,obs,
                         parts=pl,phrases=op+vp+phrases,
                         num=num,subnum=subnum,
                         name=name,filename=filename,loc=loc,
                         same=same,both=True)
        
    @classmethod
    def independent(cls,table,var):
        """Utility to create an independent variable column 

        >>> i = hepdata.names.Helper.independent(Variable.PT)
        
        One can declare multiple columns at a time by passing a list
        of Variable identifiers

        >>> is = hepdata.names.Helper.independent([Variable.PT,Variable.MT])

        Parameters
        ----------
        table : Table 
            Table to add column(s) to 
        var : Variable or list of Variable 
            Indepent variable identifier(s)

        Returns
        -------
        ind : Independent ot list
            A new independent variable column(s)

        Notes
        -----

        Although it is possible to define multiple columns with the
        same variable 
        
        >>> is = hepdata.names.Helper([Variable.PT]*3)

        it does not make a lot of sense.  If the intent is to define a
        2D table of say the diffential cross-section versus
        :math:`p_{\mathrm{T}}` of pions and kaons separately, one
        should define a new variable for each of these.  For example 

        >>> hepdata.names.Variable.register('PT_PI',
        ...                                 'PT(PI)',
        ...                                 r'p_{\mathrm{T,\pi}}',
        ...                                 Variable.phrases(Variable.PT))
        >>> hepdata.names.Variable.register('PT_K',
        ...                                 'PT(K)',
        ...                                 r'p_{\mathrm{T,K}}',
        ...                                 Variable.phrases(Variable.PT))

        and then use those when declaring the independent variables 
        
        >>> is = hepdata.names.Helper([Variable.PT_PI,Variable.PT_K])

        """
        if type(var) in [list,tuple]:
            return [table.independent(v,Unit.var(v)) for v in var]
        return table.independent(var,Unit.var(var))

    @classmethod
    def _dependent(cls,table,obs,parts=None,more=None):
        """Create a single dependent variable column 

        >>> hepdata.names._dependent(t,Observable.DNDYRAP,
        ...                          [Particle.PI_P],
        ...                          [dict(name='CENTRALITY',
        ...                                value='0-10'),
        ...                           dict(name='PT',
        ...                                value='500-10000',
        ...                                units=Units.MEV)])


        Multiple dependent variable columns can be declared in a
        single go

        >>> hepdata.names.

        Parameters
        ----------
        table : Table 
            Table to add column to 
        obs : Observable 
            Observable identifier 
        parts : Particle or list 
            (List of) Particle identifier(s)
        more : list 
            Additional qualifiers to add to column.  
    
            Each entry must be a dict with 
        
            - ``name`` : str 
                Name of qualifier 
            - ``value`` : str or float 
                Value of qualifier 
            - ``units`` : str (optional)
                Units of identfier.  If not specified, we will try to
                deduce it from the qualifier name

        Returns
        -------
        dep : Dependent 
            The dependent variable column

        """
        from hepdata import Dependent
        dep = table.dependent(obs,Unit.obs(obs))
        if parts is not None:
            dep.qualifier('PARTICLE',' '.join(p for p in _ensureList(parts)))

        if more is not None:
            # print(f'Got more: {more}')
            for m in _ensureList(more):
                # print(f'Adding qualifier: {m}')
                dep.qualifier(m.get('name'),
                              m.get('value'),
                              Unit.var(m.get('name'),
                                       m.get('units')))
                    
        return dep
     
    @classmethod
    def dependent(cls,table,obs,parts=None,more=None):
        """"A utility to easily make dependent variable column

        This fills in various pieces of information based on the
        observable, particles, and list of qualifiers optionally
        passed

        >>> d = hepdata.names.dependent(t,Observable.DNDYRAP,
        ...                             [Particle.PI_P],
        ...                             [dict(name='CENTRALITY',
        ...                                  value='0-10'),
        ...                              dict(name='PT',
        ...                                   value='500-10000',
        ...                                   units=Units.MEV)])


        Multiple dependent variable columns can be declared in a
        single go

        >>> ds = hepdata.names.dependent(t,[Observable.D3_YIELD,
        ...                                 Observable.D3_XSEC])

        If we pass a single value or list for particles (or additional
        qualifiers), then those will be copied to all returned
        dependent variable columns.

        >>> ds = hepdata.names.dependent(t,[Observable.D3_YIELD,
        ...                                 Observable.D3_XSEC],
        ...                              Particle.PI_P)
        
        Here, all returned columns will have the qualifier 
        
            ``PARTICLE = PI+``

        >>> ds = hepdata.names.dependent(t,[Observable.D3_YIELD,
        ...                                 Observable.D3_XSEC],
        ...                              more=[dict(name=Variable.YRAP,
        ...                                         value=0),
        ...                                    dict(name='SELECT',
        ...                                         value='INELASTIC')])

        If we are to give separate particles or aditional qualifiers
        for each column, we must pass a list of list of particles or
        qualifiers.
        
        >>> ds = hepdata.names.dependent(t,[Observable.D3_YIELD,
        ...                                 Observable.D3_XSEC],
        ...                              more=[[dict(name=Variable.LUMI,
        ...                                          value=10)],[]])
        
        Note, we need not specifiy additional qualifiers for `all`
        columns: The last set of qualifiers will be copied to the
        remaining columns.  To make these empty, put the empty list at
        the end of the list of lists (as above). 
        
        Parameters
        ----------
        table : Table 
            Table to add column to 
        obs : Observable or list 
            Observable identifier(s) 
        parts : Particle or list 
            (List of) Particle identifier(s)

            If more than one observable is given, and this argument is

            - a list of lists of identifiers, then each observable
                will get it's own set of particle qualifiers.

            - a list of identifiers, then all observables will get
                the same set of particle qualifier.

        more : list or list of list
            Additional qualifiers to add to column.  
        
            If more than one observable is given, and this argument is

            - a list of lists of dictionaries, then each observable
                will get it's own set of additional qualifiers.

            - a list of dictionaries, then all observables will get
                the same set of additional qualifier.

            Each dict entry must be 
        
            - ``name`` : str 
                Name of qualifier 
            - ``value`` : str or float 
                Value of qualifier 
            - ``units`` : str (optional)
                Units of identfier.  If not specified, we will try to
                deduce it from the qualifier name

        Returns
        -------
        dep : Dependent or list
            The dependent variable column(s)

        """
        if type(obs) not in [list,tuple]:
            return cls._dependent(table,obs,parts,more)

        def _pad(inp,n):
            if type(inp) in [list,tuple] and len(inp) > 0:
                if len(inp) > 0 and type(inp[0]) in [list,tuple]:
                    # We have list of list.  Let's append however much we need
                    return inp + [inp[-1]]*(n-len(inp))
                else:
                    return inp + [inp[-1]]*(n-len(inp))

            # We have a single list or single value 
            return [inp]*(n)

        pl = _pad(parts,len(obs))
        ml = _pad(more, len(obs))
        # print(pl)
        
        return [cls._dependent(table,o,p,m) for o,p,m in zip(obs,pl,ml)]

    @classmethod
    def columns(cls,
                sub,
                desc,
                sys,
                sqrts,
                var,
                obs,
                parts=None,
                phrases=[],
                more=[],
                name=None,
                filename=None,
                loc=None,
                num=1,
                subnum='',
                isaa=False,
                same=False):        
        """Utility function to easily define a data table and columns. 
        
        For each independent variable in ``var`` we create an
        independent variable column.  

        For each dependent variable in ``obs`` we create an
        independent variable column.  
                
        This will fill in information based on the passed arguments,
        such as the units for variables and observables, phrases based
        on variables and observerables, and so on.

        Parameters
        ----------
        sub : Submission 
            Submission to add the data table to 
        desc : str 
            Free-form description of table.  If None, use
            :meth:`Helper.description` to fill this in
        sys : System identifier 
            Collision system identifier 
        sqrts : float 
            Collision energy in centre of mass (in GeV)
        var : Variable indentifier 
            Independent variable 
        obs : Observable identifier(s)
            (List of) Observable 
        parts : Particle identifier(s)
            (List of) particles produced 
        phrases : List of Phrase identifiers 
            Additional phrases 
        more : dict, list of dict, or list of list of dict
            Additional qualifiers 
        num : int or str
            Data table (Location) identifier 
        subnum : int or str 
            Data table (Location) sub identifier 
        name : str  (optional)
            Name of table.  Mutually exclusive with arguments 
            num and subnum            
        filename : str  (optional)
            Name of file to write data to. Mutually exclusive with
            arguments num and subnum
        loc : str (optional)
            Location. Mutually exclusive with
            arguments num and subnum
        same : bool (optional)
            If true, then we will put the data table into the same
            file as the submission it self.

        Returns
        -------
        table : Table 
            A data table to be filled
        meta : Meta 
            The meta data of the table
        ind : Independent or list 
            (List of) Independent variable(s) 
        dep : Dependent or list 
            (List of) Dependent variable(s)

        """
        if desc is None:
            desc = cls.description(sys,sqrts,var,obs,parts)
        t, m = cls.table(sub, desc, sys, sqrts, var, obs,
                         parts=parts, phrases=phrases,
                         name=name, filename=filename,
                         loc=loc, num=num, subnum=subnum,
                         same=same)
        i = cls.independent(t, var)
        d = cls.dependent(t, obs, parts, more)
        return t, m, i, d
    
    @classmethod
    def description(cls,sys,sqrts,var,obs,parts=None,more='',isaa=False):
        """Utlity to easily format a description based on the system,
        collision energy, variable, observables, and particles.

        This is useful in conjuction with the table
        :meth:`Helper.table` - the returned string can be passed to
        that method as the description string.

        >>> sys = System.PP
        >>> sqrts = 13000
        >>> var   = Variable.PT
        >>> obs   = Observable.Y_INVARIANT_YIELD
        >>> parts = [Particle.PI,Particle.K]
        >>> d = hepdata.names.Helper.description(sys,sqrts,var,obs,parts)
        >>> t = hepdata.names.Helper.table(sub,d,sys,sqrts,var,obs,parts,
        ...                                ['More phrases'], num=1)

        The returned string is formatted as 

            [Observables] versus [Variables] for [Particles] in
            [Systems] at [Energy] [More]

        where if a bracketed part is not specified, the corresponding
        propersitions will be left out too.

        Parameters
        ----------
        sys : System identifier 
            Collision system identifier 
        sqrts : float 
            Collision energy in centre of mass (in GeV)
        var : Variable indentifier 
            Independent variable 
        obs : Observable identifier(s)
            (List of) Observable 
        parts : Particle identifier(s)
            (List of) particles produced 
        more : str 
            More text to add 
        
        Returns
        -------
        desc : str 
            Description

        """ 
        pl   = _ensureList(parts)    
        ol   = _ensureList(obs)      
        vl   = _ensureList(var)      
        op   = Observable.phrases(ol)
        sl   = _ensureList(sys)
        tl   = _ensureList(sqrts)
        if type(pl[0]) in [tuple,list]:
            tmp = [];
            for t in pl:
                tmp.extend(t)
            pl = tmp

        # print(f'Generating description from\n'
        #       f'  Particles:   {pl}'+'\n'
        #       f'  Observables: {ol}'+'\n'
        #       f'  Variables:   {vl}'+'\n'
        #       f'  Phrases:     {op}'+'\n'
        #       f'  Systems:     {sl}'+'\n'
        #       f'  Energies:    {tl}'+'\n'
        #       f'  More:        {more}')
        desc = ', '.join(Pretty.obs(o) for o in set(ol)) + \
            ' versus ' + ', '.join(Pretty.var(v) for v in set(vl))
    
        if pl is not None and len(pl) > 0:
            desc += ' for ' + ', '.join(Pretty.part(p) for p in set(pl))

        if sl is not None and len(sl) > 0:
            desc += ' in '+','.join([Pretty.col(s) for s in set(sl)])

        if tl is not None and len(tl) > 0:
            if sl is not None and len(sl) > 0:
                tsl = list(zip(tl,sl))
                desc += ' at '+','.join(Pretty.sqrts(ts[0],ts[1])
                                        for ts in set(tsl))
            else:
                desc += ' at '+','.join(Pretty.sqrts(t) for t in set(tl))
                

        desc += ' ' + more
        return desc


#
# EOF
#
