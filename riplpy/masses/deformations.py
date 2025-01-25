# -*- coding: utf-8 -*-
"""Python objects that provide access to the nuclear deformations.

Python 3.10+ is expected to run this code properly.

Examples:
    (1) Load and print the deformation database::
       $ import riplpy.deformations as deformations
       $ deform_db = deformations.deformation.load() # The deformation database
       $ print(deform_db.data)
    (2) Access a particular entry of the deformation database using the get method::
       $ from riplpy.collections import Nuclide
       $ n = Nuclide(z=92, a=238)
       $ print(deform_db.get(n))
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

__all__ = ('local_file_path', 'FILE_HEADER', 'FORTRAN_FORMAT', 'reader', 'writer', 'read_ascii_file', 'write_ascii_file', 'Entry', 'Database', 'load')

# ========================

# Relative path to database file
local_file_path = _os.path.join("masses", "gs-deformations-exp.dat")

# ========================

FILE_HEADER    = "#      Nuclear Deformations\n#  Z  A  El    beta2      error\n#                [-]      [-]\n#-------------------------------\n"
FORTRAN_FORMAT = '(2i4,1x,a2,1x,2f8.4)'
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
            package = {'n': n, 'beta2': data[3], 'error': data[4]}
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
            fp.write(writer.write(line) + "\n")


@_dataclass
class Entry(_db.NuclideDatabaseEntry):
    """An entry in the deformation database. """

    n      : _c.Nuclide = None # Compound nucleus
    beta2  : float      = None # Experimental deformation parameter
    error  : float      = None # Error on the deformation parameter


class Database(_db.NuclideDatabase):
    """The deformation database. """

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
