
# ========================

# Dataclass
from dataclasses import dataclass

# ========================

_ripl_versions_ = ('3', )

saddle_shorthand = {'S' : 'symmetric',
                    'GA': 'axially asymmetric (triaxial)',
                    'MA': 'mass asymmetric',
                   }

# ========================

@dataclass
class ParabolicBarrier(object):
    """An object which represents a single (parabolic) fission barrier defined by a height and curvature. """

    height    : float = None# Generally in [MeV]
    curvature : float = None # Generally in [MeV]


@dataclass
class ParabolicBarrierWithInfo(ParabolicBarrier):
    """An object which represents a parabolic barrier with additional information. """

    sp_sym: str   = None # Saddle point symmetry [one of saddle_shorthand keys]


@dataclass
class ParabolicBarrierWithTheory(object):
    """An object which represents a parabolic barrier with additional theoretical information about the nuclear level density at the saddle configuration. """

    height   : float = None # Generally in [MeV]
    curvature: float = None # Generally in [MeV]
    alpha    : float = None # Renormalization factor for the NLD at the outer saddle point [MeV^(-1/2)]
    delta    : float = None # Renormalization factor for the NLD at the outer saddle point [MeV]


@dataclass
class TwoParabolicBarriers(object):
    """An object which represents a double-hump (parabolic) fission barrier. 

    The second barrier is optional; it may or may not be given.
    """

    A: ParabolicBarrier = None
    B: ParabolicBarrier = None


@dataclass
class ThreeParabolicBarriers(TwoParabolicBarriers):
    """An object which represents a triple-hump (parabolic) fission barrier. """

    C: ParabolicBarrier = None


@dataclass
class DoubleHumpBarrier(TwoParabolicBarriers):
    """An object which represents a double-hump (parabolic) fission barrier. 

    This object also contains information regarding the pairing correlation function
    """

    deltaf: float = None # Pairing correlation function for saddle points used for fission level density calculation in [MeV]
