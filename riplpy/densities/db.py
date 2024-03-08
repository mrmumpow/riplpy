
# The pre-loaded databases

# ========================

# RIPLpy
from . import bsfg as _bsfg
from . import ct as _ct
from . import egsm as _egsm
from . import egsm_norm as _egsm_norm
from . import shell_corr as _shell_corr

# ========================

# Imports
__all__ = ('bsfg', 'ct', 'egsm', 'egsm_norm', 'shellcorr_ms', 'shellcorr_mk')

# ========================

# The BSFG level density database
bsfg = _bsfg.load()

# The CT level density database
ct = _ct.load()

# The EGSM database
egsm = _egsm.load()

# The EGSM normalization database
egsm_norm = _egsm_norm.load()

# The shell correction energies databases
shellcorr_ms = _shell_corr.load_ms()
shellcorr_mk = _shell_corr.load_mk()
