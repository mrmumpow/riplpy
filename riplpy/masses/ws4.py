# -*- coding: utf-8 -*-
"""Python objects that provide access to the WS4 mass model. 

Python 3.10+ is expected to run this code properly.

Examples:
    (1) Load and print the WS4 database::
       $ import riplpy.masses as masses
       $ ws4 = masses.ws4.load() # The WS4 database
       $ print(ws4.data)
    (2) Access a particular entry of the mass database using the get method::
       $ from riplpy.collections import Nuclide
       $ n = Nuclide(z=82, a=208)
       $ print(ws4.get(n))
    (3) 
Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

"""

# ========================

# Dataclasses
from dataclasses import dataclass as _dataclass

# Functools
from functools import partial as _partial

# Logging
import logging as _logging

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.config as _config
import riplpy.collections as _c
import riplpy.db as _db
from . import core as _core

# Module logger
_logger = _logging.getLogger(__name__)

# ========================

__all__ = ('FILE_PATH_KEY', 'LOCAL_FILE_PATH', 'FILE_HEADER', 'FORTRAN_FORMAT', 'reader', 'writer', 'read_ascii_file', 'write_ascii_file', 'Entry', 'Database', 'load')

# ========================

# Relative path to database file
FILE_PATH_KEY = 'mass_ws4'
LOCAL_FILE_PATH = _config.get_data_file_path(FILE_PATH_KEY)

# ========================

FILE_HEADER = "#\n#  Z   A s fl     Mexp      Err       Mth      Esh     beta2   beta4   beta6\n#                [MeV]     [MeV]     [MeV]     [MeV]                        \n#----------------------------------------------------------------------------------------------------\n"
FORTRAN_FORMAT = '(2i4,1x,a2,1x,i1,4f10.3,3f8.3)'
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
                    'Esh': data[7],
                    'beta2': data[8],
                    'beta4': data[9],
                    'beta6': data[10],
                }
                data_dict[n] = package
            except Exception as e:
                _logger.warning("Failed to parse line: %s. Error: %s", line.strip(), e)
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
                    entry['Esh'],
                    entry['beta2'],
                    entry['beta4'],
                    entry['beta6'],
                )
                fp.write(writer.write(line) + "\n")
            except Exception as e:
                _logger.warning("Failed to write entry: %s. Error: %s", entry, e)


@_dataclass
class Entry:
    """An entry in the WS4 mass database."""
    n      : _c.Nuclide  # Compound nucleus
    flag   : int         # Data flag
    Mexp   : float       # Experimental or recommended atomic mass excess [MeV]
    Err    : float       # Error on the experimental or recommended mass excess [MeV]
    Mth    : float       # Calculated WS4 atomic mass excess [MeV]
    Esh    : float       # Calculated shell correction energy [MeV]
    beta2  : float       # Quadrupole deformation
    beta4  : float       # Hexadecapole deformation
    beta6  : float       # Hexacontatetrapole deformation

    @classmethod
    def from_dict(cls, data: dict) -> "Entry":
        """Create an entry from a dictionary."""
        return cls(
            n=data['n'],
            flag=data['flag'],
            Mexp=data['Mexp'],
            Err=data['Err'],
            Mth=data['Mth'],
            Esh=data['Esh'],
            beta2=data['beta2'],
            beta4=data['beta4'],
            beta6=data['beta6'],
        )


class Database(_core.MassDatabase):
    """The WS4 ground state masses database. """

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


# Create the local 'load' function with config, database object, and file_path_key pre-filled
load = _partial(_db.loader, config=_config, db_obj=Database, file_path_key=FILE_PATH_KEY)
