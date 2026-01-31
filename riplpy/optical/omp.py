
# Dataclasses
from dataclasses import dataclass

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.collections as _c
import riplpy.db as _db

# ========================

FILE_HEADER = ""
FORTRAN_FORMAT   = ""
ENTRY_HEADER = "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
#reader   = _ff.FortranRecordReader(FORTRAN_FORMAT)
#writer   = _ff.FortranRecordWriter(FORTRAN_FORMAT)

# ========================

def read_ascii_file(fpath: str) -> dict:
    """Read data from an ASCII file and return a dictionary. """
    # Placeholder dictionary
    d = {}

    # Read data from file
    with open(fpath, 'r') as fp:
        j = 0 # entry index
        for i, line in enumerate(fp.readlines()):
            if "+++++++++++" not in line:
                end_flag = False
                if j == 0:
                    ripl_id = int(line)
                    desc    = ""
                    # elow    = None
                    # ehigh   = None
                    j += 1
                    print('J=0', line)
                elif j > 0:
                    if line[0].isspace():
                        if len(line.replace("\n", "")) > 0:
                            #j += 1
                            print(j)
                            if j == 1:
                                # Energy range
                                tmp = line.split()
                                Elow, Ehigh = float(tmp[0]), float(tmp[1])
                                j += 1
                            elif j == 2:
                                # Proton range
                                tmp = line.split()
                                Zlow, Zhigh = float(tmp[0]), float(tmp[1])
                                j += 1
                            elif j == 3:
                                # Mass number range
                                tmp = line.split()
                                Alow, Ahigh = float(tmp[0]), float(tmp[1])
                                j += 1
                            elif j == 4:
                                # Unknown set of 5 numbers
                                numbers = list(map(int, line.split()))
                                j += 1
                            elif j == 5:
                                something = float(line.strip())
                                j += 1
                            # Data section
                            print('DATA', line)
                    else:
                        print('DESC', line)
                        desc += line
            else:
                end_flag = True
                j = 0
                print('END', line)
                d[ripl_id] = {'Elow': Elow, 'Ehigh': Ehigh, 'Zlow': Zlow, 'Zhigh': Zhigh, 'Alow': Alow, 'Ahigh': Ahigh, 
                             }
            #d[n] = package
            if i > 1000:
                stop
    return d

read_ascii_file("data/om-parameter-u.dat")


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
    """An entry in the FRDM1995 mass database. """

    n     : _c.Nuclide = None # Compound nucleus
    flag  : int        = None # flag corresponding to:
                              #   0 if no experimental data available
                              #   1  for a mass excess recommended by Audi et al. (2007)
                              #   2 for a measured mass from Audi et al. (2007)
    Mexp  : float      = None # Experimental or recommended atomic mass excess [MeV] of Audi et al. (2007) 
    Err   : float      = None # Error on the experimental or recommended atomic mass excess [MeV] of Audi et al. (2007) 
    Mth   : float      = None # Calculated FRDM atomic mass excess [MeV]
    Emic  : float      = None # Calculated FRDM microscopic energy [MeV]
    beta2 : float      = None # Calculated quadrupole deformation of the nuclear ground-state
    beta3 : float      = None # Calculated octupole deformation of the nuclear ground-state
    beta4 : float      = None # Calculated hexadecapole deformation of the nuclear ground-state
    beta6 : float      = None # Calculated hexacontatetrapole deformation of the nuclear ground-state
