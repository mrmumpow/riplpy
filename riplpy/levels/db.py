# OS
import os as _os

# Collections
from dataclasses import dataclass, field

# Fortran format
import fortranformat as _ff

# RIPLpy
from riplpy.collections import Nuclide
from riplpy.levels import DiscreteNuclearLevel

# ========================

# Current location
__loc__  = _os.path.dirname(_os.path.realpath(__file__))
data_dir = _os.path.join(__loc__, "data")

# ========================

IDENT_FORTRAN_FORMAT = '(a5,6i5,2f12.6)'
#LEVEL_FORTRAN_FORMAT = '(i3,1x,f10.6,1x,f5.1,i3,1x,(e10.3),i3,1x,a1,1x,a4,1x,a18,i3,10(1x,a2,1x,e10.4,1x,a7),f10.6,1x,3(2i))'
#LEVEL_FORTRAN_FORMAT = '(i3,1x,f10.6,1x,f5.1,i3,1x,(1pe10.2),i3,1x,a1,1x,a4,1x,a18,i3,10(1x,a2,1x,0pf10.4,1x,a7))'
LEVEL_FORTRAN_FORMAT = '(i3,1x,f10.6,1x,f5.1,i3,1x,(1pe10.2),i3,1x,a1,1x,a4,1x,a18,i3,10(1x,a2,1x,0pf10.4,1x,a7),f10.6,1x,3(i2))'
GAMMA_FORTRAN_FORMAT = '(39x,i4,1x,f10.3,3(1x,e10.3))'
ident_reader = _ff.FortranRecordReader(IDENT_FORTRAN_FORMAT)
level_reader = _ff.FortranRecordReader(LEVEL_FORTRAN_FORMAT)
gamma_reader = _ff.FortranRecordReader(GAMMA_FORTRAN_FORMAT)

# ========================

def read_identification_record(substr: str) -> list:
    """Read the isotope's identification record. """
    return ident_reader.read(substr)


def read_level_record(substr: str) -> list:
    """Read a level record of the particular isotope. """
    return level_reader.read(substr)


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
class DiscreteLevel(DiscreteNuclearLevel):
    """An object representing a discrete nuclear level. """

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




class Interface(object):
    """An object which interfaces with the RIPL levels database. """
    pass


class DiscreteLevelsDatabase(object):
    """An object which holds the RIPL discrete levels database information. """


    def __init__(self, data: dict = {}) -> None:
        """Initialize a new RIPL discrete levels database. """
        self.data = data # The dictionary which defines the database

    def load_all(self, ) -> None:
        """Read the entire database into memory from many individual ASCII files. """
        # Loop over the element numbers
        #for Z in range(50, 52):
        for Z in range(1, 119):
            fpath = _os.path.join(data_dir, "discrete", f"z{Z:03d}.dat")
            _data = self.read_raw_ascii(fpath)
            _data = self.parse_ascii_dict(_data)
            for entry in _data.keys():
                self.data[entry] = _data[entry]

    def load_element(self, Z: int) -> None:
        """Read the database entry for element with proton number (Z). """
        fpath     = _os.path.join(data_dir, "discrete", f"z{Z:03d}.dat")
        data      = self.read_raw_ascii(fpath)
        self.data = self.parse_ascii_dict(data)

    @classmethod
    def read_raw_ascii(cls, fpath: str) -> None:
        """Read data into the database object from a single ASCII file. """

        # Placeholder for data
        data = {}

        # RIPL discrete level files have no headers
        with open(fpath, 'r') as fp:    
            # Begin reading data directly from the first line
            for line in fp.readlines():
                # Parse the given line
                try:
                    header     = ident_reader.read(line)
                    nucleus    = header[0]
                    num_levels = int(header[3])
                    levels     = []
                    gammas     = {}
                except ValueError:
                    if "                                      " in line[0:40]:
                        # Find appropriate level to attach to
                        lvl = int(level[0])
                        # Parse data
                        gamma = gamma_reader.read(line)
                        gammas[lvl] = gamma
                    else:
                        # Parse data
                        level = level_reader.read(line)
                        levels.append(level)
                # Check if we save data to the dictionary
                if len(levels) == num_levels:
                    data[nucleus] = (header, levels, gammas)

        return data

    @staticmethod
    def parse_ascii_dict(data: dict) -> dict:
        """Parse the dictionary to a more Pythonic friendly representation. """
        
        offset = 3 # Offset used for decay mode information
        
        output = {} # Placeholder for return information

        # Loop over the dictionary keys
        for nucleus in data.keys():
            n = Nuclide.from_string(nucleus)
            header, levels, gammas = data[nucleus]
            # Recast levels into objects
            #levels = [DiscreteLevel(*lvl) for lvl in levels]
            recasted_levels = []
            for lvl in levels:
                e       = float(lvl[1])
                spin    = float(lvl[2])
                parity  = int(lvl[3])
                t12     = float(lvl[4])
                ng      = int(lvl[5])
                jflag   = lvl[6].strip()
                unc     = lvl[7].strip()
                jpistr  = lvl[8].strip()
                n_modes = int(lvl[9])
                modes = []
                for m in range(n_modes):
                    dpm     = lvl[10+m*offset].strip()
                    percent = float(lvl[11+m*offset])
                    mode    = lvl[12+m*offset].strip()
                    modes.append(DecayMode(mode, dpm, percent))
                recasted_levels.append(DiscreteLevel(e, spin, parity, t12, ng, jflag, unc, jpistr, modes))

            # Recast the gammas into objects
            recasted_gammas = {}
            for lvl_id in gammas.keys():
                recasted_gammas[lvl_id] = DiscreteGamma(*gammas[lvl_id])

            # Save for later
            output[n] = DiscreteLevelEntry(n, recasted_levels, recasted_gammas)

        return output

# levels = DiscreteLevelsDatabase()
# levels.load_element(50)
# print(levels.data)

# levels = DiscreteLevelsDatabase()
# levels.load_all()
# print(levels.data)

