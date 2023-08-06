"""Pretty printing/formatting of hepdata.names constants 

Copyright 2019 Christian Holm Christensen
"""

class Pretty:
    """Class to pretty print various information.
    
    Pretty print are automatically registered by the various register
    methods.
    """
    UNKNOWN = 'Unknown'
    OBS_MAP  = {}
    PART_MAP = {}
    UNIT_MAP = {}
    VAR_MAP  = {}
    COL_MAP  = {}
    QUAL_MAP = {}
    
    @classmethod
    def _lookup(cls,x,m,df=None,math=True):
        """Look-up a pretty print mapping of x in map m. 

        If x isn't in m, then return df.  If math is true, put math
        delimiters around the returned string.
        
        Parameters
        ----------
        - x : str 
               Value to look-up 
        - m : dict 
                Mapping to look up x in 
        - df : str 
                Default value if x isn't found in m 
        - math : bool 
                If true, put math delimiters around returned string 

        Returns
        -------
        - ret : str 
                The pretty-print string

        """
        if x in m:
            if math:
                return '$'+m[x]+'$'
            else:
                return m[x]
            
        return df

    @classmethod
    def _add(cls,x,y,m):
        """Add mapping from x to y in map m 
        
        Parameters
        ----------
            x : str 
                Key value 
            y : str 
                Value 
            m : dict 
                Mapping to update 

        Returns
        -------
            self : Pretty 
                Reference to this class 
        """
        m[x] = y
        return cls
    
    @classmethod
    def register_part(cls,name,pretty):
        """Register a particle 
        Parameters
        ----------
            name : str 
                Key value 
            pretty : str 
                Value 

        Returns
        -------
            self : Pretty 
                Reference to this class 
        """
        return cls._add(name,pretty,cls.PART_MAP)

    @classmethod
    def register_col(cls,name,pretty):
        """Register a collision system
        Parameters
        ----------
            name : str 
                Key value 
            pretty : str 
                Value 

        Returns
        -------
            self : Pretty 
                Reference to this class 
        """
        cls._add(name,pretty,cls.COL_MAP)

    @classmethod
    def register_unit(cls,name,pretty):
        """Register a unit 
        Parameters
        ----------
            name : str 
                Key value 
            pretty : str 
                Value 

        Returns
        -------
            self : Pretty 
                Reference to this class 
        """
        return cls._add(name,pretty,cls.UNIT_MAP)

    @classmethod
    def register_var(cls,name,pretty):
        """Register a variable  
        Parameters
        ----------
            name : str 
                Key value 
            pretty : str 
                Value 

        Returns
        -------
            self : Pretty 
                Reference to this class 
        """
        return cls._add(name,pretty,cls.VAR_MAP)

    @classmethod
    def register_obs(cls,name,pretty):
        """Register an observable  
        Parameters
        ----------
            name : str 
                Key value 
            pretty : str 
                Value 

        Returns
        -------
            self : Pretty 
                Reference to this class 
        """
        return cls._add(name,pretty,cls.OBS_MAP)

    @classmethod
    def register_qual(cls,name,pretty):
        """Register a qualifer
        Parameters
        ----------
            name : str 
                Key value 
            pretty : str 
                Value 

        Returns
        -------
            self : Pretty 
                Reference to this class 
        """
        return cls._add(name,pretty,cls.QUAL_MAP)

    @classmethod
    def obs(cls,obs,math=True):
        """Find pretty-print representation of observable

        Parameters 
        ----------
            obs : str 
                Value to look-up. 
        
        Returns
        -------
            ret : str 
                Pretty print string, or obs if no mapping registered
        """
        return cls._lookup(obs,cls.OBS_MAP,obs,math)

    @classmethod
    def part(cls,part,math=True):
        """Find pretty-print representation of particle

        Parameters 
        ----------
            part : str 
                Value to look-up. 
            math : bool 
                If true, add math mode delimiters
        
        Returns
        -------
            ret : str 
                Pretty print string, or part if no mapping registered
        """
        return cls._lookup(part,cls.PART_MAP,part,math)

    @classmethod
    def col(cls,col,math=True):
        """Find pretty-print representation of collision system

        Parameters 
        ----------
            col : str 
                Value to look-up. 
            math : bool 
                If true, add math mode delimiters
        
        Returns
        -------
            ret : str 
                Pretty print string, or col if no mapping registered
        """
        return cls._lookup(col,cls.COL_MAP,col,math)

    @classmethod
    def sys(cls,col,math=True):
        """Find pretty-print representation of collision system

        Parameters 
        ----------
            col : str 
                Value to look-up. 
            math : bool 
                If true, add math mode delimiters
        
        Returns
        -------
            ret : str 
                Pretty print string, or col if no mapping registered
        """
        return cls._lookup(col,cls.COL_MAP,col,math)
    
    @classmethod
    def var(cls,var,math=True):
        """Find pretty-print representation of variable 

        Parameters 
        ----------
            var : str 
                Value to look-up. 
            math : bool 
                If true, add math mode delimiters
        
        Returns
        -------
            ret : str 
                Pretty print string, or var if no mapping registered
        """
        return cls._lookup(var,cls.VAR_MAP,var,math)

    @classmethod
    def unit(cls,unit,math=True):
        """Find pretty-print representation of unit

        Parameters 
        ----------
            unit : str 
                Value to look-up. 
            math : bool 
                If true, add math mode delimiters
        
        Returns
        -------
            pretty : str 
                Pretty print string, or unit if no mapping registered
        """
        return cls._lookup(unit,cls.UNIT_MAP,unit,math)

    
    @classmethod
    def sqrts(cls,sqrts,col=None,isaa=False):
        """Pretty print collision energy in CMS

        Parameters
        ----------
            sqrts : float
                Collision energy in GeV
            col : str (optional)
                The collision system (decides if we do sqrt(s) or sqrt(sNN) 

        Returns
        -------
            pretty : str 
                Pretty print string or col if no mapping registered
        """
        from hepdata.names.system import System
        from hepdata.names.unit import Unit
        # print(f'Format collision energy {sqrts} for {col}')
        
        if isaa or (col is not None and System.isAA(col)):
            s = r'\sqrt{s_{\mathrm{NN}}}'
        else:
            s = r'\sqrt{s}'

        u = cls.unit(getattr(Unit,'GEV','GeV'),False)
        fmt = '{}'
        try:
            isqrts = int(sqrts)
            if int(sqrts) > 1000:
                u = cls.unit(getattr(Unit,'TEV','TeV'),False)
                sqrts = isqrts / 1000
            fmt = '{:.0f}' if isqrts % 1000 == 0 else '{}'
        except:
            pass 
        se  = fmt.format(sqrts)

        return r'${}={}\,{}$'.format(s,se,u)

    @classmethod
    def rap(cls,y):
        """Find pretty-print representation of rapidity

        Parameters 
        ----------
            eta : float,list,tuple
                Value to look-up. 
        
        Returns
        -------
            pretty : str 
                Pretty print string or col if no mapping registered
        """
        if type(y) in [list,tuple] and len(y) == 2:
            return r'$y={}-{}$'.format(y[0],y[1])
        return r'$y={}$'.format(y)

    @classmethod
    def eta(cls,eta):
        """Find pretty-print representation of pseudo-rapidity

        Parameters 
        ----------
            eta : float,list,tuple
                Value to look-up. 
        
        Returns
        -------
            pretty : str 
                Pretty print string or eta if no mapping registered
        """
        if type(eta) in [list,tuple] and len(eta) == 2:
            return r'$\eta={}-{}$'.format(eta[0],eta[1])
        return r'$\eta={}$'.format(eta)

    @classmethod
    def cent(cls,c):
        """Pretty print string for centrality measure 

        Parameters 
        ----------
            c : float, str or list 
                Centrality - either a single value or a bin (two values)
        
        Returns
        -------
            pretty : str 
                Pretty print string of the centrality 
        """
        if c is None:
            return ''
        if type(c) in [list,tuple] and len(c) == 2:            
            return r'${}-{}$% central'.format(c[0],c[1])
        if type(c) is str and c == 'minbias':
            return 'Min.Bias'
        return r'${}$% central'.format(c)

    @classmethod
    def ang(cls,var,x,unit=None):
        if x is None:
            return ''

        txt = "{}={}".format(cls.var(var,False),x)
        if unit is not None and unit == 'DEGREE':
            txt += "^{\circ}"
        return "$"+txt+"$"
    
    @classmethod
    def ratio(cls,p1,p2):
        """Format a ratio of particles given two particle identifiers 
        
        Parameters
        ----------
            p1 : str 
                Particle identifier 
            p2 : str
                Particle identifier 

        Returns
        -------
            pretty : str 
                Pretty print string of the centrality 
        """
        return "{}/{}".format(cls.part(p1,math=False),
                              cls.part(p2,math=False))

    @classmethod
    def qual(cls,name,math=False):
        """Find pretty-print representation of observable

        Parameters 
        ----------
            name : str 
                Value to look-up. 
        
        Returns
        -------
            ret : str 
                Pretty print string, or name if no mapping registered
        """
        return cls._lookup(name,cls.QUAL_MAP,name,math)

    #
    # EOF
    #
    
