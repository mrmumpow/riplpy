# -*- coding: utf-8 -*-
"""Python objects that provide access to the natural abundances. 

Python 3.10+ is expected to run this code properly.

Examples:
    (1) Load and print the natural abundance database::
       $ import riplpy.masses as masses
       $ natab = masses.ab.load() # The natural abundances database
       $ print(natab.data)
    (2) Access a particular entry of the natural abundances database using the get method::
       $ from riplpy.collections import Nuclide
       $ n = Nuclide(z=50, a=120)
       $ print(natab.get(n))
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

# ========================

__all__ = ('db_file_path', 'FILE_HEADER', 'FORTRAN_FORMAT', 'reader', 'writer', 'read_ascii_file', 'write_ascii_file', 'Entry', 'Database', 'load')

# ========================

# Current location
__loc__ = _os.path.dirname(_os.path.realpath(__file__))
# Database location
db_file_path = _os.path.join(__loc__, "data", "abundance.dat")

# ========================

FILE_HEADER = "#      Natural abundances\n#  Z  A  El   abundance  uncert.\n#               [%]       [%]\n#-------------------------------\n"
FORTRAN_FORMAT   = '(2i4,1x,a2,1x,2f10.6)'
reader   = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer   = _ff.FortranRecordWriter(FORTRAN_FORMAT)

# ========================

def read_ascii_file(fpath: str) -> dict:
    """Read data from an ASCII file and return a dictionary. """
    # Placeholder dictionary
    d = {}

    # Read data from file
    with open(fpath, 'r') as fp:
        for i, line in enumerate(fp.readlines()):
            # Skip the header line(s)
            if "#" in line[0]:
                continue
            data  = reader.read(line)
            Z     = data[0]
            A     = data[1]
            n       = _c.Nuclide(Z=Z, A=A)
            package = {'n': n, 'abundance': data[3], 'uncertainty': data[4]}
            d[n] = package
    return d


def write_ascii_file(fpath: str, data: dict) -> None:
    """Write ASCII file given a filename and a data dictionary. """

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
    """An entry in the natural abundances database. """

    n          : _c.Nuclide = None # Compound nucleus
    abundance  : float      = None # Abundance in %
    uncertainty: float      = None # Uncertainties in abundance in %


class Database(_db.NuclideDatabase):
    """The natural abundances database. """

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


def load() -> Database:
    """Load and return the natural abundances database. """
    return _db.load(Database, db_file_path)
