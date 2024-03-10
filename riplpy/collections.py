# -*- coding: utf-8 -*-
"""Python objects that provide access to commonly used quantities that can be used in or as collections.

Python 3.10+ is expected to run this code properly.

Examples:
    (1) Create a placeholder representation of a nucleus as a Nucleus object::
       $ n = Nucleus()
    (2) Create a representation of 132-Sn as a Nucleus object::
       $ n = Nucleus(Z=50, N=82)
    (3) Create a representation of 132-Sn as a Nuclide object (which accepts more attributes upon init)::
       $ n = Nuclide(Z=50, N=82, attr='this is new')
    (4) Initialize a Nuclide via element name and mass number::
       $ n = Nuclide(sym='Sn', A=132)
    (5) Check the equivalence of a Nucleus and Nuclide object (this comparison only depends on (Z,N) - thus returns True)::
       $ n = Nucleus(Z=50, N=82)
       $ m = Nuclide(Z=50, N=82)
       $ n == m # True
    (6) Print out the symbol name of the Nucleus::
       $ n = Nucleus(Z=48, N=130)
       $ print(n.element_symbol)
    (7) Access the mass number of a Nucleus object::
       $ n = Nucleus(Z=50, N=82)
       $ n.A
    (8) Create a representation of the ground state of 132-Sn as an IsomericNucleus object which contains state information in the 'm' attribute (m=0 by default)::
       $ n = IsomericNucleus(Z=50, N=82)
    (9) Create a representation of the second excited state of 132-Sn::
       $ n = IsomericNucleus(Z=50, N=82, m=2)
    (10) Check the equivalence of a Nucleus and an IsomericNucleus object (these two are not the same)::
       $ n = Nucleus(Z=82, N=126)
       $ m = IsomericNucleus(Z=82, N=126, m=10)
       $ m == n # False
    (11) Check the equivalence of a Nucleus and an IsomericNucleus object when m == 0::
       $ n = Nucleus(Z=82, N=126)
       $ m = IsomericNucleus(Z=82, N=126)
       $ m == n # True
    (12) Create a set of Nucleus-like objects::
       $ n, m, p, q = Nucleus(Z=82, N=126), Nucleus(Z=50, N=82), IsomericNucleus(Z=82, N=126), Nucleus(Z=71, N=111)
       $ s = set([n,m,p,q]) # only contains: n, m and q (since n == p)

Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

"""

# ========================

# Copy
import copy

# Collections
from collections import namedtuple

# Dataclass
from dataclasses import dataclass

# RegEx
import re

# Local Namespace
from .elements import Elements

# ========================

# Tuples that can be used to quickly access properties
ZNTuple              = namedtuple('ZNTuple', 'Z, N')
ZATuple              = namedtuple('ZATuple', 'Z, A')
NATuple              = namedtuple('NATuple', 'N, A')
NucleusTuple         = namedtuple('NucleusTuple', 'Z, N, A')
IsomericNucleusTuple = namedtuple('IsomericNucleusTuple', 'Z, N, A, i')
SymNucleusTuple      = namedtuple('SymNucleusTuple', 'Z, N, A, sym')
NamedNucleusTuple    = namedtuple('NamedNucleusTuple', 'Z, N, A, name')
SymNamedNucleusTuple = namedtuple('SymNamedNucleusTuple', 'Z, N, A, sym, name')


class NucleusBase(object):
    """A base class for Nucleus-like object. 
    
    This class should not be initialized directly. Instead it contains useful methods for extended objects.
    This class assumes that several variables exist:
        cls.Z - Proton number
        cls.N - Neutron number
        cls.A - Mass number
    """


    @property
    def element_symbol(self, ) -> str:
        """Return the element symbol as a string. """
        return Elements.symbol(self.Z)
    
    @property
    def element_name(self, ) -> str:
        """Return the name of the element as a string."""
        return Elements.name(self.Z)

    @property
    def sym(self, ) -> str:
        return self.element_symbol

    def __eq__(self, other) -> bool:
        """Return the equality (bool) of this object with another. """
        return self.Z == other.Z and self.N == other.N

    def __ne__(self, other) -> bool:
        """Return the not-equality (bool) of this object with another. """
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Return a unique (unsafe) hash of a NucleusBase object given the independent variables: (Z,N). 
        
        By default this also assumes a third component (m=0); the ground state.
        """
        return hash((self.Z, self.N, 0))


class Element(object):
    """A class representing a single element. """

    _reserved_kwargs: tuple = ('z', 'symbol', 'sym', 'name')

    def __init__(self, **kwargs) -> None:
        """Initialize the object. """

        # Check if treated as a placeholder
        if len(kwargs) == 0:
            return

        # Create a reduced subset of the initialized kwargs dict
        # These two dictionary should be mutually exlusive
        nuc, kw = self._subset(kwargs)

        # Initialize by possible keyword arguments
        if 'z' in nuc.keys():
            self.Z = int(nuc['z'])
        elif 'sym' in nuc.keys():
            self.Z = Elements.element(nuc['sym'])
            self.N = A - self.Z
        elif 'symbol' in nuc.keys():
            self.Z = Elements.element(nuc['symbol'])
        elif 'name' in nuc.keys():
            self.Z = Elements.element(nuc['name'])
        else:
            raise Exception("Element is not valid!")
        
        # Set provided auxiliary attributes
        for k,v in kw.items():
            setattr(self, k, v)

    def _subset(self, kwargs: dict) -> tuple:
        """Return a tuple of the reduced subset of the provided kwargs dict and the rest. """
        ret = {} # The subset of reserved kwargs
        kw  = copy.deepcopy(kwargs)
        for key in kwargs.keys():
            k = key.lower() # Force to lower case to check against reserved dictionary keys
            if k in self._reserved_kwargs:
                ret[k] = kw.pop(key)
        return ret, kw

    def __lt__(self, other: object) -> bool:
        """Return true if self is strictly smaller than the given (other) object. """
        if self.Z < other.Z:
            return True
        else:
            return False


@dataclass
class Nucleus(NucleusBase):
    """An object representing a nucleus defined by Z-protons and N-neutrons: (Z,N). 

    By default initialization, this object can be used as a placeholder with no (Z,N) provided.
    Otherwise, this object is intended to represent a nucleus with Z protons and N neutrons.
    Besides a simple check upon initialization, this light-weight object offers no further checking methods.
    Caution: be very careful when using hashes with this object, as it is technically mutable. 
    """

    Z: int = None # The proton number of the nucleus
    N: int = None # The neutron number of the nucleus

    @classmethod
    def from_ZA(cls, val: tuple):
        """Initialize the class from (Z,A) tuple. """
        Z, A = val
        N = A - Z
        return cls(Z,N)

    @classmethod
    def from_NA(cls, val: tuple):
        """Initialize the object from (N,A) tuple. """
        N, A = val
        Z = A - N
        return cls(Z,N)

    def __post_init__(self, ) -> None:
        """Perform post-initialization checks. """
        if self.Z is not None and self.N is not None:
            assert self.Z + self.N == self.A

    @property
    def A(self, ) -> int:
        """Return the mass number of the Nucleus. """
        return self.Z + self.N

    @A.setter
    def A(self, val: tuple) -> None:
        """Set the (dependent) mass number given both proton and neutron numbers (Z,N) as a tuple. """
        Z,N = val
        # We provide a bit of validation, mapping the input to an integer
        self.Z = int(Z)
        self.N = int(N)

    def __hash__(self) -> int:
        """Return a unique (unsafe) hash of a NucleusBase object given the independent variables: (Z,N). 
        
        In this object we have to redefine the (unsafe) hash due to it being built of a dataclass.
        By default this also assumes a third component (m=0); the ground state.
        """
        return hash((self.Z, self.N, 0))

    def __str__(self, ) -> str:
        """Return a string representation of the object. """
        return f"<Nucleus(z={self.Z}, n={self.N})>"

    def __repr__(self, ) -> str:
        """Return a string representation of the object which can be used to initialize. """
        return f"Nucleus(z={self.Z}, n={self.N})"


class Nuclide(NucleusBase):
    """A Nucleus-like object which supports a more robust initialization procedure where additional attributes may be set.

       Because additional attributes may be set upon initialization, this object may perform more slowly than a Nucleus object.
       Caution: be very careful when using hashes with this object, as it is technically mutable. 
       Caution: the equivalence of this object with another depends only on the defining attributes: (Z,N).
    """

    _reserved_kwargs: tuple = ('z', 'n', 'a', 'symbol', 'sym', 'name')


    def __init__(self, **kwargs) -> None:
        """Initialize the object. """

        # Check if treated as a placeholder
        if len(kwargs) == 0:
            return
        
        # Create a reduced subset of the initialized kwargs dict
        # These two dictionary should be mutually exlusive
        nuc, kw = self._subset(kwargs)

        # Initialize by possible keyword arguments
        if 'z' in nuc.keys() and 'a' in nuc.keys():
            self.Z = int(nuc['z'])
            self.N = int(nuc['a']) - int(self.Z)
        elif 'z' in nuc.keys() and 'n' in nuc.keys():
            self.Z = int(nuc['z'])
            self.N = int(nuc['n'])
        elif 'n' in nuc.keys() and 'a' in nuc.keys():
            self.N = int(nuc['n'])
            self.Z = int(nuc['a']) - int(self.N)
        elif 'sym' in nuc.keys() and 'a' in nuc.keys():
            A = int(nuc['a'])
            self.Z = Elements.element(nuc['sym'])
            self.N = A - self.Z
        elif 'sym' in nuc.keys() and 'n' in nuc.keys():
            self.N = int(nuc['N'])
            self.Z = Elements.element(nuc['sym'])
        elif 'symbol' in nuc.keys() and 'a' in nuc.keys():
            A = int(nuc['a'])
            self.Z = Elements.element(nuc['symbol'])
            self.N = A - self.Z
        elif 'symbol' in nuc.keys() and 'n' in nuc.keys():
            self.N = int(nuc['N'])
            self.Z = Elements.element(nuc['symbol'])
        elif 'name' in nuc.keys() and 'a' in nuc.keys():
            A = int(nuc['a'])
            self.Z = Elements.element(nuc['name'])
            self.N = A - self.Z
        elif 'name' in nuc.keys() and 'n' in nuc.keys():
            self.N = int(nuc['N'])
            self.Z = Elements.element(nuc['name'])
        else:
            raise Exception("Nucleus is not valid (Z,A) or (Z,N) or (N,A) not given!")

        # Sanity check on nucleus
        assert self.Z + self.N == self.A

        # Set provided auxiliary attributes
        for k,v in kw.items():
            setattr(self, k, v)

    @property
    def A(self, ) -> int:
        """Return the mass number of the Nuclide. """
        return self.Z + self.N

    @classmethod
    def from_string(cls, val: str):
        """Initialize the object from a string. """
        if "-" in val:
            # @TODO: Implement
            pass
        else:
            # Assume of the form '###El'
            lst = []
            for i in re.split('(\d+)', val):
                i = i.strip()
                if len(i) > 0:
                    lst.append(i)
            assert len(lst) == 2
            for v in lst:
                if v.isnumeric():
                    A = int(v)
                else:
                    sym = v
            Z = Elements.element_from_symbol(sym)
            N = A - Z
            return cls(Z=Z, N=N)

    def _subset(self, kwargs: dict) -> tuple:
        """Return a tuple of the reduced subset of the provided kwargs dict and the rest. """
        ret = {} # The subset of reserved kwargs
        kw  = copy.deepcopy(kwargs)
        for key in kwargs.keys():
            k = key.lower() # Force to lower case to check against reserved dictionary keys
            if k in self._reserved_kwargs:
                ret[k] = kw.pop(key)
        return ret, kw

    def __lt__(self, other: object) -> bool:
        """Return true if self is strictly smaller than the given (other) object. """
        if (self.Z, self.A) < (other.Z, other.A):
            return True
        else:
            return False

    def __str__(self, ) -> str:
        """Return a string representation of the object. """
        return f"<Nuclide(z={self.Z}, a={self.A}, symbol={self.element_symbol})>"

    def __repr__(self, ) -> str:
        """Return a string representation of the object which can be used to initialize. """
        return f"Nuclide(z={self.Z}, a={self.A})"


@dataclass
class IsomericNucleus(Nucleus, NucleusBase):
    """An object representing a nucleus that also contains information about an isomeric state.
       
       The object may be initialized by providing proton number (Z), neutron number (N), and isomeric state enumeration (m).

       Caution: the equivalence of this object with another depends only on the defining attributes: (Z,N,m).
    """

    m: int = 0 # By default the state is assumed to be the ground state


    def __post_init__(self, ) -> None:
        """Perform post-initialization checks. """
        super(IsomericNucleus, self).__post_init__()
        # We insist that states are enumerated by the natural numbers
        assert self.m > -1

    def __eq__(self, other) -> bool:
        """Return the equality (bool) of this object with another. """
        test_Z = self.Z == other.Z
        test_N = self.N == other.N
        try:
            m = getattr(other, 'm')
        except AttributeError:
            # Assume ground state
            m = 0
        test_m = self.m == m

        return test_Z and test_N and test_m 

    def __hash__(self) -> int:
        """Return a unique (unsafe) hash of this object. """
        return hash((self.Z, self.N, self.m))

    def __str__(self, ) -> str:
        """Return a string representation of the object. """
        return f"<IsomericNucleus(z={self.Z}, n={self.N}, symbol={self.element_symbol})>"

    def __repr__(self, ) -> str:
        """Return a string representation of the object which can be used to initialize. """
        return f"IsomericNucleus(z={self.Z}, n={self.N}, m={self.m})"

# class IsomericNuclide(Nuclide, metaclass=NucleusMeta):
#     """A Nuclide-like object which handles the special case of isomeric states. """
#     pass
