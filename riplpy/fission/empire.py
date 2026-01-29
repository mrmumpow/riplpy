# -*- coding: utf-8 -*-
"""Python objects which provide access to the EMPIRE empirical fission barrier database of the Reference Input Parameter Library (RIPL). 

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
FILE_PATH_KEY = 'fission_barriers_empire'
LOCAL_FILE_PATH = _config.get_data_file_path(FILE_PATH_KEY)

# ========================

FILE_HEADER = "# The tabulation is given for fissioning nuclei (those marked * are 3H)\n#                    All barrier heights, widths and uncertainties are in MeV \n#  Z   A  s   Syma    Va     hwa   Symb    Vb     hwb    Vc  	   Deltaf\n#-------------------------------------------------------------------------------  \n"
FORTRAN_FORMAT = '(A1,I3,1X,I3,1X,A3,2X,A3,3X,F6.2,F6.2,4X,A2,2X,F6.2,2X,F6.2,2X,F6.3,2X,F6.3)'
reader = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer = _ff.FortranRecordWriter(FORTRAN_FORMAT)

# ========================

def read_ascii_file(fpath: str) -> dict:
    """Read data from an ASCII file and return a dictionary. """
    d = {}

    with open(fpath, 'r') as fp:
        for line in fp:
            # Skip header lines
            if line.startswith("#") or line.strip() == "" or "a" in line:
                continue

            # Parse using Fortran format
            data = reader.read(line)
            Z = data[1]
            A = data[2]
            n = _c.Nuclide(Z=Z, A=A)
            symbol = data[3].strip()
            symmetry = data[4].strip()
            Va = data[5]
            hwa = data[6] if len(data) > 6 else None
            Symb = data[7].strip() if len(data) > 7 else None
            Vb = data[8] if len(data) > 8 else None
            hwb = data[9] if len(data) > 9 else None
            Vc = data[10] if len(data) > 10 else None
            Deltaf = data[11] if len(data) > 11 else None

            # Create an entry
            package = {'symmetry': symmetry, 'Va': Va, 'hwa': hwa, 'Symb': Symb, 'Vb': Vb, 'hwb': hwb, 'Vc': Vc, 'Deltaf': Deltaf}
            d[n] = package

            #except ValueError as e:
            #    print(f"Could not parse line: {line.strip()}\nError: {e}")

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

    symmetry: str   = None
    Va      : float = None
    hwa     : float = None
    Symb    : str   = None
    Vb      : float = None
    hwb     : float = None
    Vc      : float = None
    Deltaf  : float = None


class Database(_db.Database):

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


# Create the local 'load' function with config, database object, and file_path_key pre-filled
load = _partial(_db.loader, config=_config, db_obj=Database, file_path_key=FILE_PATH_KEY)
