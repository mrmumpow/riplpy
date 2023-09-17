

# Dataclasses
from dataclasses import dataclass

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.collections as _c
import riplpy.densities as _densities

# ========================

CT_FILE_HEADER = "   Z  A  El   I0    Bn       D0        Derr    Nlow  Ulow   Ntop  Utop      dW      gamma      ainf     aerr    pairing   Ematch      E0         T\n"
CT_FORTRAN_FORMAT   = '(2i4,1x,a2,1x,f4.1,2x,f6.3,1x,1pe10.3,1x,1pe10.3,0p,1x,i3,2x,f6.3,2x,i3,2x,f6.3,3f10.5,f8.3,4f10.5)'
ct_reader   = _ff.FortranRecordReader(CT_FORTRAN_FORMAT)
ct_writer   = _ff.FortranRecordWriter(CT_FORTRAN_FORMAT)

# ========================

def read_ct_ascii_file(fpath: str) -> dict:
    """Read Constant Temperature (CT) data from an ASCII file and return a dictionary. """
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
            data  = ct_reader.read(line)
            Z       = data[0]
            A       = data[1]
            n       = _c.Nuclide(Z=Z, A=A)
            package = {'n': n, 'Io': data[3], 'Bn': data[4], 'Do': data[5], 'Derr': data[6], 'Nlow': data[7], 'Ulow': data[8],
                       'Ntop': data[9], 'Utop': data[10], 'dW': data[11], 'gamma': data[12], 'ainf': data[13], 'aerr': data[14],
                       'pairing': data[15], 'Ematch': data[16], 'E0': data[17], 'T': data[18],
                      }
            d[n] = package
    return d


def write_ct_ascii_file(fpath: str, data: dict) -> None:
    """Write a Constant Temperature (CT) ASCII file given a filename and a data dictionary. """

    # Write data to file
    with open(fpath, 'w') as fp:
        # Write header line
        fp.write(CT_FILE_HEADER)
        # Loop over data
        for n in data.keys():
            line = (n.Z, n.A, n.sym, data[n].Io, data[n].Bn, data[n].Do, data[n].Derr, data[n].Nlow, data[n].Ulow, data[n].Ntop, data[n].Utop, data[n].dW, data[n].gamma, data[n].ainf, data[n].aerr, data[n].pairing, data[n].Ematch, data[n].E0, data[n].T)
            fp.write(ct_writer.write(line)+"\n")


@dataclass
class CT_Entry(_densities.bsfg.BSFG_Entry):
    """An entry in the Constant Temperature (CT) database. """

    Ematch: float = None # Energy at which the low and high energy formulae match [MeV]
    E0    : float = None # Energy shift for the low-energy approach [MeV]
    T     : float = None # Temperature for the low-energy approach [MeV]
