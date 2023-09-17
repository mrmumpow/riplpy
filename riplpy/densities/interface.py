
# The pre-loaded databases

# ========================

# OS
import os as _os

# RIPLpy
import riplpy.densities.db as _db

# ========================

# Current location
__loc__ = _os.path.dirname(_os.path.realpath(__file__))

# ========================

# The BSFG level density database
bsfg_db = _db.BSFG_Database()
bsfg_db.load(_os.path.join(__loc__, "data", "level-densities-bfmeff.dat"))

# The CT level density database
ct_db = _db.CT_Database()
ct_db.load(_os.path.join(__loc__, "data", "level-densities-ctmeff.dat"))

# The EGSM database
egsm_db = _db.EGSM_Database()
egsm_db.load(_os.path.join(__loc__, "data", "level-densities-egsm.dat"))
