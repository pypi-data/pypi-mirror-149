"""Code to define names for HepData records. 

The classes are 

- Phrase 
  Phrases to use in the submissions file for each table 
- Particle 
  Particle types 
- System 
  Collision systems 
- Unit 
  Units 
- Variable
  Variables (e.g., PT) with optional units 
- Observable 
  Observables (e.g. D2N/DPT/DYRAP) with optional units 
- Pretty 
  Pretty print of the above 
- Beautifier 
  Class to beautify the above 

Constants of each of the classes Phrase, Particle, System, Unit,
Variable, and Observable are registered using the register
method. Each of these methods take at least the name of the constant
to define, the value of the constant, and a pretty-print version of
the value.  

Some (notably Variable and Observable) also accepts a Unit argument to
define the unit of the constant.  The unit argument should be a
constant in the Unit class (i.e., the unit must be registered
before-hand).

Some (again, notably Variable and Observable) also accepts a Phrase
argument to associated phrases with a constant.  This can be used to
automatically associate phrases of a table based on the variables and
observable.  The phrases argument is optional and is either a single
Phrase constant or a list of Phrase constants.

This module does not define any constants in the code.  Instead these
are read from YAML files upon import.

"""
import os
from hepdata.names.pretty import Pretty
from hepdata.names.phrase import Phrase
from hepdata.names.particle import Particle
from hepdata.names.system import System
from hepdata.names.unit import Unit
from hepdata.names.variable import Variable
from hepdata.names.observable import Observable
from hepdata.names.qualifier import Qualifier
from hepdata.names.helper import Helper
from hepdata.names.beautifier import Beautifier

#: Alias for :meth:`Helper.table`
table = Helper.table
#: Alias for :meth:`Helper.independent`
independent = Helper.independent
#: Alias for :meth:`Helper.dependent`
dependent = Helper.dependent
#: Alias for :meth:`Helper.columns`
columns	= Helper.columns
#: Alias for :meth:`Helper.description`
description = Helper.description

def load(fnstr):
    """Load additional definitions from a file. 
        
    The file may contain more information for 
        
    - Particles 
        - name: Symbol to define 
        - value: Value as a string 
        - pretty: Pretty print string 
    - Phrases 
        - name: Symbol to define 
        - value: String value  
    - Units 
        - name: Symbol to define 
        - value: Value as a string 
        - pretty: Pretty print string 
    - Variables 
        - name: Symbol to define 
        - value: Value as a string 
        - pretty: Pretty print string 
        - units (optional): Unit identifier 
        - phrases (optional): A list of phrases
    - Systems 
        - name: Symbol to define 
        - value: Value as a string, or both of 
        - projectile: Particle identifier 
        - target: Particle identifier 
        - pretty (optional): Pretty print string.  Deduced if not given
        - aa (optional): If true, give collision energy per nucleon pair
    - Observables 
        - name: Symbol to define 
        - value: Value as a string 
        - pretty: Pretty print string 
        - units (optional): Unit identifier 
        - phrases (optional): A list of phrases
    - Qualifiers
        - name: symbol to define 
        - value: Value as a string 
        - pretty: Pretty print string 
        
    """
    Particle  .load(fnstr)
    Phrase    .load(fnstr)
    Unit      .load(fnstr)
    Variable  .load(fnstr)
    System    .load(fnstr)
    Observable.load(fnstr)
    Qualifier .load(fnstr)

def _init():
    def _yamlfile(base):
        return os.path.join(os.path.dirname(__file__),'data',base+'.yaml')

    Particle  .register('X','X','X')
    Particle  .load(_yamlfile('parts'))
    Phrase    .load(_yamlfile('phrases'))
    Unit      .load(_yamlfile('units'))
    Variable  .load(_yamlfile('vars'))
    System    .load(_yamlfile('sys'))
    Observable.load(_yamlfile('obs'))
    Qualifier .load(_yamlfile('quals'))


_init()
#
# EOF
#
#

