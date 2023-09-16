
# RIPLpy
from riplpy.collections import Nuclide

# ========================

class GammaStrengthFunction(object):
    """A representation of the gamma-ray strength function (GSF) for atomic nuclei. """

    n     : Nuclide # The nucleus associated with the GSF
    energy: list    # The excitation energy in the nucleus [MeV]
    fE1   : list    # The E1 strength function in [mb/MeV]
