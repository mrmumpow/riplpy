
# ========================

# OS
import os as _os

# RIPLpy
import riplpy.optical.db as _db

# ========================

# Current location
__loc__ = _os.path.dirname(_os.path.realpath(__file__))

# ========================

# The optical model deformation database
omp_deform_db = _db.DeformationDatabase()
omp_deform_db.load(_os.path.join(__loc__, "data", "om-deformations.dat"))
