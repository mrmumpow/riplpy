
# RIPLpy
from riplpy.db import _DbAccessor

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

# ========================

db = _DbAccessor()

# ========================

def load(directory: str) -> None:
    """Load the entire database of the Masses section of RIPL. 

       Once this method is called, the databases cannot be unloaded.
    """
    # AME2020 mass evaluation
    db.ame20 = ame20.load(directory)

    # BSkG3 mass database
    db.bskg3 = bskg3.load(directory)

    # D1M mass database
    db.d1m = d1m.load(directory)

    # FRDM1995 mass database
    db.frdm1995 = frdm95.load(directory)

    # FRDM2012 mass database
    db.frdm2012 = frdm12.load(directory)

    # HFB14 mass database
    db.hfb14 = hfb14.load(directory)

    # HFB27 mass database
    db.hfb27 = hfb27.load(directory)

    # Natural abundance database
    db.natab = ab.load(directory)
