
# Local
from . import gdr
from . import slo

def load() -> None:
    """Load the entire database of the Gamma section of RIPL. 

       Once this method is called, the databases cannot be unloaded.
    """
    from .db import __all__
