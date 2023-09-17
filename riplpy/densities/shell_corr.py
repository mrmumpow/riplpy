
# ========================

# Dataclasses
from dataclasses import dataclass

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.db as _db
import riplpy.collections as _c

# ========================

FILE_HEADER = "#     Myers-Swiatecki shell corrections \n#  Z   A El     Shell   Defcor  bet2  bet4\n#               [MeV]    [MeV]\n#========================================== \n"
FORTRAN_FORMAT = '(2i4,1x,a2,2(1x,f8.3),2(f6.3))'
reader = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer = _ff.FortranRecordWriter(FORTRAN_FORMAT)

# ========================


def read_ascii_file(fpath: str) -> dict:
    """Read shell correction data from an ASCII formatted file and return as a dictionary. """

    # Placeholder dictionary
    d = {}

    # Read data from file
    with open(fpath, 'r') as fp:
        for i, line in enumerate(fp.readlines()):
            # Skip the header line(s)
            if "#" in line[0]:
                continue
            data  = reader.read(line)
            Z       = data[0]
            A       = data[1]
            n       = _c.Nuclide(Z=Z, A=A)
            package = {'n': n, 'shell': data[3], 'corr': data[4], 'beta2': data[5], 'beta4': data[6]}
            d[n] = package
    return d


def write_ascii_file(fpath: str, data: dict) -> None:
    """Write a shell correction ASCII file given a filename and a data dictionary. """

    # Write data to file
    with open(fpath, 'w') as fp:
        # Write header line
        fp.write(FILE_HEADER)
        # Loop over data
        for n in data.keys():
            line = data[n].as_tuple
            fp.write(writer.write(line)+"\n")


@dataclass
class Entry(_db.DatabaseEntry):
    """An entry in the shell correction database. """
    
    n      : _c.Nuclide = None # Compound nucleus
    shell  : float      = None # Shell correction [MeV]
    corr   : float      = None # Correction for the deformed nuclear shape [MeV]
    beta2  : float      = None # Quadrupole  parameter of the nuclear ground-state deformation
    beta4  : float      = None # Hexadecapole parameter of the nuclear ground-state deformation
