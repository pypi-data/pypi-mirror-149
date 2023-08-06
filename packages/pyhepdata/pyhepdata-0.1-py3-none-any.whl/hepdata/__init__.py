"""Package for creating HEPData submissions

The main entry point here is the :class:`hepdata.Submission`

Copyright 2019 Christian Holm Christensen
"""

from hepdata.rounder      import Rounder
from hepdata.value        import Value
from hepdata.bin          import Bin
from hepdata.column       import Column
from hepdata.independent  import Independent
from hepdata.dependent    import Dependent
from hepdata.table        import Table
from hepdata.meta         import Meta
from hepdata.submission   import Submission
from hepdata.propagator   import Propagator

#: alias for :meth:`Submission.__init__`
submission = Submission

#
# EOF
#
