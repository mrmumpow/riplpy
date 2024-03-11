# -*- coding: utf-8 -*-
"""Python objects that load discrete level databases into memory.

Python 3.10+ is expected to run this code properly.

Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

"""

# ========================

# RIPLpy
from . import ct as _ct
from . import discrete as _di

# ========================

__all__ = ('discrete_levels', 'constant_temperature')

# ========================

# The entire discrete level database
discrete_levels = _di.load_all()

# The constant temperature fit database
constant_temperature = _ct.load()
