

# Code version 
__version__ = "0.0.1"

# Local
from . import densities
from . import fission
from . import gamma
from . import levels
from . import masses
from . import resonances


def load() -> None:
    """Load the entire RIPL database. 

       Once this method is called, the databases cannot be unloaded.
    """
    densities.load()
    fission.load()
    gamma.load()
    levels.load()
    masses.load()
    resonances.load()
