# -*- coding: utf-8 -*-
"""Python objects that load the mass databases into memory.

Python 3.10+ is expected to run this code properly.

Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

"""

# ========================

# RIPLpy
from . import ame20
from . import bskg3
from . import d1m
from . import frdm95
from . import frdm12
from . import hfb14
from . import hfb27
from . import ab

# ========================

__all__ = ('ame20', 'bskg3', 'd1m', 'frdm1995', 'frdm2012', 'hfb14', 'hfb27', 'natab')

# ========================

# AME2020 mass evaluation
ame20 = ame20.load()

# BSkG3 mass database
bskg3 = bskg3.load()

# D1M mass database
d1m = d1m.load()

# FRDM1995 mass database
frdm1995 = frdm95.load()

# FRDM2012 mass database
frdm2012 = frdm12.load()

# HFB14 mass database
hfb14 = hfb14.load()

# HFB27 mass database
hfb27 = hfb27.load()

# Natural abundance database
natab = ab.load()
