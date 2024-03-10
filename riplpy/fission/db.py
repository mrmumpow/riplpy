# =========================
# -*- coding: utf-8 -*-
"""Python objects that load the fission barrier databases into memory.

Python 3.10+ is expected to run this code properly.

Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

"""

# ========================

# RIPLpy
from . import empirical as _emp
from . import hfb as _hfb

# ========================

__all__ = ('empirical_barriers', 'hfb_barriers')

# ========================

# The experimental fission barrier database
empirical_barriers = _emp.load()

# The theoretical HFB fission barrier database
hfb_barriers = _hfb.load()
