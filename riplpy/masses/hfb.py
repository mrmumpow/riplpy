
# Dataclasses
from dataclasses import dataclass

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.collections as _c
import riplpy.db as _db

# ========================

FILE_HEADER = "#\n#  Z   A s fl     Mexp      Err       Mth    beta2   beta4     rhon     rn       an       rhop     rp       ap   \n#                [MeV]     [MeV]     [MeV]                    [fm-3]   [fm]     [fm]     [fm-3]   [fm]     [fm]  \n#-----------------------------------------------------------------------------------------------------------------\n"
FORTRAN_FORMAT   = '(2i4,1x,a2,1x,i1,3f10.3,2f8.3,6f9.4)'
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
            n       = _c.Nuclide(Z=Z, A=A)
            package = {'n': n, 'flag': data[3], 'Mexp': data[4], 'Err': data[5], 'Mth': data[6], 
                       'beta2': data[7], 'beta4': data[8], 'rhon': data[9], 'rn': data[10],
                       'an': data[11], 'rhop': data[12], 'rp': data[13], 'ap': data[14],
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


@dataclass
class Entry(_db.NuclideDatabaseEntry):
    """An entry in the HFB-14 mass database. """

    n     : _c.Nuclide = None # Compound nucleus
    flag  : int        = None # flag corresponding to:
                              #   0 if no experimental data available
                              #   1  for a mass excess recommended by Audi et al. (2007)
                              #   2 for a measured mass from Audi et al. (2007)
    Mexp  : float      = None # Experimental or recommended atomic mass excess [MeV] of Audi et al. (2007) 
    Err   : float      = None # Error on the experimental or recommended atomic mass excess [MeV] of Audi et al. (2007) 
    Mth   : float      = None # Calculated HFB-14 atomic mass excess [MeV]
    beta2 : float      = None # Calculated quadrupole deformation of the nuclear ground-state
    beta4 : float      = None # Calculated hexadecapole deformation of the nuclear ground-state
    rhon  : float      = None # Calculated amplitude of the neutron density distribution [fm^(-3)]
    rn    : float      = None # Calculated radius of the neutron density distribution [fm]
    an    : float      = None # Calculated diffuseness of the neutron density distribution [fm]
    rhop  : float      = None # Calculated amplitude of the proton density distribution [fm^(-3)]
    rp    : float      = None # Calculated radius of the proton density distribution [fm]
    ap    : float      = None # Calculated diffuseness of the proton density distribution [fm]
