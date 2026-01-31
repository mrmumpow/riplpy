
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
from . import density_bskg3 as density_bskg3
from . import density_d1m as density_d1m
from . import deformations as deformations

# ========================

db = _DbAccessor()

# ========================

# Model map: user-friendly name -> (db attribute name, mass excess field name)
# This allows users to use shorthand names like 'frdm12' instead of 'frdm2012'
MASS_MODELS = {
    'ame20': ('ame20', 'Mexp'),
    'frdm12': ('frdm2012', 'Mth'),
    'frdm2012': ('frdm2012', 'Mth'),
    'frdm95': ('frdm1995', 'Mth'),
    'frdm1995': ('frdm1995', 'Mth'),
    'hfb14': ('hfb14', 'Mth'),
    'hfb27': ('hfb27', 'Mth'),
    'bskg3': ('bskg3', 'Mth'),
    'd1m': ('d1m', 'Mth'),
}

# ========================

def load_only_masses(directory: str) -> None:
    """Loads only the mass database of the Masses section of RIPL. 

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


def load(directory: str) -> None:
    """Load the entire database of the Masses section of RIPL. 

       Once this method is called, the databases cannot be unloaded.
    """
    # Load masses
    load_only_masses(directory)

    # Natural abundance database
    db.natab = ab.load(directory)

    # Density BSKG3
    db.density_bskg3 = density_bskg3.load_all(directory)
    
    # Density D1M
    db.density_d1m = density_d1m.load_all(directory)

    # Ground state deformations
    db.deformations = deformations.load(directory)
