
# ========================

# OS
import os as _os

# Dataclass
from dataclasses import dataclass as _dataclass

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.collections as _c
import riplpy.db as _db

# ========================

# Relative path to database file
local_file_path = _os.path.join('resonances', 'resonances1.dat')

# ========================

FILE_HEADER = "#                 Resonance data for p-wave resonances \n# Z El  A   Io     Bn        D1        dD      S1    dS    Gg   dG   Com.\n#                 [MeV]     [keV]     [keV]  [1E-4][1E-4][meV][meV]  &Ref\n#========================================================================\n"
FORTRAN_FORMAT   = '(i3,1x,a2,1x,i3,2x,f3.1,2x,f6.3,2x,2(e8.2,2x),1x,2(f4.2,2x),2(f4.1,1x),2x,a4)'
reader = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer = _ff.FortranRecordWriter(FORTRAN_FORMAT)

# ========================

def read_ascii_file(fpath: str) -> dict:
    """Read P-wave data from an ASCII file and return a dictionary. """
    # Placeholder dictionary
    d = {}

    # Skip this many header lines
    skiprows = 1

    # Read data from file
    with open(fpath, 'r') as fp:
        for i, line in enumerate(fp.readlines()):
            # Skip the header line(s)
            if "#" in line[0]:
                continue
            data  = reader.read(line)
            Z     = data[0]
            # @TODO: Inconsistent column ordering; this needs to be fixed in the ASCII file
            A = data[2]
            n       = _c.Nuclide(Z=Z, A=A)
            package = {'n': n, 'Io': data[3], 'Bn': data[4], 'D': data[5], 'Derr': data[6], 'Str': data[7], 'Serr': data[8],
                       'Gam': data[9], 'Gerr': data[10], 'ref': data[11],
                      }
            d[n] = package
    return d


def write_ascii_file(fpath: str, data: dict) -> None:
    """Write P-wave ASCII file given a filename and a data dictionary. """

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
    """An entry in the resonance spacing database. """

    n     : _c.Nuclide = None # Compound nucleus
    Io    : float      = None # Spin of the ground state of the target nucleus
    Bn    : float      = None # Neutron binding energy for the corresponding compound nucleus [MeV]
    D     : float      = None # Average resonance spacing [keV]
    Derr  : float      = None # Uncertainty in D [keV]
    Str   : float      = None # S/P-wave neutron strength function 10**(-4)
    Serr  : float      = None # Uncertainty of Str 10**(-4)
    Gam   : float      = None # Average radiative width [meV]
    Gerr  : float      = None # Uncertainty of Gam [meV]
    ref   : str        = None # Reference to the work in which the analysis was performed


class Database(_db.NuclideDatabase):

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


def load(directory: str = None, file_path: str = None) -> Database:
    """Load the database into memory and return it. """
    if file_path is not None:
        return _db.load(Database, file_path)
    elif directory is not None:
        file_path = _os.path.join(directory, local_file_path)
        return _db.load(Database, file_path)
