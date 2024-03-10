# -*- coding: utf-8 -*-
"""Python objects that load the gamma databases into memory.

Python 3.10+ is expected to run this code properly.

Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

"""

# ========================

# RIPLpy
from . import gdr as _gdr
from . import slo as _slo

# ========================

__all__ = ('theory_gdr', 'experiment_slo')

# ========================

# The theoretical GDR parameter database
theory_gdr = _gdr.load()

# The experimental SLO parameter database
experiment_slo = _slo.load()
