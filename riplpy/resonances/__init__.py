"""Average parameters of s- and p-wave neutron resonances.

The average resonance parameters recommended for RIPL-4 were taken from RIPL-3
and Brookhaven National Laboratory (BNL, Mughabghab 2018) and compiled by
S. Goriely (August 2025). Each record provides the recommended values from
both evaluations side-by-side: the average resonance spacing, the average
total radiative width, and the neutron strength function, each with its
quoted uncertainty.

The recommended parameters are given separately for s- and p-wave resonances
in files ``resonances_L0.dat`` and ``resonances_L1.dat`` respectively. The
s-wave file covers 324 nuclides; the p-wave file covers 248 nuclides.

References
----------
S.F. Mughabghab, *Atlas of Neutron Resonances*, Elsevier (2018).
R. Capote *et al.*, *Nuclear Data Sheets* **110**, 3107 (2009).
"""

# ========================

# RIPLpy
from riplpy.db import _DbAccessor

# Local
from . import swave as swave
from . import pwave as pwave

# ========================

db = _DbAccessor()

# ========================

def load(directory: str) -> None:
    """Load the entire database of the Resonances section of RIPL. 

       Once this method is called, the databases cannot be unloaded.
    """
    
    # The s-/p-wave resonance databases
    db.swave = swave.load(directory)
    db.pwave = pwave.load(directory)
