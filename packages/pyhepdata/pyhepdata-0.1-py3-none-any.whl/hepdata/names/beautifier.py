"""Beautifier using the hepdata.names databases 

Copyright 2019 Christian Holm Christensen 
"""
from .. plot.beautifier import Beautifier as BaseBeautifier
from . pretty import Pretty
from . phrase import Phrase
from . particle import Particle
from . system import System
from . variable import Variable
from . observable import Observable
from . unit import Unit

class Beautifier(BaseBeautifier):
    def __init__(self):
        super(Beautifier,self).__init__()

    def _value(self,name,value=None,units=None):
        if value is None:
            if units is None:
                return ''
            if '$' in units:
                units = units.replace('$', '')
            return r' \left({}\right)'\
                .format(Pretty.unit(Unit.obs(name,units),False))

            
        value = str(value)
        if '$' in value:
            value = value.replace('$','')
        else:
            value = fr'\text{{{value}}}'

        if units is None or units == '':
            return '{}'.format(value)

        return r'{}\,{}'\
            .format(value,Pretty.unit(Unit.obs(name,units),False))

    def _obsvar(self,name,value=None,units=None,func=Pretty.obs):
        """Format a qualifier
        
        Parameters
        ----------
        name : str 
            Name 
        value : str or float
            Value 
        units : str 
            Units 
        
        Returns
        -------
        r : str 
            Formatted string 
        """
        if '$' in name:
            v = self._value(name,value,units)
            if v == '':
                r = name
            else:
                r = '{} ${}$'.format(name,v)
        else:
            r = '${}$'.format(func(name,False))
        return r
        
    def qualifier(self,name,value=None,units=None):
        """Format a qualifier
        
        Parameters
        ----------
        name : str 
            Name 
        value : str or float
            Value 
        units : str 
            Units 
        
        Returns
        -------
        r : str 
            Formatted string 
        """
        if name == 'PARTICLE':
            return ','.join([Pretty.part(p) for p in value.split()])
        if name == Variable.ETARAP:
            return Pretty.eta(value)
        if name == Variable.YRAP:
            return Pretty.rap(value)
        if name == Variable.CENTRALITY:
            return Pretty.cent(value)
        if name == 'SQRT(S)/NUCLEON':
            return Pretty.sqrts(value,System.AUAU)
        if name == 'SQRT(S)':
            return Pretty.sqrts(value,System.PP)
        if name == 'reaction' or name == "reactions":
            ret =  Pretty.sys(value.split('-->')[0].strip())
            ret += r'$\rightarrow$'
            ret += Pretty.part(value.split('-->')[1].strip())
            #print('Formatting reaction {} -> {}'.format(value,ret))
            return ret
        if name == 'observables' or name == "observable":
            return Pretty.obs(value)
        if name == 'THETA' or name == 'PHI':
            return Pretty.ang(name,value,units)
        if name in Pretty.OBS_MAP:
            return self.observable(name,units,value)
        if name in Pretty.VAR_MAP:
            return self.variable(name,units,value)

        r = r'${}$'.format(self._value(name,value,units))
        #print('Got unknown {} = {} ({}) -> {}'.format(name,value,units,r))
        return r

    def observable(self,name,units=None,value=None):
        """Format an observable (ordinate labels)
        
        Parameters
        ----------
        n : str 
            Name 
        u : str 
            Units 
        
        Returns
        -------
        r : str 
            Formatted string 
        """
        #print(name,units)
        return self._obsvar(name,value,units,Pretty.obs)

    def variable(self,name,units=None,value=None):
        """Format a variable (abscissa labels)
        
        Parameters
        ----------
        name : str 
            Name 
        units : str 
            Units 
        
        Returns
        -------
        r : str 
            Formatted string 
        """
        return self._obsvar(name,value,units,Pretty.var)

    def common(self,n):
        return self.qualifier(n)

    def uncertainty(self,n,main):
        return self.qualifier(n)

    def unit(self,unit):
        return Pretty.unit(unit)

    def qualifier_name(self,name):
        prefix = ''
        if name[:4] == 'sys:':
            prefix = 'Syst.uncer. '
            name = name[4:]
        return prefix+Pretty.qual(name)

    qual = qualifier
    var = variable
    obs = observable
    qname = qualifier_name
#
# EOF
#
