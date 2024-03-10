# -*- coding: utf-8 -*-
"""Python objects which provide access to the experimental giant dipole resonance (GDR) fits with SLO of the Reference Input Parameter Library (RIPL). 

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
from . import core as _core

# ========================

__all__ = ('db_file_path', 'FILE_HEADER', 'FORTRAN_FORMAT', 'reader', 'writer', 'read_ascii_file', 'write_ascii_file', 'Entry', 'Database', 'load')

# ========================

# Current location
__loc__ = _os.path.dirname(_os.path.realpath(__file__))
# Database location
db_file_path = _os.path.join(__loc__, "data", "ripl3-gdr-parameters&errors-exp-SLO.dat")

# ========================

FILE_HEADER = "#   gdr-parameters&errors-exp-SLO.dat\n#   Experimental values and errors of GDR parameters  within SLO approach\n#\n# Z   A El Reac  E1     CS1     W1    E2     CS2    W2  E_{min}-E_{max} Ref\n#               Err     Err    Err   Err     Err    Err\n#              [MeV]   [mb]   [MeV] [MeV]   [mb]  [MeV]     [MeV]\n#-----------------------------------------------------------------------\n"
LINE1_FORMAT = '(2X,I2,1X,I3,1X,A2,1X,I2,1X,F5.2,2X,F5.1,2X,F5.2,2X,F5.2,2X,F5.1,3X,F5.2,1X,F4.1,3X,F4.1,2X,A5)'
LINE2_FORMAT = '(15X,F5.2,2X,F5.1,2X,F5.2,2X,F5.2,2X,F5.1,3X,F5.2)'
line1_reader = _ff.FortranRecordReader(LINE1_FORMAT)
line2_reader = _ff.FortranRecordReader(LINE2_FORMAT)
line1_writer = _ff.FortranRecordWriter(LINE1_FORMAT)
line2_writer = _ff.FortranRecordWriter(LINE2_FORMAT)

# ========================

def line1_as_tuple(entry: object, ) -> tuple:
    """Return line1 in the ASCII file as a tuple. """
    return (entry.n.Z, entry.n.A, entry.n.symbol, entry.reac, entry.E1, entry.CS1, entry.W1, entry.E2, entry.CS2, entry.W2, entry.Emin, entry.Emax, entry.reference)


def line2_as_tuple(entry: object, ) -> tuple:
    """Return line2 in the ASCII file as a tuple. """
    return (entry.E1_error, entry.CS1_error, entry.W1_error, entry.E2_error, entry.CS2_error, entry.W2_error)


def read_ascii_file(fpath: str) -> dict:
    """Read data from an ASCII file and return a dictionary. """
    # Data placeholder
    d = {}

    # Counter for number of header lines
    header_lines = 0

    # Read file
    with open(fpath, 'r') as fp:
        # Skip the header
        flag = False
        for i,line in enumerate(fp.readlines()):
            if "#" in line[0]:
                header_lines += 1
                continue
            # Define even / odd structure of data
            j = i - header_lines
            #print(line, i, j)
            if j % 2 == 0:
                data = line1_reader.read(line)
                Z    = int(data[0])
                A    = int(data[1])
                n    = _c.Nuclide(Z=Z, A=A)
                reac = int(data[3])
                E1   = float(data[4])
                CS1  = float(data[5])
                W1   = float(data[6])
                try:
                    E2  = float(data[7])
                    CS2 = float(data[8])
                    W2  = float(data[9])
                except:
                    E2  = None
                    CS2 = None
                    W2  = None
                Emin = float(data[10])
                Emax = float(data[11])
                ref  = data[12]
                flag = False
            else:
                data = line2_reader.read(line)
                E1_error  = float(data[0])
                CS1_error = float(data[1])
                W1_error  = float(data[2])
                try:
                    E2_error  = float(data[3])
                    CS2_error = float(data[4])
                    W2_error  = float(data[5])
                except:
                    E2_error  = None
                    CS2_error = None
                    W2_error  = None
                flag = True
            if flag:
                packet = {'n': n, 'reac': reac, 'E1': E1, 'E2': E2, 'W1': W1, 'W2': W2, 'CS1': CS1, 'CS2': CS2,
                          'E1_error': E1_error, 'E2_error': E2_error, 'W1_error': W1_error, 'W2_error': W2_error,
                          'CS1_error': CS1_error, 'CS2_error': CS2_error, 'Emin': Emin, 'Emax': Emax, 
                          'reference': ref,
                         }
                d[n] = packet
    return d


def write_ascii_file(fpath: str, data: dict) -> None:
    """Write ASCII file given a filename and a data dictionary. """

    # Write data to file
    with open(fpath, 'w') as fp:
        # Write header line
        fp.write(FILE_HEADER)
        # Loop over data
        for n in data.keys():
            line1 = line1_as_tuple(data[n])
            line2 = line2_as_tuple(data[n])
            fp.write(line1_writer.write(line1)+"\n")
            fp.write(line2_writer.write(line2)+"\n")


class Entry(_core.Experimental_GDR_Parameter, _db.NuclideDatabaseEntry):
    """An object which represents an entry in the experimental GDR SLO parameter database. """
    pass


class Database(_db.Database):

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


def load() -> Database:
    """Load and return the experimental GDR SLO parameter database. """
    return _db.load(Database, db_file_path)
