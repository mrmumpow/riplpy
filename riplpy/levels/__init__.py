
# Local
from .core import *
from . import ct as ct
from . import discrete as discrete

def load() -> None:
    """Load the entire database of the Levels section of RIPL. 

       Once this method is called, the databases cannot be unloaded.
       Warning: this method can take a long time to complete.
    """
    from .db import __all__
