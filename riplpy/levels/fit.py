
# Dataclasses
from dataclasses import dataclass

# RIPLpy
from riplpy.collections import Nuclide

@dataclass
class ConstTempEntry(object):

    n    : Nuclide = None  # Nuclide of the dataset
    T    : float   = None  # Temperature T in the CT model
    dT   : float   = None  # Uncertainty of T
    U0   : float   = None  # Back-shift in CT model
    dU0  : float   = None  # Uncertainty of U0
    Nlev : int     = None  # Number of levels in the ENSDF data set
    Nmax : int     = None  # Maximum level number up to which the level scheme is complete
    N0   : int     = None  # Minimum level number from which the fit is considered
    Nc   : int     = None  # Number of level at which unique spin sequence ends
    Umax : float   = None # Energy corresponds to Nmax
    Uc   : float   = None # Energy corresponds to Nc
    Chi  : float   = None # Measure of the quality of fit (blank if there was no fit)
    Fit  : str     = None # If the record comes from the fit of pre-selected nuclei, which provided the T(A) function = blank if there was no fit
    Flag : str     = None # 'F' if Chi>0.05 (bad fit); blank otherwise
    NoX  : int     = None # Number of levels with +X, +Y, +Z ... notation (X,Y,Z... are unknown energy values)
    Xm   : int     = None # Level number where the first +X, +Y, +Z ... notation appears
    Ex   : float   = None # Level energy where the first +X, +Y, +Z ... notation appears
    sigma: float   = None # Spin cut-off values extracted from the discrete level library


class ConstTemp(object):
    """Constant Temperature (CT) fit of nuclear level schemes. """

    def __init__(self, data: dict = {}) -> None:
        """Initialze the object. """
        self.data = data
