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

# Dataclasses
from dataclasses import dataclass as _dataclass

# Typing
from typing import ClassVar as _ClassVar

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
FILE_PATH_KEY = 'fission_barriers_empirical_new'
LOCAL_FILE_PATH = _config.get_data_file_path(FILE_PATH_KEY)

# ========================

FILE_HEADER = "# The tabulation is given for fissioning nuclei (those marked * are 3H)\n#                    All barrier heights, widths and uncertainties are in MeV \n#  Z   A  s   Syma   Va  dVa  hwa dwa  Symb   Vb  dVb hwb dwb  Vc  Dvc  hwc  dwc\n#-------------------------------------------------------------------------------  \n"
FORTRAN_FORMAT = "(A1,I3,1X,I3,1X,A3,2X,A3,3X,F5.2,F4.2,F5.2,F4.2,1X,A2,3X,F5.2,F4.2,F4.2,F5.2,F4.1,F4.2,F4.1,F4.2)"
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
            if "#" in line[0] or "a" in line or len(line.split()) == 0:
                continue
            data   = reader.read(line)

            Z    = int(data[1])        # Atomic number
            A    = int(data[2])        # Mass number
            n    = _c.Nuclide(Z=Z, A=A)
            s    = data[3].strip()     # Symbol (e.g., Hg, Tl)
            syma = data[4].strip()     # Symmetry for barrier A
            Va   = float(data[5])      # Barrier height A
            dVa  = float(data[6])      # Uncertainty in Va
            hwa  = None if (data[7] is None or str(data[7]).strip() == "") else float(data[7])    # Barrier width A
            dwa  = None if (data[8] is None or str(data[8]).strip() == "") else float(data[8])    # Uncertainty in width A
            symb = data[9].strip()                                                           # Symmetry for barrier B
            Vb   = None if (data[10] is None or str(data[10]).strip() == "") else float(data[10]) # Barrier height B
            dVb  = None if (data[11] is None or str(data[11]).strip() == "") else float(data[11]) # Uncertainty in Vb
            hwb  = None if (data[12] is None or str(data[12]).strip() == "") else float(data[12]) # Barrier width B
            dwb  = None if (data[13] is None or str(data[13]).strip() == "") else float(data[13]) # Uncertainty in width B
            Vc   = None if (data[14] is None or str(data[14]).strip() == "") else float(data[14]) # Barrier height C
            Dvc  = None if (data[15] is None or str(data[15]).strip() == "") else float(data[15]) # Uncertainty in Vc
            hwc  = None if (data[16] is None or str(data[16]).strip() == "") else float(data[16]) # Barrier width C
            dwc  = None if (data[17] is None or str(data[17]).strip() == "") else float(data[17]) # Uncertainty in width C

            # Create an entry
            package = {'n': n, 's': s, 'syma': syma, 'Va': Va, 'dVa': dVa, 'hwa': hwa, 'dwa': dwa,
                       'symb': symb, 'Vb': Vb, 'dVb': dVb, 'hwb': hwb, 'dwb': dwb,
                       'Vc': Vc, 'Dvc': Dvc, 'hwc': hwc, 'dwc': dwc}

            # Add entry to dictionary
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
    """An entry in the new empirical fission barrier database.

    Contains multi-humped fission barrier parameters with uncertainties,
    supporting up to triple-humped barriers for actinides.

    Attributes:
        n: Target nucleus (Nuclide object with Z, A, N properties)
        s: Element symbol
        syma: Symmetry designation for barrier A
        Va: Barrier A height [MeV]
        dVa: Uncertainty on Va [MeV]
        hwa: Barrier A curvature [MeV]
        dwa: Uncertainty on hwa [MeV]
        symb: Symmetry designation for barrier B
        Vb: Barrier B height [MeV]
        dVb: Uncertainty on Vb [MeV]
        hwb: Barrier B curvature [MeV]
        dwb: Uncertainty on hwb [MeV]
        Vc: Barrier C height [MeV] (third hump, if present)
        Dvc: Uncertainty on Vc [MeV]
        hwc: Barrier C curvature [MeV]
        dwc: Uncertainty on hwc [MeV]
    """

    n: _c.Nuclide = None
    s: str     = None
    syma: str  = None
    Va: float  = None
    dVa: float = None
    hwa: float = None
    dwa: float = None
    symb: str  = None
    Vb: float  = None
    dVb: float = None
    hwb: float = None
    dwb: float = None
    Vc: float  = None
    Dvc: float = None
    hwc: float = None
    dwc: float = None

    # Field descriptions for help/info display
    _field_info: _ClassVar[dict] = {
        'n': 'Target nucleus',
        's': 'Element symbol',
        'syma': 'Symmetry designation for barrier A',
        'Va': 'Barrier A height [MeV]',
        'dVa': 'Uncertainty on Va [MeV]',
        'hwa': 'Barrier A curvature [MeV]',
        'dwa': 'Uncertainty on hwa [MeV]',
        'symb': 'Symmetry designation for barrier B',
        'Vb': 'Barrier B height [MeV]',
        'dVb': 'Uncertainty on Vb [MeV]',
        'hwb': 'Barrier B curvature [MeV]',
        'dwb': 'Uncertainty on hwb [MeV]',
        'Vc': 'Barrier C height [MeV] (third hump)',
        'Dvc': 'Uncertainty on Vc [MeV]',
        'hwc': 'Barrier C curvature [MeV]',
        'dwc': 'Uncertainty on hwc [MeV]',
    }

    @property
    def as_tuple(self) -> tuple:
        """Return a tuple representation matching the ASCII file format."""
        # First character is blank or '*' for triaxial
        marker = '*' if self.Vc is not None else ' '
        return (marker, self.n.Z, self.n.A, self.s, self.syma, self.Va, self.dVa, self.hwa, self.dwa,
                self.symb, self.Vb, self.dVb, self.hwb, self.dwb, self.Vc, self.Dvc, self.hwc, self.dwc)


class Database(_db.Database):

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file

    @property
    def heights(self, ) -> list:
        """Return the barrier heights in the database as a list of tuples (Z,A,F_A,F_B,F_C). """
        ret = []
        for n in self.data.keys():
            Z, A = n.Z, n.A
            ret.append((Z,A,self.data[n].Va,self.data[n].Vb,self.data[n].Vc))
        return ret
    
    @property
    def curvatures(self, ) -> list:
        """Return the barrier curvatures in the database as list of tuples (Z,A,C_A,C_B,C_C). """
        ret = []
        for n in self.data.keys():
            Z, A = n.Z, n.A
            ret.append((Z,A,self.data[n].hwa,self.data[n].hwb,self.data[n].hwc))
        return ret

    def first_barrier(self, n: _c.Nuclide) -> float:
        """Return the first barrier properties of the provided nucleus (n). """
        return self.data[n].Va
    
    def second_barrier(self, n: _c.Nuclide) -> float:
        """Return the second barrier properties of the provided nucleus (n). """
        return self.data[n].Vb

    def third_barrier(self, n: _c.Nuclide) -> float:
        """Return the third barrier properties of the provided nucleus (n). """
        return self.data[n].Vc


# Create the local 'load' function with config, database object, and file_path_key pre-filled
load = _partial(_db.loader, config=_config, db_obj=Database, file_path_key=FILE_PATH_KEY)
