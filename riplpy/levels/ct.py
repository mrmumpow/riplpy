

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
local_file_path = _os.path.join("levels", "levels-param.data")

# ========================

FILE_HEADER = "#Constant Temperature fit results; RIPL III discrete level library; December 2021\n#  Z   A El         T        dT        U0       dU0NlevNmax  N0  Nc     Umax       Uc     Chi Fit Flag NoX  Xm  EX   sigma\n#               [MeV]     [MeV]     [MeV]     [MeV]                    [MeV]    [MeV]                         [MeV]\n#-------------------------------------------------------------------------------------------------------------------------\n"
FORTRAN_FORMAT   = '(2i4,1x,a2,4(1x,f9.5),4i4,1x,f8.5,1x,f8.5,(1x,e10.3),1x,A1,1x,A1,2i4,f7.4,1x,f6.3)'
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
            data  = reader.read(line)
            Z     = data[0]
            A     = data[1]
            n       = _c.Nuclide(Z=Z, A=A)
            package = {'n': n,            # Nucleus
                       'T': data[3],      # Temperature T in the CT model
                       'dT': data[4],     # Uncertainty of T
                       'U0': data[5],     # Back-shift in CT model
                       'dU0': data[6],    # Uncertainty of U0
                       'Nlev': data[7],   # Number of levels in the ENSDF data set
                       'Nmax': data[8],   # Maximum level number up to which the level scheme is complete
                       'N0': data[9],     # Minimum level number from which the fit is considered
                       'Nc': data[10],    # Number of level at which unique spin sequence ends
                       'Umax': data[11],  # Energy corresponds to Nmax
                       'Uc': data[12],    # Energy corresponds to Nc
                       'Chi': data[13],   # Measure of the quality of fit (blank if there was no fit)
                       'Fit': data[14],   # If the record comes from the fit of pre-selected nuclei, which provided the T(A) function = blank if there was no fit
                       'Flag': data[15],  # 'F' if Chi>0.05 (bad fit); blank otherwise
                       'NoX': data[16],   # Number of levels with +X, +Y, +Z ... notation (X,Y,Z... are unknown energy values)
                       'Xm': data[17],    # Level number where the first +X, +Y, +Z ... notation appears
                       'Ex': data[18],    # Level energy where the first +X, +Y, +Z ... notation appears
                       'sigma': data[19]  # Spin cut-off values extracted from the discrete level library
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
    """An entry in the Constant Temperature (CT) fit database. """

    n    : _c.Nuclide = None  # Nuclide of the dataset
    T    : float      = None  # Temperature T in the CT model
    dT   : float      = None  # Uncertainty of T
    U0   : float      = None  # Back-shift in CT model
    dU0  : float      = None  # Uncertainty of U0
    Nlev : int        = None  # Number of levels in the ENSDF data set
    Nmax : int        = None  # Maximum level number up to which the level scheme is complete
    N0   : int        = None  # Minimum level number from which the fit is considered
    Nc   : int        = None  # Number of level at which unique spin sequence ends
    Umax : float      = None # Energy corresponds to Nmax
    Uc   : float      = None # Energy corresponds to Nc
    Chi  : float      = None # Measure of the quality of fit (blank if there was no fit)
    Fit  : str        = None # If the record comes from the fit of pre-selected nuclei, which provided the T(A) function = blank if there was no fit
    Flag : str        = None # 'F' if Chi>0.05 (bad fit); blank otherwise
    NoX  : int        = None # Number of levels with +X, +Y, +Z ... notation (X,Y,Z... are unknown energy values)
    Xm   : int        = None # Level number where the first +X, +Y, +Z ... notation appears
    Ex   : float      = None # Level energy where the first +X, +Y, +Z ... notation appears
    sigma: float      = None # Spin cut-off values extracted from the discrete level library


class Database(_db.NuclideDatabase):
    """Database of Constant Temperature (CT) fit of nuclear level schemes. """

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file

    # def load_numpy(self, filename: str) -> _np.array:
    #     """"""
    #     lst = []
    #     with open(filename, 'r') as fp:
    #         for line in fp.readlines():
    #             # Skip header lines
    #             if "#" in line[0]:
    #                 continue
    #             lst.append(const_reader.read(line))
    #     return _np.array(lst)



def load(directory: str = None, file_path: str = None) -> Database:
    """Load the database into memory and return it. """
    if file_path is not None:
        return _db.load(Database, file_path)
    elif directory is not None:
        file_path = _os.path.join(directory, local_file_path)
        return _db.load(Database, file_path)
