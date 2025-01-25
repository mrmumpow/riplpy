# -*- coding: utf-8 -*-
"""Python objects that provide access to the 2020 Atomic Mass Evaluation (AME2020). 

Python 3.10+ is expected to run this code properly.

Examples:
    (1) Load and print the AME20 database::
       $ import riplpy.masses as masses
       $ ame20 = masses.ame20.load() # The AME20 database
       $ print(ame20.data)
    (2) Access a particular entry of the mass database using the get method::
       $ from riplpy.collections import Nuclide
       $ n = Nuclide(z=82, a=208)
       $ print(ame20.get(n))
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
local_file_path = _os.path.join("masses", "mass-ame20.dat")

# ========================

FILE_HEADER = "#\n#  Z   A s fl     Mexp      Err\n#                 [MeV]    [MeV]\n#----------------------------------\n"
FORTRAN_FORMAT = '(2i4,1x,a2,1x,i1,2f10.3)'
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
                )
                fp.write(writer.write(line) + "\n")
            except Exception as e:
                print(f"Failed to write entry: {entry}. Error: {e}")


@_dataclass
class Entry:
    """An entry in the AME20 mass database."""
    n      : _c.Nuclide  # Compound nucleus
    flag   : int         # Data flag
    Mexp   : float       # Experimental or recommended atomic mass excess [MeV]
    Err    : float       # Error on the experimental or recommended mass excess [MeV]

    @classmethod
    def from_dict(cls, data: dict) -> "Entry":
        """Create an entry from a dictionary."""
        return cls(
            n=data['n'],
            flag=data['flag'],
            Mexp=data['Mexp'],
            Err=data['Err'],
        )


class Database(_core.MassDatabase):
    """The AME2020 ground state masses database. """

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
