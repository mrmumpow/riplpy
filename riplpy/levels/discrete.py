
# Collections
from dataclasses import dataclass, field

# Numpy
import numpy as _np


# RIPLpy
from riplpy.collections import Nuclide
from riplpy.levels import DiscreteNuclearLevel

# ========================

@dataclass
class DecayMode(object):
    """A representation of a decay mode for the RIPL database. """

    mode      : str   = None # Decay flag as a string
    flag      : str   = None # Decay percentage modifier flag; informs a user about major uncertainties. 
                             # The modifiers are copied out of ENSDF with no modification, and can 
                             # have the following values: =, <, >, ? (unknown, but expected), 
                             # AP (approximate), GE (greater or equal), LE (less or equal), 
                             # LT (less then), SY  (value from systematics)
    percent   : str   = None # Percentage decay of different decay modes



@dataclass
class DiscreteLevelInfo(DiscreteNuclearLevel):
    """An object representing an entry in the discrete nuclear level database. """

    halflife   : float = None # Half-life in [seconds]
    num_gammas : int   = None # Number of gamma-rays de-exciting the level
    jflag      : str   = None # Flag for spin estimation method
    unc        : str   = None # Flag for an uncertain level energy
    jpistr     : str   = None # String representation of spin-parity (original spins from the ENSDF file)
    decay_modes: list  = field(default_factory=list) # Decay modes of the level
    shift      : str   = None # Value assigned to uncertain "X" in an ENSDF level
    band       : int   = None # Integer assigned to band(s) to which the level is part

    @property
    def number_decay_modes(self) -> int:
        """Return the number of decay modes. Returns None for unknown. """
        return len(self.decay_modes)


@dataclass
class DiscreteLevelGammaEntry(DiscreteNuclearLevel):
    """An object representing an entry in the  discrete nuclear level database that also contains associated gamma-rays. """

    halflife   : float = None # Half-life in [seconds]
    jflag      : str   = None # Flag for spin estimation method
    unc        : str   = None # Flag for an uncertain level energy
    jpistr     : str   = None # String representation of spin-parity (original spins from the ENSDF file)
    gammas     : dict  = field(default_factory=dict) # Associated gamma-rays with this level
    decay_modes: list  = field(default_factory=list) # Decay modes of the level
    shift      : str   = None # Value assigned to uncertain "X" in an ENSDF level
    band       : int   = None # Integer assigned to band(s) to which the level is part

    @property
    def number_decay_modes(self, ) -> int:
        """Return the number of decay modes. Returns None for unknown. """
        return len(self.decay_modes)
    
    @property
    def number_gammas(self, ) -> int:
        """Return the number of gamma-rays associated with the de-excitation of this nuclear level. """
        return len(self.gammas)


@dataclass
class DiscreteGamma(object):
    """An object representing a gamma-ray from a discrete nuclear level. """

    to_level_numer: int   = None # Final level number (unique integer in associated DiscreteLevel list)
    energy        : float = None # Energy, typically in [MeV]
    prob_g        : float = None # Probability that the level decays through photon (gamma ray) emission
    prob_em       : float = None # Probability of the electromagnetic transition (photon, conversion electron, pair creation)
                                 # The sum of the Pe gives the IT (electromagnetic transition) branching ratio of the level
                                 # This is 1 unless other decay modes are listed in the level record (see example below)
    cc            : float = None # Internal conversion coefficient of the transition
                                 # Pe, Pg, and ICC are in the following relation:
                                 # Pe = Pg * (1 + ICC)


@dataclass
class DiscreteLevelEntry(object):
    """Object which represents an entry in the DiscreteLevelsDatabase. """

    nucleus: Nuclide = None
    levels: list = field(default_factory=list) # Order matters
    gammas: dict = field(default_factory=dict) # Order matters


    @property
    def num_levels(self, ) -> int:
        return len(self.levels)

    @property
    def level_energies(self, ) -> list:
        """Return a list of the level energies. """
        return [lvl.energy for lvl in self.levels]


class DiscreteLevels(object):
    """An object which holds the RIPL discrete levels information. """


    def __init__(self, data: dict = {}) -> None:
        """Initialize a new RIPL discrete levels object. """
        self.data = data # The dictionary which defines the data

    def entry(self, n: Nuclide) -> object:
        """Return the database entry for the requested nucleus. """
        try:
            return self.data[n]
        except KeyError:
            return None

    def levels(self, n: Nuclide) -> object:
        """Return the levels for the particular nuclide in the database. """
        try:
            return self.data[n].levels
        except KeyError:
            return []

    @property
    def levels_dict(self, ) -> dict:
        """Return the levels in the current database as a dictionary accessible by the nucleus. """
        d = {}
        for n in self.data.keys():
            d[n] = self.data[n].levels
        return d

    @property
    def levels_list(self, ) -> list:
        """Return the levels in the current database as a list (independent of the nuclei). """
        lst = []
        for n in self.data.keys():
            for lvl in self.data[n].levels:
                lst.append(lvl)
        return lst

    def insert_level(self, n: Nuclide, new_level: DiscreteLevelInfo) -> None:
        """Insert a new level into the database for the provided nuclide. """
        # Check if nucleus is already in the database
        if n in self.data.keys():
            # Nucleus is in the database
            # Grab existing energies
            energies = [x.energy for x in self.levels(n)]
            # Check if the level is already in the database via the energy of the level
            new_energy = new_level.energy
            if new_level.energy in energies:
                # Replace the existing level with the new level
                i = energies.index(new_energy)
                self.data[n].levels[i] = new_level
            else:
                # Find the nearest energy level and insert there
                i = _np.argmin(_np.abs(new_level.energy - _np.array(energies)))
                self.data[n].levels.insert(i, new_level)
        else:
            # We can easily add since the nucleus is not in the database
            self.data[n] = DiscreteLevelEntry(n, new_level, [])
