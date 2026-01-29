# -*- coding: utf-8 -*-
"""Python objects which provide access to the theoretical BSGK3 fission barrier database of the Reference Input Parameter Library (RIPL). 

Python 3.10+ is expected to run this code properly.

Examples:
    (1) @TODO: Finish
        $

Todo:
    * Provide more examples of use cases.
    * Test in production.
    
Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

"""

# ========================

# Dataclasses
from dataclasses import dataclass as _dataclass

# Functools
from functools import partial as _partial

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.config as _config
import riplpy.collections as _c
import riplpy.db as _db

# ========================

__all__ = ('FILE_PATH_KEY', 'LOCAL_FILE_PATH', 'FILE_HEADER', 'FORTRAN_FORMAT', 'reader', 'writer', 'read_ascii_file', 'write_ascii_file', 'Entry', 'Database', 'load')

# ========================

# Path key of the database file as defined in config.py
FILE_PATH_KEY = 'fission_barriers_bskg3'
LOCAL_FILE_PATH = _config.get_data_file_path(FILE_PATH_KEY)

# ========================

FILE_HEADER = "#         |         Inner            |            Outer 1         |         Outer 2          |    Isomer\n# Z   N   |  E[MeV] B20   B22   B30  |  E[MeV]  B20   B22   B30   | E[MeV]  B20   B22   B30  |  E[MeV] B20   B22   B30\n"
FORTRAN_FORMAT = '(2I4, 4(F8.3, F6.2, F6.2, F6.2))'
reader = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer = _ff.FortranRecordWriter(FORTRAN_FORMAT)

# ========================

def read_ascii_file(fpath: str) -> dict:
    """Read data from an ASCII file and return a dictionary. """
    # Placeholder dictionary
    d = {}

    # Read data from file
    with open(fpath, 'r') as fp:
        for line in fp:
            # Skip header lines
            if line.startswith("#"):
                continue

            # Use FortranRecordReader to parse the line
            data = reader.read(line)
            Z, N = data[0], data[1]

            # Extract data for each section
            inner = {
                'E[MeV]': data[2],
                'B20': data[3],
                'B22': data[4],
                'B30': data[5]
            }
            outer1 = {
                'E[MeV]': data[6],
                'B20': data[7],
                'B22': data[8],
                'B30': data[9]
            }
            outer2 = {
                'E[MeV]': data[10],
                'B20': data[11],
                'B22': data[12],
                'B30': data[13]
            }
            isomer = {
                'E[MeV]': data[14],
                'B20': data[15],
                'B22': data[16],
                'B30': data[17]
            }

            # Create a dictionary entry
            package = {
                'inner': inner,
                'outer1': outer1,
                'outer2': outer2,
                'isomer': isomer
            }

            # Use Z, N as the key
            n = _c.Nuclide(Z=Z, N=N)
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
    """An object which represents an entry in the empirical fission barrier database. """
    
    inner : dict = None  # Inner fission barrier
    outer1: dict = None # Outer 1 fission barrier
    outer2: dict = None # Outer 2 fission barrier
    isomer: dict = None # Isomer 


class Database(_db.Database):

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


# Create the local 'load' function with config, database object, and file_path_key pre-filled
load = _partial(_db.loader, config=_config, db_obj=Database, file_path_key=FILE_PATH_KEY)
