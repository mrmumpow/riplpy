
"""
Normalization factors that can be applied to the level density parameter 'a' 
to improve precision of the global systematics. These factors were obtained
for 83 individual elements (8<Z<99) by calculating ratio between experimental 
and systematics' value of 'a' at neutron binding and averaging these ratios 
over the whole isotopic chain. The factors are intended to be used for nuclei 
for which there is no experimental value for S-wave resonance spacing (otherwise 
EGSM code normalizes systematics to reproduce experimental 'a' as given in the 
file 'level-densities-egsm.dat'). 

The average (over Z) value of the normalization factor is 1.00 +- 0.06 (one
standard deviation).
"""

# ========================

# OS
import os as _os

# Dataclasses
from dataclasses import dataclass as _dataclass

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.collections as _c
import riplpy.db as _db

# ========================

__all__ = ('local_file_path', 'FILE_HEADER', 'FORTRAN_FORMAT', 'reader', 'writer', 'read_ascii_file', 'write_ascii_file', 'Entry', 'Database', 'load')

# ========================

# Relative path to database file
local_file_path = _os.path.join("densities", "level-densities-egsm-norm.dat")

# ========================

FILE_HEADER = "# Normalization factors for the level density parameter in the EGSM \n# a_exp/a_sys ratio averaged over isotopes of an element\n#  Z   factor\n#------------------------------------------------------------------------\n"
FORTRAN_FORMAT = '(i5,f8.4)'
reader = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer = _ff.FortranRecordWriter(FORTRAN_FORMAT)

# ========================

def read_ascii_file(fpath: str) -> dict:
    """Read Enhanced Generalized Superfluid Model (EGSM) normalization data from an ASCII formatted file and return as a dictionary. """

    # Placeholder dictionary
    d = {}

    # Read data from file
    with open(fpath, 'r') as fp:
        for i, line in enumerate(fp.readlines()):
            # Skip the header line(s)
            if "#" in line[0]:
                continue
            data = reader.read(line)
            ele    = _c.Element(Z=data[0])
            package = {'element': ele, 'factor': data[1],
                      }
            d[ele] = package
    return d


def write_ascii_file(fpath: str, data: dict) -> None:
    """Write a Enhanced Generalized Superfluid Model (EGSM) normalization ASCII file given a filename and a data dictionary. """

    # Write data to file
    with open(fpath, 'w') as fp:
        # Write header line
        fp.write(FILE_HEADER)
        # Loop over data
        for n in data.keys():
            line = data[n].as_tuple
            fp.write(writer.write(line)+"\n")


@_dataclass
class Entry(_db.DatabaseEntry):
    """An entry in the Enhanced Generalized Superfluid Model (EGSM) normalization database. """
   
    element: _c.Element = None # Element
    factor : float      = None # Normalization factor

    @property
    def Z(self, ) -> int:
        return self.element.Z

    @property
    def sym(self, ) -> str:
        return self.element.sym

    @property
    def symbol(self, ) -> str:
        return self.element.symbol

    @property
    def name(self, ) -> str:
        return self.element.name

    @property
    def as_tuple(self, ) -> tuple:
        return tuple([self.Z, self.factor])


class Database(_db.NuclideDatabase):
    """The database object for the Enhanced Generalized Superfluid Model (EGSM) level density model. """

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


def load(directory: str = None, file_path: str = None) -> Database:
    """Load the database into memory and return it. """
    if file_path is not None:
        return _db.load(Database, file_path)
    elif directory is not None:
        file_path = _os.path.join(directory, local_file_path)
        return _db.load(Database, file_path)
