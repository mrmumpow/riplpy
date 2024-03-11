
# Local
from .core import *
from . import empirical
from . import hfb

_ripl_versions_ = ('3', )

saddle_shorthand = {'S' : 'symmetric',
                    'GA': 'axially asymmetric (triaxial)',
                    'MA': 'mass asymmetric',
                    '  ': '',
                   }

# ========================

def load() -> None:
    """Load the entire database of the Gamma section of RIPL. 

       Once this method is called, the databases cannot be unloaded.
    """
    from .db import __all__
