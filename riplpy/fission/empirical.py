# -*- coding: utf-8 -*-
"""Python objects which provide access to the empirical fission barrier database of the Reference Input Parameter Library (RIPL). 

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

# OS
import os as _os

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
db_file_path = _os.path.join(__loc__, "data", "empirical-barriers.dat")

# ========================

FILE_HEADER = "#  Z   A  s   Syma    Ea     hwa   Symb    Eb     hwb    Deltaf\n#                   [MeV]   [MeV]        [MeV]   [MeV]    [MeV]\n#--------------------------------------------------------------\n"
FORTRAN_FORMAT = '(2i4,1x,a2,1x,2(3x,a2,2f8.2),f9.3)'
reader = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer = _ff.FortranRecordWriter(FORTRAN_FORMAT)

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
            data   = reader.read(line)
            Z      = data[0]
            A      = data[1]
            n      = _c.Nuclide(Z=Z, A=A)
            syma   = data[3]
            Ea     = data[4]
            hwa    = data[5]
            symb   = data[6]
            Eb     = data[7]
            hwb    = data[8]
            deltaf = data[9]

            package = {
                       'Ea': Ea, 'hwa': hwa, 'syma': syma, 
                       'Eb': Eb, 'hwa': hwb, 'symb': symb,
                       'deltaf': deltaf
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


class Entry(_db.NuclideDatabaseEntry):
    """An object which represents an entry in the empirical fission barrier database. """
    
    Ea    : float = None # Generally in [MeV]
    hwa   : float = None # Generally in [MeV]
    syma  : str   = None # shorthand notation for saddle
    Eb    : float = None # Generally in [MeV]
    hwb   : float = None # Generally in [MeV]
    symb  : str   = None # shorthand notation for saddle
    deltaf: float = None # Generally in [MeV]


class Database(_db.Database):

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


def load() -> Database:
    """Load and return the empirical fission barrier database. """
    return _db.load(Database, db_file_path)
