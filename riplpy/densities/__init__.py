
# Local
from . import bsfg as bsfg
from . import ct as ct
from . import egsm as egsm
from . import egsm_norm as egsm_norm
from . import shell_corr as shell_corr

def load() -> None:
    """Load the entire database of the Densities section of RIPL. 

       Once this method is called, the databases cannot be unloaded.
    """
    from .db import __all__
