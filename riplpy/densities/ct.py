# -*- coding: utf-8 -*-
"""Python objects that provide access to the Constant Temperature (CT) level density model. 

Python 3.10+ is expected to run this code properly.

Examples:
    (1) Load and print the CT level density database::
       $ import riplpy.densities as dens
       $ ct = dens.ct.load() # The CT level density database
       $ print(ct.data)
    (2) Access a particular entry of the CT level density database using the get method::
       $ from riplpy.collections import Nuclide
       $ n = Nuclide(z=17, a=36)
       $ print(ct.get(n))
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

# Local Namespace
from . import bsfg as _bsfg

# ========================

__all__ = ('local_file_path', 'FILE_HEADER', 'FORTRAN_FORMAT', 'reader', 'writer', 'read_ascii_file', 'write_ascii_file', 'Entry', 'Database', 'load')

# Relative path to database file
local_file_path = _os.path.join("densities", "level-densities-ctmeff.dat")

# ========================

FILE_HEADER = "   Z  A  El   I0    Bn       D0        Derr    Nlow  Ulow   Ntop  Utop      dW      gamma      ainf     aerr    pairing   Ematch      E0         T\n"
FORTRAN_FORMAT   = '(2i4,1x,a2,1x,f4.1,2x,f6.3,1x,1pe10.3,1x,1pe10.3,0p,1x,i3,2x,f6.3,2x,i3,2x,f6.3,3f10.5,f8.3,4f10.5)'
reader   = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer   = _ff.FortranRecordWriter(FORTRAN_FORMAT)

# ========================

def read_ascii_file(fpath: str) -> dict:
    """Read Constant Temperature (CT) data from an ASCII file and return a dictionary. """
    # Placeholder dictionary
    d = {}

    # Skip this many header lines
    skiprows = 1

    # Read data from file
    with open(fpath, 'r') as fp:
        for i, line in enumerate(fp.readlines()):
            # Skip the header line(s)
            if i < skiprows:
                continue
            data  = reader.read(line)
            Z       = data[0]
            A       = data[1]
            n       = _c.Nuclide(Z=Z, A=A)
            package = {'n': n, 'Io': data[3], 'Bn': data[4], 'Do': data[5], 'Derr': data[6], 'Nlow': data[7], 'Ulow': data[8],
                       'Ntop': data[9], 'Utop': data[10], 'dW': data[11], 'gamma': data[12], 'ainf': data[13], 'aerr': data[14],
                       'pairing': data[15], 'Ematch': data[16], 'E0': data[17], 'T': data[18],
                      }
            d[n] = package
    return d


def write_ascii_file(fpath: str, data: dict) -> None:
    """Write a Constant Temperature (CT) ASCII file given a filename and a data dictionary. """

    # Write data to file
    with open(fpath, 'w') as fp:
        # Write header line
        fp.write(FILE_HEADER)
        # Loop over data
        for n in data.keys():
            #line = (n.Z, n.A, n.sym, data[n].Io, data[n].Bn, data[n].Do, data[n].Derr, data[n].Nlow, data[n].Ulow, data[n].Ntop, data[n].Utop, data[n].dW, data[n].gamma, data[n].ainf, data[n].aerr, data[n].pairing, data[n].Ematch, data[n].E0, data[n].T)
            line = data[n].as_tuple
            fp.write(writer.write(line)+"\n")


@_dataclass
class Entry(_bsfg.Entry):
    """An entry in the Constant Temperature (CT) database. """

    Ematch: float = None # Energy at which the low and high energy formulae match [MeV]
    E0    : float = None # Energy shift for the low-energy approach [MeV]
    T     : float = None # Temperature for the low-energy approach [MeV]


class Database(_bsfg.Database):
    """The database object for the Constant Temperature (CT) level density model. """

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


def load(directory: str = None, file_path: str = None) -> Database:
    """Load the database into memory and return it. """
    if file_path is not None:
        return _bsfg._db.load(Database, file_path)
    elif directory is not None:
        file_path = _os.path.join(directory, local_file_path)
        return _bsfg._db.load(Database, file_path)
