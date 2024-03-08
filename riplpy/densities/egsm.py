# Enhanced Generalized Superfluid Model (EGSM)

"""
Level density parameters for the Enhanced Generalized Superfluid Model, 
which combines the superfluid model below BCS critical energy and  the
Fermi gas model above. The spin distribution in the Fermi gas part is
calculated by reducing excitation energy by subtracting rotational energy.
Nuclear deformation is used to determine the latter. EGSM
takes into account collective enhancement of nuclear level densities
in addition to shell and superfluid effects. The parameters were
obtained by fitting the corresponding model formulas to the RIPL-3
recommended spacings of s-wave neutron resonances.  Matching of the
level densities to the low-lying levels must be performed by the user. 
To this end, a dedicated option is provided in the EGSM code.

Quantities Sym, Io, Bn, Do, dDo, Esh, +da, and -da are only provided 
for convenience and are not used in the calculations. The EGSM code
reads shell corrections, nuclear deformations, and neutron bindings
directly from the respective RIPL files.
"""

# Example usage:
# d = read_ascii_file("data/level-densities-egsm.dat")
# print(d)

# ========================

# OS
import os as _os

# Dataclasses
from dataclasses import dataclass as _dataclass

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.db as _db
import riplpy.collections as _c

# ========================

__all__ = ('db_file_path', 'FILE_HEADER', 'FORTRAN_FORMAT', 'reader', 'writer', 'read_ascii_file', 'write_ascii_file', 'Entry', 'Database', 'load')

# ========================

# Current location
__loc__ = _os.path.dirname(_os.path.realpath(__file__))

db_file_path = _os.path.join(__loc__, "data", "level-densities-egsm.dat")

# ========================

FILE_HEADER = "#           Level density parameters for the EGSM model\n#  Z  A  Sym Io   Bn       Do            dDo           Esh          +da      a       -da   \n#                [MeV]    [keV]         [keV]         [MeV]         [1/MeV] [1/MeV] [1/MeV]\n#-----------------------------------------------------------------------------------------------------"
FORTRAN_FORMAT = '(2(i3,1x),a2,2x,f3.1,1x,f6.3,3(1x,e13.5),3(f8.4))'
reader = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer = _ff.FortranRecordWriter(FORTRAN_FORMAT)

# ========================

def read_ascii_file(fpath: str) -> dict:
    """Read Enhanced Generalized Superfluid Model (EGSM) data from an ASCII formatted file and return as a dictionary. """

    # Placeholder dictionary
    d = {}

    # Read data from file
    with open(fpath, 'r') as fp:
        for i, line in enumerate(fp.readlines()):
            # Skip the header line(s)
            if "#" in line[0]:
                continue
            data  = reader.read(line)
            Z       = data[0]
            A       = data[1]
            n       = _c.Nuclide(Z=Z, A=A)
            package = {'n': n, 'Io': data[3], 'Bn': data[4], 'Do': data[5], 'Derr': data[6], 
                       'Esh': data[7], 'dap': data[8], 'a': data[9], 'dam': data[10],
                      }
            d[n] = package
    return d


def write_ascii_file(fpath: str, data: dict) -> None:
    """Write a Enhanced Generalized Superfluid Model (EGSM) ASCII file given a filename and a data dictionary. """

    # Write data to file
    with open(fpath, 'w') as fp:
        # Write header line
        fp.write(FILE_HEADER)
        # Loop over data
        for n in data.keys():
            line = data[n].as_tuple
            fp.write(writer.write(line)+"\n")


@_dataclass
class Entry(_db.NuclideDatabaseEntry):
    """An entry in the Enhanced Generalized Superfluid Model (EGSM) database. """
   
    n   : _c.Nuclide = None # Compound nucleus
    Io  : float      = None # Spin of the ground state of the target nucleus
    Bn  : float      = None # Neutron binding energy of the compound nucleus [MeV]
    Do  : float      = None # Experimental S-wave resonance spacing [eV or MeV?]
    Derr: float      = None # Uncertainty of the resonance spacing [eV or MeV?] # Changed from original dDo to be consistent
    Esh : float      = None # Shell correction used for estimation of the level density parameter [MeV?]
    dap : float      = None # Upper uncertainty of the level density parameter 'a' at neutron binding energy Bn, corresponding to the 'Do - Derr' spacing of S-wave resonances
    a   : float      = None # Level density parameter 'a' at the neutron binding energy Bn
    dam : float      = None # Lower uncertainty of the level density parameter 'a' at neutron binding energy Bn, corresponding to the 'Do + Derr' spacing of S-wave resonances


class Database(_db.NuclideDatabase):
    """The database object for the Enhanced Generalized Superfluid Model (EGSM) level density model. """

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


def load() -> Database:
    """Load the database into memeory and return it. """
    return _db.load(Database, db_file_path)
