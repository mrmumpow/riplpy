
# RIPLpy
from riplpy.db import _DbAccessor

# Local
from .core import *
from . import bskg3 as bskg3
from . import empirical as emp
from . import empirical_new as emp_new
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
    db.empirical_barriers     = emp.load(directory)
    db.empirical_barriers_new = emp_new.load(directory)

    # The theoretical BSKG3 fission barrier database
    db.bskg3_barriers = bskg3.load(directory)

    # The theoretical HFB fission barrier database
    db.hfb_barriers = hfb.load(directory)
