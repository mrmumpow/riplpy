# -*- coding: utf-8 -*-
"""Python objects that provide access to the Finite-Range Droplet Model (FRDM). 

Python 3.10+ is expected to run this code properly.

Examples:
    (1) Load and print the FRDM1995 database::
       $ import riplpy.masses as masses
       $ frdm1995 = masses.frdm95.load() # The FRDM1995 database
       $ print(frdm1995.data)
    (2) Access a particular entry of the mass database using the get method::
       $ from riplpy.collections import Nuclide
       $ n = Nuclide(z=82, a=208)
       $ print(frdm1995.get(n))
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

__all__ = ('db_file_path', 'FILE_HEADER', 'FORTRAN_FORMAT', 'reader', 'writer', 'read_ascii_file', 'write_ascii_file', 'Entry', 'Database', 'load')

# ========================

# Current location
__loc__ = _os.path.dirname(_os.path.realpath(__file__))
# Database location
db_file_path = _os.path.join(__loc__, "data", "mass-frdm95.dat")

# ========================

FILE_HEADER = "#\n#  Z   A s fl     Mexp      Err       Mth      Emic    beta2   beta3   beta4   beta6\n#                [MeV]     [MeV]     [MeV]     [MeV]                                \n#----------------------------------------------------------------------------------------------------\n"
FORTRAN_FORMAT   = '(2i4,1x,a2,1x,i1,4f10.3,4f8.3)'
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
            package = {'n': n, 'flag': data[3], 'Mexp': data[4], 'Err': data[5], 'Mth': data[6], 'Emic': data[7],
                       'beta2': data[8], 'beta3': data[9], 'beta4': data[10], 'beta6': data[11],
                      }
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
    """An entry in the FRDM1995 mass database. """

    n     : _c.Nuclide = None # Compound nucleus
    flag  : int        = None # flag corresponding to:
                              #   0 if no experimental data available
                              #   1  for a mass excess recommended by Audi et al. (2007)
                              #   2 for a measured mass from Audi et al. (2007)
    Mexp  : float      = None # Experimental or recommended atomic mass excess [MeV] of Audi et al. (2007) 
    Err   : float      = None # Error on the experimental or recommended atomic mass excess [MeV] of Audi et al. (2007) 
    Mth   : float      = None # Calculated FRDM atomic mass excess [MeV]
    Emic  : float      = None # Calculated FRDM microscopic energy [MeV]
    beta2 : float      = None # Calculated quadrupole deformation of the nuclear ground-state
    beta3 : float      = None # Calculated octupole deformation of the nuclear ground-state
    beta4 : float      = None # Calculated hexadecapole deformation of the nuclear ground-state
    beta6 : float      = None # Calculated hexacontatetrapole deformation of the nuclear ground-state


class Database(_core.MassDatabase):
    """The FRDM1995 ground state masses database. """

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


def load() -> Database:
    """Load and return the FRDM1995 database. """
    return _db.load(Database, db_file_path)
