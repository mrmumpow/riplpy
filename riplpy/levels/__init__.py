
# RIPLpy
from riplpy.db import _DbAccessor

# Local
from .core import *
from . import ct as ct
from . import discrete as discrete

# ========================

db = _DbAccessor()

# ========================

def load(directory: str) -> None:
    """Load the entire database of the Levels section of RIPL. 

       Once this method is called, the databases cannot be unloaded.
       Warning: this method can take a long time to complete.
    """
    
    # The entire discrete level database
    db.discrete_levels = discrete.load_all(directory)

    # The constant temperature fit database
    db.constant_temperature = ct.load(directory)

