
# Local
from .core import *
from . import frdm as frdm
from . import hfb as hfb
from . import ab as ab

def load() -> None:
    """Load the entire database of the Masses section of RIPL. 

       Once this method is called, the databases cannot be unloaded.
    """
    from .db import __all__
