
# OS
import os as _os

# Fortran format
import fortranformat as _ff

# Numpy
import numpy as _np

# RIPLpy
from riplpy.collections import Nuclide
import riplpy.levels.discrete as _discrete
import riplpy.levels.fit as _fit

# ========================

# Current location
__loc__  = _os.path.dirname(_os.path.realpath(__file__))
data_dir = _os.path.join(__loc__, "data")

# ========================

IDENT_FORTRAN_FORMAT = '(a5,6i5,2f12.6)'
LEVEL_FORTRAN_FORMAT = '(i3,1x,f10.6,1x,f5.1,i3,1x,(1pe10.2),i3,1x,a1,1x,a4,1x,a18,i3,10(1x,a2,1x,0pf10.4,1x,a7),f10.6,1x,3(i2))'
GAMMA_FORTRAN_FORMAT = '(39x,i4,1x,f10.3,3(1x,e10.3))'
CONST_FORTRAN_FORMAT = '(2i4,1x,a2,4(1x,f9.5),4i4,1x,f8.5,1x,f8.5,(1x,e10.3),1x,A1,1x,A1,2i4,f7.4,1x,f6.3)'
ident_reader = _ff.FortranRecordReader(IDENT_FORTRAN_FORMAT)
level_reader = _ff.FortranRecordReader(LEVEL_FORTRAN_FORMAT)
gamma_reader = _ff.FortranRecordReader(GAMMA_FORTRAN_FORMAT)
const_reader = _ff.FortranRecordReader(CONST_FORTRAN_FORMAT)

# ========================

def read_identification_record(substr: str) -> list:
    """Read the isotope's identification record. """
    return ident_reader.read(substr)


def read_level_record(substr: str) -> list:
    """Read a level record of the particular isotope. """
    return level_reader.read(substr)

# ========================

class DiscreteLevelsDatabase(_discrete.DiscreteLevels):
    """An object that can load and store discrete level information."""

    def load_all(self, ) -> None:
        """Read the entire database into memory from many individual ASCII files. """
        # Loop over the element numbers
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
                    modes.append(_discrete.DecayMode(mode, dpm, percent))
                recasted_levels.append(_discrete.DiscreteLevelInfo(e, spin, parity, t12, ng, jflag, unc, jpistr, modes))

            # Recast the gammas into objects
            recasted_gammas = {}
            for lvl_id in gammas.keys():
                recasted_gammas[lvl_id] = _discrete.DiscreteGamma(*gammas[lvl_id])

            # Save for later
            output[n] = _discrete.DiscreteLevelEntry(n, recasted_levels, recasted_gammas)

        return output


class ConstTempDatabase(_fit.ConstTemp):
    """A database holding information on the constant temperature (CT) fit of nuclear level schemes. """

    def load(self, filename: str) -> None:
        """Load the database from ASCII file. """
        d = {}
        with open(filename, 'r') as fp:
            for line in fp.readlines():
                # Skip header lines
                if "#" in line[0]:
                    continue
                info = const_reader.read(line)
                Z    = info[0]
                A    = info[1]
                n    = Nuclide(Z=Z, A=A)
                # sym  = info[2]
                # T    = info[3]  # Temperature T in the CT model
                # dT   = info[4]  # Uncertainty of T
                # U0   = info[5]  # Back-shift in CT model
                # dU0  = info[6]  # Uncertainty of U0
                # Nlev = info[7]  # Number of levels in the ENSDF data set
                # Nmax = info[8]  # Maximum level number up to which the level scheme is complete
                # N0   = info[9]  # Minimum level number from which the fit is considered
                # Nc   = info[10]  # Number of level at which unique spin sequence ends
                # Umax = info[11] # Energy corresponds to Nmax
                # Uc   = info[12] # Energy corresponds to Nc
                # Chi  = info[13] # Measure of the quality of fit (blank if there was no fit)
                # Fit  = info[14] # If the record comes from the fit of pre-selected nuclei, which provided the T(A) function = blank if there was no fit
                # Flag = info[15] # 'F' if Chi>0.05 (bad fit); blank otherwise
                # NoX  = info[16] # Number of levels with +X, +Y, +Z ... notation (X,Y,Z... are unknown energy values)
                # Xm   = info[17] # Level number where the first +X, +Y, +Z ... notation appears
                # Ex   = info[18] # Level energy where the first +X, +Y, +Z ... notation appears
                # sigma= info[19] # Spin cut-off values extracted from the discrete level library
                inputs = info[3:]
                inputs.insert(0, n)
                d[n] = _fit.ConstTempEntry(*inputs)
        self.data = d

    def load_numpy(self, filename: str) -> _np.array:
        """"""
        lst = []
        with open(filename, 'r') as fp:
            for line in fp.readlines():
                # Skip header lines
                if "#" in line[0]:
                    continue
                lst.append(const_reader.read(line))
        return _np.array(lst)

# levels = DiscreteLevelsDatabase()
# levels.load_element(50)
# print(levels.data)

# levels = DiscreteLevelsDatabase()
# levels.load_all()
# print(levels.data)

# ct = ConstTempDatabase()
# ct.load("data/levels-param.data")
# print(ct.data)
