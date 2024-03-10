# -*- coding: utf-8 -*-
"""Python objects which provide access to the HFB fission barrier database of the Reference Input Parameter Library (RIPL). 

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
db_file_path = _os.path.join(__loc__, "data", "empirical-hfb-barriers.dat")

# ========================

FILE_HEADER = "# Z   N   A  s     Bin     hwin   alphain deltain  Bout   hwout  alphaout deltaout Bout2  hwout2 alphaout2 deltaout2\n#                 [MeV]   [MeV] [MeV^-1/2] [MeV]  [MeV]   [MeV] [MeV^-1/2] [MeV]  [MeV]   [MeV] [MeV^-1/2] [MeV]\n#-------------------------------------------------------------------------------------------------------------------\n"
FORTRAN_FORMAT = '(3i4,1x,a2,12f8.2)'
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
            data      = reader.read(line)
            Z         = data[0]
            N         = data[1]
            A         = data[2]
            n         = _c.Nuclide(Z=Z, A=A)
            Bin       = data[4]
            hwin      = data[5]
            alphain   = data[6]
            deltain   = data[7]
            Bout      = data[8]
            hwout     = data[9]
            alphaout  = data[10]
            deltaout  = data[11]
            Bout2     = data[12]
            hwout2    = data[13]
            alphaout2 = data[14]
            deltaout2 = data[15]

            package = {'Bin': Bin, 'hwin': hwin, 'alphain': alphain, 'deltain': deltain,
                       'Bout': Bout, 'hwout': hwout, 'alphaout': alphaout, 'deltaout': deltaout,
                       'Bout2': Bout2, 'hwout2': hwout2, 'alphaout2': alphaout2, 'deltout2': deltaout2,
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
    """An object which represents an entry in the HFB fission barrier database. """
    
    Bin      : float = None # Comment
    hwin     : float = None # Comment
    alphain  : float = None # Comment
    deltain  : float = None # Comment
    Bout     : float = None # Comment
    hwout    : float = None # Comment
    alphaout : float = None # Comment
    deltaout : float = None # Comment
    Bout2    : float = None # Comment
    hwout2   : float = None # Comment
    alphaout2: float = None # Comment
    deltaout2: float = None # Comment


class Database(_db.Database):

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


def load() -> Database:
    """Load and return the HFB fission barrier database. """
    return _db.load(Database, db_file_path)
