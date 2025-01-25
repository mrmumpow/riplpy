
# RIPLpy
from riplpy.db import _DbAccessor

# Local
from .core import *
from . import gdr
from . import gsf
from . import exp

# ========================

db = _DbAccessor()

# ========================

def load(directory: str) -> None:
    """Load the entire database of the Gamma section of RIPL from a specified directory. 

       Once this method is called, the databases cannot be unloaded.
    """

    # Gamma strength function database
    db.gsf = gsf.load_all(directory)

    # The theoretical GDR parameter database
    db.theory_gdr = gdr.load(directory)

    # The experimental SLO parameter database
    db.experiment_slo = exp.load_slo(directory)
    # The experimental MLO parameter database
    db.experiment_mlo = exp.load_mlo(directory)
