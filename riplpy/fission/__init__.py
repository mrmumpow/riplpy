
# RIPLpy
from riplpy.db import _DbAccessor

# Local
from .core import *
from . import empirical as emp
from . import hfb

# ========================

_ripl_versions_ = ('3', )


saddle_shorthand = {'S' : 'symmetric',
                    'GA': 'axially asymmetric (triaxial)',
                    'MA': 'mass asymmetric',
                    '  ': '',
                   }

db = _DbAccessor()

# ========================

def load(directory: str) -> None:
    """Load the entire database of the Fission section of RIPL from a specified directory. 

       Once this method is called, the databases cannot be unloaded.
    """

    # The experimental fission barrier database
    db.empirical_barriers = emp.load(directory=directory)

    # The theoretical HFB fission barrier database
    db.hfb_barriers = hfb.load(directory=directory)
