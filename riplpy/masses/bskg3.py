# -*- coding: utf-8 -*-
"""Python objects that provide access to the BSkG3 mass model database.

Python 3.10+ is expected to run this code properly.

Examples:
    (1) Load and print the BSkG3 database::
       $ import riplpy.masses as masses
       $ bskg3 = masses.bskg3.load() # The BSkG3 database
       $ print(bskg3.data)
    (2) Access a particular entry of the mass database using the get method::
       $ from riplpy.collections import Nuclide
       $ n = Nuclide(z=82, a=208)
       $ print(bskg3.get(n))
    (3) 
Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

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
from . import core as _core

# ========================

__all__ = ('local_file_path', 'FILE_HEADER', 'FORTRAN_FORMAT', 'reader', 'writer', 'read_ascii_file', 'write_ascii_file', 'Entry', 'Database', 'load')

# ========================

# Relative path to database file
local_file_path = _os.path.join("masses", "mass-bskg3.dat")

# ========================

FILE_HEADER = "#\n#  Z   A s fl     Mexp      Err       Mth    beta20  beta22  Gamma  beta30  beta32  beta4    Rch\n#                [MeV]     [MeV]     [MeV]                                                   [fm]\n#----------------------------------------------------------------------------------------------------\n"
FORTRAN_FORMAT = '(2i4,1x,a2,1x,i1,3f10.3,7f8.3)'
reader = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer = _ff.FortranRecordWriter(FORTRAN_FORMAT)

# ========================

def read_ascii_file(fpath: str) -> dict:
    """Read data from an ASCII file and return a dictionary."""
    data_dict = {}

    with open(fpath, 'r') as fp:
        for line in fp.readlines():
            # Skip header or empty lines
            if line.startswith("#") or not line.strip():
                continue
            try:
                data = reader.read(line)
                Z, A = data[0], data[1]
                n = _c.Nuclide(Z=Z, A=A)
                package = {
                    'n': n,
                    'flag': data[3],
                    'Mexp': data[4],
                    'Err': data[5],
                    'Mth': data[6],
                    'beta20': data[7],
                    'beta22': data[8],
                    'Gamma': data[9],
                    'beta30': data[10],
                    'beta32': data[11],
                    'beta4': data[12],
                    'Rch': data[13],
                }
                data_dict[n] = package
            except Exception as e:
                print(f"Failed to parse line: {line.strip()}. Error: {e}")
    return data_dict


def write_ascii_file(fpath: str, data: dict) -> None:
    """Write ASCII file given a filename and a data dictionary."""
    with open(fpath, 'w') as fp:
        # Write the header line
        fp.write(FILE_HEADER)
        for n, entry in data.items():
            try:
                line = (
                    n.Z,
                    n.A,
                    n.symbol,
                    entry['flag'],
                    entry['Mexp'],
                    entry['Err'],
                    entry['Mth'],
                    entry['beta20'],
                    entry['beta22'],
                    entry['Gamma'],
                    entry['beta30'],
                    entry['beta32'],
                    entry['beta4'],
                    entry['Rch'],
                )
                fp.write(writer.write(line) + "\n")
            except Exception as e:
                print(f"Failed to write entry: {entry}. Error: {e}")


@_dataclass
class Entry:
    """An entry in the BSkG3 mass database."""
    n       : _c.Nuclide  # Compound nucleus
    flag    : int         # Data flag
    Mexp    : float       # Experimental or recommended atomic mass excess [MeV]
    Err     : float       # Error on the experimental or recommended mass excess [MeV]
    Mth     : float       # Calculated BSkG3 atomic mass excess [MeV]
    beta20  : float       # Quadrupole deformation
    beta22  : float       # Higher-order quadrupole deformation
    Gamma   : float       # Pairing gap parameter
    beta30  : float       # Octupole deformation
    beta32  : float       # Higher-order octupole deformation
    beta4   : float       # Hexadecapole deformation
    Rch     : float       # Charge radius [fm]

    @classmethod
    def from_dict(cls, data: dict) -> "Entry":
        """Create an entry from a dictionary."""
        return cls(**data)


class Database(_core.MassDatabase):
    """The BSkG3 ground state masses database. """

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


def load(directory: str = None, file_path: str = None) -> Database:
    """Load the database into memeory and return it. """
    if file_path is not None:
        return _db.load(Database, file_path)
    elif directory is not None:
        file_path = _os.path.join(directory, local_file_path)
        return _db.load(Database, file_path)
