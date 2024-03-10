

# Collections
from collections import namedtuple as _namedtuple

# Dataclass
from dataclasses import dataclass as _dataclass

# RIPLpy
import riplpy.collections as _c

# ========================

GDR_ParameterTuple = _namedtuple('GDR_ParameterTuple', 'Z, A, El, E1, W1, E2, W2')

# ========================

@_dataclass
class Base_GDR_Parameter(object):
    """A base class for a GDR parameter (can be used for experiment or theory). """

    n  : _c.Nuclide = None # The nucleus
    E1 : float   = None # Associated energy [MeV]
    W1 : float   = None # Associated width [MeV]
    E2 : float   = None # Associated second energy [MeV]
    W2 : float   = None # Associated second width [MeV]

    @property
    def nucleus(self, ) -> _c.Nuclide:
        """Additional reference to the nucleus. """
        return self.n

    @property
    def symbol(self, ) -> str:
        """Return the element symbol. """
        return self.n.element_symbol

    @property
    def first(self, ) -> tuple:
        """Return the first GDR (energy, width) pair as a Python tuple. """
        return (self.E1, self.W1)

    @property
    def second(self, ) -> tuple:
        """Return the second GDR (energy, width) pair as a Python tuple. """
        return (self.E2, self.W2)


@_dataclass
class Theory_GDR_Parameter(Base_GDR_Parameter):
    """A representation of a single theoretical Giant Dipole Resonance (GDR) parameter. """
    
    eta: float = None # The deformation parameter
                      # This parameter is calculated by the diameter along the nuclear symmetry axis / diameter along the axis perpedicular to it

    # @property
    # def as_dict(self, ) -> dict:
    #     """Return the object as a dictionary. """
    #     return {'n': self.n, 'eta': self.eta, 'E1': self.E1, 'W1': self.W1, 'E2': self.E2, 'W2': self.W2}

    # @property
    # def as_ascii_string(self, ) -> str:
    #     """Return values as a string formatted for the ASCII file. """
    #     # @TODO: Finish proper format
    #     return f"{self.n.Z:3d} {self.n.A:3d} {self.n.sym} {self.E1} {self.W1} {self.E2} {self.W2}"

    # @property
    # def as_tuple(self, ) -> tuple:
    #     """Return the object as a tuple. """
    #     return tuple(self.n, self.eta, self.E1, self.W1, self.E2, self.W2)

    # @property
    # def as_list(self, ) -> list:
    #     """Return the object as a list. """
    #     return list(self.n, self.eta, self.E1, self.W1, self.E2, self.W2)

    # def as_list(self, sort: bool = False) -> list:
    #     """Return the dataset as a list of Theory_GDR_Parameter objects. """
    #     # Attempt to sort
    #     if sort:
    #         keys = sorted(self.data.keys())
    #     else:
    #         keys = self.data.keys()
        
    #     # Placeholder return list
    #     r = []
    #     # Loop over data keys and construct list
    #     for k in keys:
    #         eta = self.data[k]['eta']
    #         E1  = self.data[k]['E1']
    #         W1  = self.data[k]['W1']
    #         E2  = self.data[k]['E2']
    #         W2  = self.data[k]['W2']
    #         r.append(Theory_GDR_Parameter(k, eta, E1, W1, E2, W2))
    #     return r

    # def as_numpy_array(self, sort: bool = False) -> _np.array:
    #     """Return the dataset as a Numpy array. """
    #     dtype = {"names": ('Z', 'N', 'A', 'sym', 'eta', 'E1', 'W1', 'E2', 'W2'),
    #              "formats": (_np.int16, _np.int16, _np.int16, object, _np.float, _np.float, _np.float, _np.float, _np.float)}
        
    #     # Attempt to sort
    #     if sort:
    #         keys = sorted(self.data.keys())
    #     else:
    #         keys = self.data.keys()
        
    #     # Placeholder return array
    #     a = _np.empty(0, dtype=dtype)
        
    #     for k in self.data.keys():
    #         Z,N,A,sym = k.Z,k.N,k.A,k.sym
    #         eta = self.data[k]['eta']
    #         E1  = self.data[k]['E1']
    #         W1  = self.data[k]['W1']
    #         E2  = self.data[k]['E2']
    #         W2  = self.data[k]['W2']
    #         v = _np.array((Z,N,A,sym,eta,E1,W1,E2,W2), dtype=dtype)
    #         a = _np.append(a, v)
    #     return a


class Theory_GDR_ParameterMarshaller(object):
    """The marshaller for a Theory_GDR_Parameter object. It can perform conversions of a Theory_GDR_Parameter object to other formats. """

    @staticmethod
    def to_dict(obj: Theory_GDR_Parameter) -> dict:
        """Return the object as a dictionary. """
        return {'n': obj.n, 'eta': obj.eta, 'E1': obj.E1, 'W1': obj.W1, 'E2': obj.E2, 'W2': obj.W2}

    @staticmethod
    def to_ascii_string(obj: Theory_GDR_Parameter) -> str:
        """Return values as a string formatted for the standard ASCII file. """
        # @TODO: Finish proper format
        return f"{obj.n.Z:3d} {obj.n.A:3d} {obj.n.sym} {obj.eta} {obj.E1} {obj.W1} {obj.E2} {obj.W2}"

    @staticmethod
    def to_tuple(obj: Theory_GDR_Parameter) -> tuple:
        """Return the object as a tuple. """
        return tuple(obj.n, obj.eta, obj.E1, obj.W1, obj.E2, obj.W2)

    @staticmethod
    def to_list(obj: Theory_GDR_Parameter) -> list:
        """Return the object as a list. """
        return list(obj.n, obj.eta, obj.E1, obj.W1, obj.E2, obj.W2)

    @staticmethod
    def from_dict(d: dict) -> Theory_GDR_Parameter:
        """Return the object initialized from a dictionary. """
        return Theory_GDR_Parameter(**d)

    @staticmethod
    def from_ascii_string(s: str) -> Theory_GDR_Parameter:
        """Return the object initialized from a string"""
        lst = s.split()
        Z   = int(lst[0])
        A   = int(lst[1])
        eta = lst[3]
        E1  = float(lst[4])
        W1  = float(lst[5])
        E2  = float(lst[6]) 
        W2  = float(lst[7])
        n   = _c.Nuclide(Z=Z, A=A)
        return Theory_GDR_Parameter(n=n, E1=E1, W1=W1, E2=E2, W2=W2, eta=eta)



@_dataclass
class Experimental_GDR_Parameter(Base_GDR_Parameter):
    """A representation of an experimental GDR parameter. """

    CS1      : float = None # Peak cross section of the first peak [mb]
    CS1_error: float = None # Standard deviation of the first peak cross section [mb]
    E1_error : float = None # Standard deviation of the first peak energy [MeV]
    W1_error : float = None # Full width half maximum of the first peak width [MeV]
    CS2      : float = None # Peak cross section of the second peak [mb]
    CS2_error: float = None # Standard deviation of the second peak cross section [mb]
    E2_error : float = None # Standard deviation of the second peak energy [MeV]
    W2_error : float = None # Full width half maximum of the second peak width [MeV]
    Emin     : float = None # Lower energy limit of fitting interval [MeV]
    Emax     : float = None # Upper energy limit of fitting interval [MeV]
    reac     : int   = None # ?
    reference: str   = None # A reference key


@_dataclass
class ExperimentalEntry(Experimental_GDR_Parameter):
    """A representation of a single experimental Giant Dipole Resonance (GDR) parameter entry in RIPL. """

    reac     : int   = None # Reaction flag (valid numbers are 1-10)
    reference: str   = None # References on the experimental data

    def check(self, ) -> None:
        """Perform sanity checks regarding the class variables that define the object. """
        assert self.reac in range(0, 11)


class GammaStrengthFunction(object):
    """A discrete representation of the gamma-ray strength function (GSF) for atomic nuclei. """

    n     : _c.Nuclide # The nucleus associated with the GSF
    energy: list       # The excitation energy in the nucleus [MeV]
    fE1   : list       # The E1 strength function in [mb/MeV]

