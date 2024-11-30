
# Local
from .core import *
from . import ame20 as ame20
from . import bskg3 as bskg3
from . import d1m as d1m
from . import frdm12 as frdm12
from . import frdm95 as frdm95
from . import hfb14 as hfb14
from . import hfb27 as hfb27
from . import ws4 as ws4
from . import ab as ab

def load() -> None:
    """Load the entire database of the Masses section of RIPL. 

       Once this method is called, the databases cannot be unloaded.
    """
    from .db import __all__
