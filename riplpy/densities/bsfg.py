# -*- coding: utf-8 -*-
"""Python objects that provide access to the Back-Shifted Fermi-Gas (BSFG) level density model. 
   Level density parameters are provided for the BSFG model without explicit treatment of collective effects. 
   The parameters are obtained by fitting the Fermi-gas model formula both to the RIPL II recommended spacings of s-wave neutron resonances D0 and to the cumulative number of low-lying levels evaluated from the analysis of nuclear levels. 
   Since the goal is to reproduce as well as possible both the discrete levels and the D0 values, the adopted parameters do not generally provide a perfect fit of D0. 
   Instead, we obtain a theoretical value Dth. 
   Therefore, uncertainty aerr is deduced by fitting Dth+Derr or Dth-Derr (See TECHDOC for more explanations). 

Python 3.10+ is expected to run this code properly.

Examples:
    (1) Load and print the BSFG level density database::
       $ import riplpy.densities as dens
       $ bsfg = dens.bsfg.load() # The BSFG level density database
       $ print(bsfg.data)
    (2) Access a particular entry of the BSFG level density database using the get method::
       $ from riplpy.collections import Nuclide
       $ n = Nuclide(z=50, a=125)
       $ print(bsfg.get(n))
    (3) 
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
import riplpy.db as _db
import riplpy.collections as _c

# ========================

__all__ = ('db_file_path', 'FILE_HEADER', 'FORTRAN_FORMAT', 'reader', 'writer', 'read_ascii_file', 'write_ascii_file', 'Entry', 'Database', 'load')

# ========================

# Current location
__loc__ = _os.path.dirname(_os.path.realpath(__file__))

# Database file
db_file_path = _os.path.join(__loc__, "data", "level-densities-bfmeff.dat")

# ========================

FILE_HEADER = "   Z  A  El   I0    Bn       D0        Derr    Nlow  Ulow   Ntop  Utop      dW      gamma      ainf     aerr    pairing\n"
FORTRAN_FORMAT = '(2i4,1x,a2,1x,f4.1,2x,f6.3,1x,1pe10.3,1x,1pe10.3,0p,1x,i3,2x,f6.3,2x,i3,2x,f6.3,3f10.5,f8.3,1f10.5)'
reader = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer = _ff.FortranRecordWriter(FORTRAN_FORMAT)

# ========================

def read_ascii_file(fpath: str) -> dict:
    """Read BSFG data from an ASCII formatted file and return as a dictionary. """

    # Placeholder dictionary
    d = {}

    # Skip this many header lines
    skiprows = 1

    # Read data from file
    with open(fpath, 'r') as fp:
        for i, line in enumerate(fp.readlines()):
            # Skip the header line(s)
            if i < skiprows:
                continue
            data  = reader.read(line)
            Z       = data[0]
            A       = data[1]
            n       = _c.Nuclide(Z=Z, A=A)
            package = {'n': n, 'Io': data[3], 'Bn': data[4], 'Do': data[5], 'Derr': data[6], 'Nlow': data[7], 'Ulow': data[8],
                       'Ntop': data[9], 'Utop': data[10], 'dW': data[11], 'gamma': data[12], 'ainf': data[13], 'aerr': data[14],
                       'pairing': data[15],
                      }
            d[n] = package
    return d


def write_ascii_file(fpath: str, data: dict) -> None:
    """Write a Back-Shifted Fermi-Gas (BSFG) ASCII file given a filename and a data dictionary. """

    # Write data to file
    with open(fpath, 'w') as fp:
        # Write header line
        fp.write(FILE_HEADER)
        # Loop over data
        for n in data.keys():
            #line = (n.Z, n.A, n.sym, data[n].Io, data[n].Bn, data[n].Do, data[n].Derr, data[n].Nlow, data[n].Ulow, data[n].Ntop, data[n].Utop, data[n].dW, data[n].gamma, data[n].ainf, data[n].aerr, data[n].pairing)
            line = data[n].as_tuple
            fp.write(writer.write(line)+"\n")


@_dataclass
class Entry(_db.NuclideDatabaseEntry):
    """An entry in the Back-Shifted Fermi-Gas (BSFG) database. """
    
    n      : _c.Nuclide = None # Compound nucleus
    Io     : float      = None # Spin of the ground state of the target nucleus
    Bn     : float      = None # Neutron binding energy of the compound nucleus [MeV]
    Do     : float      = None # Evaluated average resonance spacing [eV]
    Derr   : float      = None # Uncertainty of the resonance spacing [eV]
    Nlow   : int        = None # Lowest level used for the fit
    Ulow   : float      = None # Excitation energy of the level Nlow [MeV]
    Ntop   : int        = None # Highest level used for the fit
    Utop   : float      = None # Excitation energy of the level Ntop [MeV]
    dW     : float      = None # Shell correction energy used in the Ignatyuk formula [MeV]
    gamma  : float      = None # Damping parameter of the Ignatyuk formula
    ainf   : float      = None # Asymptotic level density parameter [1/MeV]
    aerr   : float      = None # Uncertainty of the asymptotic level density parameter [1/MeV]
    pairing: float      = None # Effective energy shift in MeV


class Database(_db.NuclideDatabase):
    """The database object for the Back-Shifted Fermi-Gas (BSFG) level density model. """

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


def load() -> Database:
    """Load the database into memeory and return it. """
    return _db.load(Database, db_file_path)
