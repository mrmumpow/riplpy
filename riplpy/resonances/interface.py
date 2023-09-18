
# ========================

# OS
import os as _os

# RIPLpy
import riplpy.resonances.db as _db

# ========================

# Current location
__loc__ = _os.path.dirname(_os.path.realpath(__file__))

# ========================

# The s-/p-wave resonance databases
swave_db = _db.SwaveDatabase()
swave_db.load(_os.path.join(__loc__, "data", "resonances0.dat"))
pwave_db = _db.PwaveDatabase()
pwave_db.load(_os.path.join(__loc__, "data", "resonances1.dat"))
