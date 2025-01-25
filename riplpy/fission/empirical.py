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
local_file_path = _os.path.join("fission", "empirical-barriers.dat")

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


@_dataclass
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

    @property
    def heights(self, ) -> list:
        """Return the first and second barrier heights in the database as a list of tuples (Z,A,F_A,F_B). """
        ret = []
        for n in self.data.keys():
            Z, A = n.Z, n.A
            ret.append((Z,A,self.data[n].Ea,self.data[n].Eb))
        return ret
    
    @property
    def curvatures(self, ) -> list:
        """Return the first and second barrier curvatures in the database as list of tuples (Z,A,C_A,C_B). """
        ret = []
        for n in self.data.keys():
            Z, A = n.Z, n.A
            ret.append((Z,A,self.data[n].hwa,self.data[n].hwb))
        return ret

    # @property
    # def as_structured_numpy_array(self, ) -> _np.array:
    #     """Return the database as a structured Numpy array. """
    #     ret = []
    #     for n, v in self.data.items():
    #         # Define nucleus information
    #         Z,N,A,sym = n.Z,n.N,n.A,n.element_symbol
    #         # First barrier
    #         Syma, Ea, hwa = v.A.sp_sym, v.A.height, v.A.curvature
    #         # Second barrier
    #         Symb, Eb, hwb = v.B.sp_sym, v.B.height, v.B.curvature
    #         # Deltaf
    #         deltaf = v.deltaf
    #         # Append row
    #         ret.append((Z,N,A,sym,Syma,Ea,hwa,Symb,Eb,hwb,deltaf))
    #     return _np.array(ret, dtype=EXP_DB_NUMPY_DTYPE)

    # @property
    # def as_numpy_array(self, ) -> _np.array:
    #     """Return the database as a Numpy array. """
    #     ret = []
    #     for n, v in self.data.items():
    #         # Define nucleus information
    #         Z,N,A,sym = n.Z,n.N,n.A,n.element_symbol
    #         # First barrier
    #         Syma, Ea, hwa = v.A.sp_sym, v.A.height, v.A.curvature
    #         # Second barrier
    #         Symb, Eb, hwb = v.B.sp_sym, v.B.height, v.B.curvature
    #         # Deltaf
    #         deltaf = v.deltaf
    #         # Append row
    #         ret.append((Z,N,A,sym,Syma,Ea,hwa,Symb,Eb,hwb,deltaf))
    #     return _np.array(ret, dtype=object)

    # @property
    # def as_nuclides(self, ) -> list:
    #     """Return the database as a list of Nuclides. Each nuclide contains the relevant barrier properties. """
    #     ret = []
    #     for _n, _v in self.data.items():
    #         # Copy nucleus to a new memory location
    #         n = _copy.deepcopy(_n)
    #         # First barrier
    #         n.Syma, n.Ea, n.hwa = _v.A.sp_sym, _v.A.height, _v.A.curvature
    #         # Second barrier
    #         n.Symb, n.Eb, n.hwb = _v.B.sp_sym, _v.B.height, _v.B.curvature
    #         # Deltaf
    #         n.deltaf = _v.deltaf
    #         ret.append(n)
    #     return ret

    def first_barrier(self, n: _c.Nuclide) -> float:
        """Return the first barrier properties of the provided nucleus (nuc). """
        return self.data[n].Ea
    
    def second_barrier(self, n: _c.Nuclide) -> float:
        """Return the second barrier properties of the provided nucleus (nuc). """
        return self.data[n].Eb


def load(directory: str = None, file_path: str = None) -> Database:
    """Load the database into memory and return it. """
    if file_path is not None:
        return _db.load(Database, file_path)
    elif directory is not None:
        file_path = _os.path.join(directory, local_file_path)
        return _db.load(Database, file_path)
