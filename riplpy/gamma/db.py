

# ========================

# Numpy
import numpy as _np

# Fortran format
import fortranformat as _ff

# RIPLpy
from riplpy.collections import Nuclide
from riplpy.gamma.gdr import Theory_GDR_Parameter

# ========================

LINE1_FORMAT = '(2X,I2,1X,I3,1X,A2,1X,I2,1X,F5.2,2X,F5.1,2X,F5.2,2X,F5.2,2X,F5.1,3X,F5.2,1X,F4.1,3X,F4.1,2X,A5)'
LINE2_FORMAT = '(15X,F5.2,2X,F5.1,2X,F5.2,2X,F5.2,2X,F5.1,3X,F5.2)'

# ========================

line1_reader = _ff.FortranRecordReader(LINE1_FORMAT)
line2_reader = _ff.FortranRecordReader(LINE2_FORMAT)

# ========================

def read_expermintal_ascii_file(fpath: str) -> dict:
    """Read the GDR experimental file and return data as a Python dictionary. """

    # Data placeholder
    d = {}

    # Counter for number of header lines
    header_lines = 0

    # Read file
    with open(fpath, 'r') as fp:
        # Skip the header
        flag = False
        for i,line in enumerate(fp.readlines()):
            if "#" in line[0]:
                header_lines += 1
                continue
            # Define even / odd structure of data
            j = i - header_lines
            print(line, i, j)
            if j % 2 == 0:
                data = line1_reader.read(line)
                Z    = int(data[0])
                A    = int(data[1])
                n    = Nuclide(Z=Z, A=A)
                reac = int(data[3])
                E1   = float(data[4])
                CS1  = float(data[5])
                W1   = float(data[6])
                try:
                    E2  = float(data[7])
                    CS2 = float(data[8])
                    W2  = float(data[9])
                except:
                    E2  = None
                    CS2 = None
                    W2  = None
                Emin = float(data[10])
                Emax = float(data[11])
                ref  = data[12]
                flag = False
            else:
                data = line2_reader.read(line)
                E1_error  = float(data[0])
                CS1_error = float(data[1])
                W1_error  = float(data[2])
                try:
                    E2_error  = float(data[3])
                    CS2_error = float(data[4])
                    W2_error  = float(data[5])
                except:
                    E2_error  = None
                    CS2_error = None
                    W2_error  = None
                flag = True
            if flag:
                packet = {'n': n, 'E1': E1, 'E2': E2, 'W1': W1, 'W2': W2, 'CS1': CS1, 'CS2': CS2,
                          'E1_error': E1_error, 'E2_error': E2_error, 'W1_error': W1_error, 'W2_error': W2_error,
                          'CS1_error': CS1_error, 'CS2_error': CS2_error, 'Emin': Emin, 'Emax': Emax, 
                          'reac': reac, 'reference': ref,
                         }
                d[n] = packet
    return d


def read_theory_ascii_file(fpath: str, ) -> dict:
    """Read the GDR theory file and return data as a Python dictionary. """
    
    # Data placeholder
    d = {}

    # Read file
    with open(fpath, 'r') as fp:
        # Skip the header
        for line in fp.readlines():
            if "#" in line[0]:
                continue
            # Read the rest of the file
            line = line.split()
            Z   = int(line[0])
            A   = int(line[1])
            sym = line[2]
            eta = float(line[3])
            E1  = float(line[4])
            W1  = float(line[5])
            E2  = float(line[6])
            W2  = float(line[7])
            nuc = Nuclide(Z=Z, A=A)
            if nuc.sym != sym:
                raise Exception(f"Nucleus symbol ({sym}) incorrect!")
            d[nuc] = {'eta': eta, 'E1': E1, 'W1': W1, 'E2': E2, 'W2': W2}
    return d


class Theory_GDR_Parameters(object):
    """A set of Giant Dipole Resonance (GDR) parameters from theory. """
    

    def __init__(self, fpath: str) -> None:
        """Initialize the object . """
        self.data = read_theory_ascii_file(fpath)
        
    def __iter__(self, ) -> iter:
        """Return the list of keys for the data property as an iterable. """
        return iter(self.data.keys())

    def insert(self, entry: Theory_GDR_Parameter) -> None:
        """Insert an entry into the dataset. """
        d = entry.dict_values
        n = d.pop('n')
        self.data[n] = d
    
    def remove(self, entry: Theory_GDR_Parameter) -> None:
        """Remove an entry from the dataset. """
        self.data.pop(entry.n)
        
    def get(self, n: Nuclide) -> dict:
        """Return a dictionary of values for the given nucleus. """
        return self.data[n]

    def as_list(self, sort: bool = False) -> list:
        """Return the dataset as a list of Theory_GDR_Parameter objects. """
        # Attempt to sort
        if sort:
            keys = sorted(self.data.keys())
        else:
            keys = self.data.keys()
        
        # Placeholder return list
        r = []
        # Loop over data keys and construct list
        for k in keys:
            eta = self.data[k]['eta']
            E1  = self.data[k]['E1']
            W1  = self.data[k]['W1']
            E2  = self.data[k]['E2']
            W2  = self.data[k]['W2']
            r.append(Theory_GDR_Parameter(k, eta, E1, W1, E2, W2))
        return r

    def as_numpy_array(self, sort: bool = False) -> _np.array:
        """Return the dataset as a Numpy array. """
        dtype = {"names": ('Z', 'N', 'A', 'sym', 'eta', 'E1', 'W1', 'E2', 'W2'),
                 "formats": (_np.int16, _np.int16, _np.int16, object, _np.float, _np.float, _np.float, _np.float, _np.float)}
        
        # Attempt to sort
        if sort:
            keys = sorted(self.data.keys())
        else:
            keys = self.data.keys()
        
        # Placeholder return array
        a = _np.empty(0, dtype=dtype)
        
        for k in self.data.keys():
            Z,N,A,sym = k.Z,k.N,k.A,k.sym
            eta = self.data[k]['eta']
            E1  = self.data[k]['E1']
            W1  = self.data[k]['W1']
            E2  = self.data[k]['E2']
            W2  = self.data[k]['W2']
            v = _np.array((Z,N,A,sym,eta,E1,W1,E2,W2), dtype=dtype)
            a = _np.append(a, v)
        return a

#gdr = Theory_GDR_Parameters(os.path.join("data", "ripl3_gdr-parameters-theor.dat"))
#print(gdr.get(Nuclide(Z=50, A=140)))

#d = read_expermintal_ascii_file("data/ripl3-gdr-parameters&errors-exp-SLO.dat")
#print(d)