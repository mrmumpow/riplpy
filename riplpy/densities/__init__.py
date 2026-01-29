
# RIPLpy
from riplpy.db import _DbAccessor

# Local
from . import bsfg as bsfg
from . import ct as ct
from . import egsm as egsm
from . import egsm_norm as egsm_norm
from . import shell_corr as shell_corr
from . import hfb as hfb

# ========================

db = _DbAccessor()

# ========================

def load(directory: str) -> None:
    """Load the entire database of the Densities section of RIPL from a specified directory.

       Once this method is called, the databases cannot be unloaded.
    """

    # The BSFG level density database
    db.bsfg = bsfg.load(directory=directory)

    # The CT level density database
    db.ct = ct.load(directory=directory)

    # The EGSM database
    db.egsm = egsm.load(directory=directory)

    # The EGSM normalization database
    db.egsm_norm = egsm_norm.load(directory=directory)

    # The shell correction energies databases
    db.shellcorr_ms = shell_corr.load_ms(directory=directory)
    db.shellcorr_mk = shell_corr.load_mk(directory=directory)

    # The HFB level density database (spin-dependent)
    db.hfb = hfb.load_all(directory=directory)

