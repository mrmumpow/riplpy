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
FILE_PATH_KEY = 'fission_barriers_hfb'
LOCAL_FILE_PATH = _config.get_data_file_path(FILE_PATH_KEY)

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

            package = {'n': n, 'Bin': Bin, 'hwin': hwin, 'alphain': alphain, 'deltain': deltain,
                       'Bout': Bout, 'hwout': hwout, 'alphaout': alphaout, 'deltaout': deltaout,
                       'Bout2': Bout2, 'hwout2': hwout2, 'alphaout2': alphaout2, 'deltaout2': deltaout2,
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
    """An object which represents an entry in the HFB fission barrier database. """

    n        : _c.Nuclide = None # Compound nucleus
    Bin      : float = None # Inner barrier height [MeV]
    hwin     : float = None # Inner barrier width [MeV]
    alphain  : float = None # Inner barrier alpha [MeV^-1/2]
    deltain  : float = None # Inner barrier delta [MeV]
    Bout     : float = None # Outer barrier height [MeV]
    hwout    : float = None # Outer barrier width [MeV]
    alphaout : float = None # Outer barrier alpha [MeV^-1/2]
    deltaout : float = None # Outer barrier delta [MeV]
    Bout2    : float = None # Second outer barrier height [MeV]
    hwout2   : float = None # Second outer barrier width [MeV]
    alphaout2: float = None # Second outer barrier alpha [MeV^-1/2]
    deltaout2: float = None # Second outer barrier delta [MeV]

    @property
    def as_tuple(self) -> tuple:
        """Return a tuple representation matching the ASCII file format."""
        return (self.n.Z, self.n.N, self.n.A, self.n.element_symbol,
                self.Bin, self.hwin, self.alphain, self.deltain,
                self.Bout, self.hwout, self.alphaout, self.deltaout,
                self.Bout2, self.hwout2, self.alphaout2, self.deltaout2)


class Database(_db.Database):

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file

    # @property
    # def heights(self, ) -> list:
    #     """Return the barrier heights in the database as a list of tuples (Z,A,F_A,F_B,F_C). """
    #     ret = []
    #     for nuc in self.data.keys():
    #         Z, A = nuc.Z, nuc.A
    #         ret.append((Z,A,self.data[nuc].A.height,self.data[nuc].B.height,self.data[nuc].C.height))
    #     return ret

    # @property
    # def curvatures(self, ) -> list:
    #     """Return the barrier curvatures in the database as list of tuples (Z,A,C_A,C_B,C_C). """
    #     ret = []
    #     for nuc in self.data.keys():
    #         Z, A = nuc.Z, nuc.A
    #         ret.append((Z,A,self.data[nuc].A.curvature,self.data[nuc].B.curvature,self.data[nuc].C.curvature))
    #     return ret

    # @property
    # def as_numpy_array(self, ) -> _np.array:
    #     """Return the database as a structured Numpy array. """
    #     ret = []
    #     for n, v in self.data.items():
    #         # Define nucleus information
    #         Z, N, A, sym = n.Z, n.N, n.A, n.element_symbol
    #         # First barrier
    #         Bin, hwin, alphain, deltain = v.A.height, v.A.curvature, v.A.alpha, v.A.delta
    #         # Second barrier
    #         Bout, hwout, alphaout, deltaout = v.B.height, v.B.curvature, v.B.alpha, v.B.delta
    #         # Third barrier
    #         Bout2, hwout2, alphaout2, deltaout2 = v.C.height, v.C.curvature, v.C.alpha, v.C.delta
    #         ret.append((Z,N,A,sym,Bin,hwin,alphain,deltain,Bout,hwout,alphaout,deltaout,Bout2,hwout2,alphaout2,deltaout2))
    #     return _np.array(ret, dtype=HFB_DB_NUMPY_DTYPE)

    # @property
    # def as_nuclides(self, ) -> list:
    #     """Return the database as a list of Nuclides. Each nuclide contains the relevant barrier properties. """
    #     ret = []
    #     for _n, _v in self.data.items():
    #         # Copy nucleus to a new memory location
    #         n = _copy.deepcopy(_n)
    #         # First barrier
    #         n.Bin, n.hwin, n.alphain, n.deltain = _v.A.height, _v.A.curvature, _v.A.alpha, _v.A.delta
    #         # Second barrier
    #         n.Bout, n.hwout, n.alphaout, n.deltaout = _v.B.height, _v.B.curvature, _v.B.alpha, _v.B.delta
    #         # Third barrier
    #         n.Bout2, n.hwout2, n.alphaout2, n.deltaout2 = _v.C.height, _v.C.curvature, _v.C.alpha, _v.C.delta
    #         ret.append(n)
    #     return ret


# Create the local 'load' function with config, database object, and file_path_key pre-filled
load = _partial(_db.loader, config=_config, db_obj=Database, file_path_key=FILE_PATH_KEY)
