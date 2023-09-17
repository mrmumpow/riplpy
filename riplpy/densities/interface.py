
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

# The EGSM normalization database
egsm_norm_db = _db.EGSM_NormDatabase()
egsm_norm_db.load(_os.path.join(__loc__, "data", "level-densities-egsm-norm.dat"))

# The shell correction energies database
shell_corr_db = _db.ShellCorrDatabase()
shell_corr_db.load(_os.path.join(__loc__, "data", "shellcor-ms.dat"))
