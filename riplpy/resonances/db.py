# -*- coding: utf-8 -*-
"""Python objects that load the gamma databases into memory.

Python 3.10+ is expected to run this code properly.

Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

"""

# ========================

# RIPLpy
from . import pwave as _pwave
from . import swave as _swave

# ========================

__all__ = ('swave_db', 'pwave_db')

# ========================

# The s-/p-wave resonance databases
swave_db = _swave.load()
pwave_db = _pwave.load()
