
# ========================

# OS
import os as _os

# RIPLpy
import riplpy.masses.db as _db

# ========================

# Current location
__loc__ = _os.path.dirname(_os.path.realpath(__file__))

# ========================

# The FRDM1995 mass model
frdm95 = _db.FRDM95Database()
frdm95.load(_os.path.join(__loc__, "data", "mass-frdm95.dat"))

# The HFB
hfb14  = _db.HFB14Database()
hfb14.load(_os.path.join(__loc__, "data", "mass-hfb14.dat"))

# The natural abundances
ab = _db.NaturalAbundancesDatabase()
ab.load(_os.path.join(__loc__, "data", "abundance.dat"))
