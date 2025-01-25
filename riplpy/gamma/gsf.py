
# -*- coding: utf-8 -*-
"""Python objects which provide access to the gamma-ray strength function (GSF) database of the Reference Input Parameter Library (RIPL). 

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

__all__ = ('local_data_dir', 'FILE_HEADER', 'FORTRAN_FORMAT', 'reader', 'writer', 'read_ascii_file', 'write_ascii_file', 'Entry', 'Database', 'load')

# ========================

# Relative path to database folder
local_data_dir = "gamma"

# ========================

FILE_HEADER = "#-----------------------\n#  U[MeV]  fE1[mb/MeV]\n#-----------------------\n"
FORTRAN_FORMAT = '(f9.3,e12.3)'
reader   = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer   = _ff.FortranRecordWriter(FORTRAN_FORMAT)

# ========================

def read_ascii_file(fpath: str) -> dict:
    """Read data from an ASCII file and return a dictionary. """
    # Placeholder dictionary
    d = {}

    U, fE1 = [], []

    # Read data from file
    with open(fpath, 'r') as fp:
        for i, line in enumerate(fp.readlines()):
            if i == 0:
                line = line.split()
                Z = int(line[0])
                A = int(line[1])
                n = _c.Nuclide(z=Z, a=A)
                continue
            # Skip the header line(s)
            elif "#" in line[0]:
                continue
            data  = reader.read(line)
            U.append(data[0])
            fE1.append(data[1])
        package = {'U': U, 'fE1': fE1}
        d[n] = package
    return d


def write_ascii_file(fpath: str, data: dict, n: _c.Nuclide) -> None:
    """Write ASCII file given a filename, data dictionary and entry (n). """

    # Write data to file
    with open(fpath, 'w') as fp:
        fp.write(f"{n.Z} {n.A}\n")
        # Write header line
        fp.write(FILE_HEADER)
        # Loop over data (only one entry per file)
        for u,fE1 in zip(data[n]['U'], data[n]['fE1']):
            line = (u,fE1)
            fp.write(writer.write(line)+"\n")


class Entry(_core.GammaStrengthFunction, _db.NuclideDatabaseEntry):
    """An object which represents an entry in the GSF database. """
    pass


class Database(_db.Database):

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file

    def load(self, fpath: str) -> None:
        """Read gamma-ray strength (GSF) information from an ASCII file for a single entry. 
           Not this can be used in successive calls, each time adding potentially new entries to the database (self.data).
        """
        _data = type(self).reader(fpath)
        for entry in _data.keys():
            self.data[entry] = _data[entry]

    def load_all(self, directory: str) -> None:
        """Load the entire gamma-ray strength function (GSF) database. """
        # Loop over the element numbers
        db_loc = _os.path.join(directory, local_data_dir, 'gsf')
        for fn in _os.listdir(db_loc):
            fpath = _os.path.join(db_loc, fn)
            self.load(fpath)

    def save(self, fpath: str, entry: _c.Nuclide) -> None:
        """Save a single entry in the database. """
        write_ascii_file(fpath, self.data, entry)

    def save_all(self, directory: str) -> None:
        """Save all entries in the database to a directory in individual files. """
        for entry in self.data.keys():
            fn = f"gsf_Z{entry.Z:03d}A{entry.A:03d}.dat"
            fpath = _os.path.join(directory, fn)
            self.save(fpath, entry)


def load_all(directory: str) -> Database:
    """Load and return the GSF database. """
    d = Database()
    d.load_all(directory)
    return d


def load_nucleus(n: _c.Nuclide, directory: str) -> Database:
    d = Database()
    fpath = _os.path.join(directory, local_data_dir, 'gsf', f'gsf_Z{n.Z:03d}A{n.A:03d}.dat')
    d.load(fpath)
    return d