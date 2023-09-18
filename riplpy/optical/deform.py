
# Dataclasses
from dataclasses import dataclass

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.collections as _c
import riplpy.db as _db

# ========================

FILE_HEADER = "#       Excited-level deformation parameters\n#  Z   A El        Ex     J  P L       beta  Reference   \n#                [MeV]\n#------------------------------------------------------  \n"
FORTRAN_FORMAT   = "(2i4,1x,a2,1x,f10.6,1x,f4.1,i3,i2,1x,f10.6,2x,a13)"
reader   = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer   = _ff.FortranRecordWriter(FORTRAN_FORMAT)

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
            n     = _c.Nuclide(Z=Z, A=A)
            ref   = data[8].strip()
            package = {'n': n, 'Ex': data[3], 'spin': data[4], 'parity': data[5], 'order': data[6], 'beta': data[7], 'ref': ref}
            d[(n,ref)] = package
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


@dataclass
class Entry(_db.NuclideDatabaseEntry):
    """An entry in the optical model deformation database. """

    n     : _c.Nuclide = None # Compound nucleus
    Ex    : float      = None # Energy of the excited-level [MeV]
    spin  : float      = None # Spin of the excited-level (if the spin is unknown, this field is left blank)
    parity: float      = None # Parity of the excited-level (if the parity is unknown, parity = 0)
    order : int        = None # Order of the deformation parameter, beta
    beta  : float      = None # Deformation parameter beta (of a particular order)
    ref   : str        = None # Reference flag for where the data came from
