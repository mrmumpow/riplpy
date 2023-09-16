# -*- coding: utf-8 -*-
"""Python objects which provide access to the giant dipole resonance (GDR) sector of the Reference Input Parameter Library (RIPL). 

@TODO: Finish the longer description. Python 3.7+ is expected to run this code properly.

Examples:
    (1) @TODO: Finish
        $

Todo:
    * Provide more examples of use cases.
    * Test in production.
    
Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

"""

# ========================

# OS
import os

# Collections
from collections import namedtuple

# Dataclasses
from dataclasses import dataclass

# Numpy
import numpy as _np

# RIPLpy
from riplpy.collections import Nuclide

# ========================

GDR_TheoryParameterTuple = namedtuple('GDR_TheoryParameterTuple', 'Z, A, El, E1, W1, E2, W2')

ASCII_FILE_HEADER = "#  Theoretical Giant Dipole Resonance parameters\n#  Z   A El    Eta    E1     W1     E2     W2\n#                   [MeV]  [MeV]  [MeV]  [MeV] \n#--------------------------------------------------\n"

# ========================

@dataclass
class GDR_TheoryParameter(object):
    """A representation of a single theoretical Giant Dipole Resonance (GDR) parameter. """
    
    n  : Nuclide  # The nucleus
    eta: float    # ?
    E1 : float    # Energy [MeV]
    W1 : float    # Width [MeV]
    E2 : float    # Energy [MeV]
    W2 : float    # Width [MeV]

    @property
    def nucleus(self, ) -> Nuclide:
        """Additional reference to the nucleus. """
        return self.n

    @property
    def as_dict(self, ) -> dict:
        """Return the object as a dictionary. """
        return {'nuc': self.nuc, 'eta': self.eta, 'E1': self.E1, 'W1': self.W1, 'E2': self.E2, 'W2': self.W2}

    @property
    def as_ascii_string(self, ) -> str:
        """Return values as a string formatted for the ASCII file. """
        # @TODO: Finish proper format
        return f"{self.nuc.Z:3d} {self.nuc.A:3d} {self.nuc.sym} {self.E1} {self.W1} {self.E2} {self.W2}"

    @property
    def to_tuple(self, ) -> tuple:
        """Return the object as a tuple. """
        return tuple(self.nuc, self.eta, self.E1, self.W1, self.E2, self.W2)

    @property
    def to_list(self, ) -> list:
        """Return the object as a list. """
        return list(self.nuc, self.eta, self.E1, self.W1, self.E2, self.W2)


class GDR_TheoryParameterMarshaller(object):
    """The marshaller for a GDR_TheoryParameter object. It can perform conversions of a GDR_TheoryParameter object to other formats. """

    def to_dict(obj: GDR_TheoryParameter) -> dict:
        """Return the object as a dictionary. """
        return {'nuc': obj.n, 'eta': obj.eta, 'E1': obj.E1, 'W1': obj.W1, 'E2': obj.E2, 'W2': obj.W2}

    def to_ascii_string(obj: GDR_TheoryParameter) -> str:
        """Return values as a string formatted for the standard ASCII file. """
        # @TODO: Finish proper format
        return f"{obj.n.Z:3d} {obj.n.A:3d} {obj.n.sym} {obj.E1} {obj.W1} {obj.E2} {obj.W2}"

    def to_tuple(obj: GDR_TheoryParameter) -> tuple:
        """Return the object as a tuple. """
        return tuple(obj.n, obj.eta, obj.E1, obj.W1, obj.E2, obj.W2)

    def to_list(obj: GDR_TheoryParameter) -> list:
        """Return the object as a list. """
        return list(obj.n, obj.eta, obj.E1, obj.W1, obj.E2, obj.W2)


def read_theory_ascii_file(fpath: str, skiprows: int = 4) -> dict:
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


class GDR_TheoryParameters(object):
    """A set of Giant Dipole Resonance (GDR) parameters from theory. """
    

    def __init__(self, fpath: str) -> None:
        """Initialize the object . """
        self.data = read_theory_ascii_file(fpath)
        
    def __iter__(self, ) -> iter:
        """Return the list of keys for the data property as an iterable. """
        return iter(self.data.keys())

    def insert(self, entry: GDR_TheoryParameter) -> None:
        """Insert an entry into the dataset. """
        d = entry.dict_values
        n = d.pop('n')
        self.data[n] = d
    
    def remove(self, entry: GDR_TheoryParameter) -> None:
        """Remove an entry from the dataset. """
        self.data.pop(entry.n)
        
    def get(self, n: Nuclide) -> dict:
        """Return a dictionary of values for the given nucleus. """
        return self.data[n]

    def as_list(self, sort: bool = False) -> list:
        """Return the dataset as a list of GDR_TheoryParameter objects. """
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
            r.append(GDR_TheoryParameter(k, eta, E1, W1, E2, W2))
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

#gdr = GDR_TheoryParameters(os.path.join("data", "ripl3_gdr-parameters-theor.dat"))
#print(gdr.get(Nuclide(Z=50, A=140)))
