
"""
Level density parameters for the BSFG model without explicit treatment of collective effects. 
The parameters are obtained by fitting the Fermi-gas model formula both to the RIPL II recommended spacings of s-wave neutron resonances D0 and to the cumulative number of low-lying levels evaluated from the analysis of nuclear levels. 
Since the goal is to reproduce as well as possible both the discrete levels and the D0 values, the adopted parameters do not generally provide a perfect fit of D0. Instead, we obtain a theoretical value Dth. 
Therefore, uncertainty aerr is deduced by fitting Dth+Derr or Dth-Derr (See TECHDOC for more explanations). 

"""


# Dataclasses
from dataclasses import dataclass

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.collections as _c

# ========================

BSFG_FILE_HEADER = "   Z  A  El   I0    Bn       D0        Derr    Nlow  Ulow   Ntop  Utop      dW      gamma      ainf     aerr    pairing\n"
BSFG_FORTRAN_FORMAT = '(2i4,1x,a2,1x,f4.1,2x,f6.3,1x,1pe10.3,1x,1pe10.3,0p,1x,i3,2x,f6.3,2x,i3,2x,f6.3,3f10.5,f8.3,1f10.5)'
bsfg_reader = _ff.FortranRecordReader(BSFG_FORTRAN_FORMAT)
bsfg_writer = _ff.FortranRecordWriter(BSFG_FORTRAN_FORMAT)

# ========================

def read_bsfg_ascii_file(fpath: str) -> dict:
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
            data  = bsfg_reader.read(line)
            Z       = data[0]
            A       = data[1]
            n       = _c.Nuclide(Z=Z, A=A)
            package = {'n': n, 'Io': data[3], 'Bn': data[4], 'Do': data[5], 'Derr': data[6], 'Nlow': data[7], 'Ulow': data[8],
                       'Ntop': data[9], 'Utop': data[10], 'dW': data[11], 'gamma': data[12], 'ainf': data[13], 'aerr': data[14],
                       'pairing': data[15],
                      }
            d[n] = package
    return d


def write_bsfg_ascii_file(fpath: str, data: dict) -> None:
    """Write a Back-Shifted Fermi-Gas (BSFG) ASCII file given a filename and a data dictionary. """

    # Write data to file
    with open(fpath, 'w') as fp:
        # Write header line
        fp.write(BSFG_FILE_HEADER)
        # Loop over data
        for n in data.keys():
            line = (n.Z, n.A, n.sym, data[n].Io, data[n].Bn, data[n].Do, data[n].Derr, data[n].Nlow, data[n].Ulow, data[n].Ntop, data[n].Utop, data[n].dW, data[n].gamma, data[n].ainf, data[n].aerr, data[n].pairing)
            fp.write(bsfg_writer.write(line)+"\n")


@dataclass
class BSFG_Entry(object):
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

