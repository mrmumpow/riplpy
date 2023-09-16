# -*- coding: utf-8 -*-
"""Python objects that provide quick access to the RIPL fission databases.

Python 3.10+ is expected to run this code properly.

Examples:
    (1) Load the experimental fission barriers from an ASCII file into memory::
       $ ExperimentalDatabase.load()
    (2) Access the properties of the first fission barrier of 249-Cm in the experimental database::
       $ ExperimentalDatabase.data[Nuclide(Z=96, A=249)].A
    (3) Return a list of tuples of barrier heights from the experimental database::
       $ ExperimentalDatabase.heights

Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

"""

# ========================

# OS
import os as _os

# Copy
import copy as _copy

# Numpy
import numpy as _np

# Fortran format
import fortranformat as _ff

# Local namespace
import riplpy.collections as _c
import riplpy.fission as _f

# ========================

# Current location
__loc__  = _os.path.dirname(_os.path.realpath(__file__))
data_dir = _os.path.join(__loc__, "data")

EXP_DB_ASCII_HEADER   = '#\n#  Z   A  s   Syma    Ea     hwa   Symb    Eb     hwb    Deltaf\n#                   [MeV]   [MeV]        [MeV]   [MeV]    [MeV]\n#--------------------------------------------------------------\n'
EXP_DB_HEADER_LINES   = len(EXP_DB_ASCII_HEADER.split("\n"))
EXP_DB_FORTRAN_FORMAT = '(2i4,1x,a2,1x,2(3x,a2,2f8.2),f9.3)'
EXP_DB_NUMPY_DTYPE    = {'names'  : ('Z', 'N', 'A', 'sym', 'Syma', 'Ea', 'hwa', 'Symb', 'Eb', 'hwb', 'deltaf'), 
                         'formats': (_np.uint16, _np.uint16, _np.uint16, object, object, float, float, object, float ,float, float),
                        }

HFB_DB_ASCII_HEADER   = '# Z   N   A  s     Bin     hwin   alphain deltain  Bout   hwout  alphaout deltaout Bout2  hwout2 alphaout2 deltaout2\n#                 [MeV]   [MeV] [MeV^-1/2] [MeV]  [MeV]   [MeV] [MeV^-1/2] [MeV]  [MeV]   [MeV] [MeV^-1/2] [MeV]\n#-------------------------------------------------------------------------------------------------------------------'
HFB_DB_HEADER_LINES   = len(HFB_DB_ASCII_HEADER.split("\n"))
HFB_DB_FORTRAN_FORMAT = '(3i4,1x,a2,12f8.2)'
HFB_DB_NUMPY_DTYPE    = {'names': ('Z', 'N', 'A', 'sym', 'Bin', 'hwin', 'alphain', 'deltain', 'Bout', 'hwout', 'alphaout', 'deltaout', 'Bout2', 'hwout2', 'alphaout2', 'deltaout2'),
                         'formats': (_np.uint16, _np.uint16, _np.uint16, object, float, float, float, float, float, float, float, float, float, float, float, float),
                        }

# ========================

def parse_float(substr: str) -> float:
    """Return a floating point representation of the substring. """
    try:
        return float(substr)
    except:
        return None


def parse_barrier_sp_sym(substr: str, validate: bool = False) -> float:
    """Return a barrier saddle point symmetry. """
    try:
        # Clean up the string first, and convert all letters to upper case
        ret = str(substr).replace(' ', '').upper()
        if validate:
            if ret not in _f.saddle_shorthand.keys():
                raise Exception(f'Invalid saddle point symmetry ({ret})!')
        return ret
    except:
        return None


class BarrierDictDatabase(object):
    """A meta class with commonly used methods for database additions and removals assuming the data is stored as a dictionary. """
 
    def __init__(self, data: dict = {}) -> None:
        """Initialize the object. """
        self.data = data

    @property
    def nuclei(self, ) -> tuple:
        """A list of nuclei in the database (the keys of cls.data). """
        return tuple(self.data.keys())

    def add_entry(self, n: _c.Nuclide, barrier: _f.DoubleHumpBarrier) -> None:
        """Add an entry to the database for provided nucleus (nuc). """
        self.data[n] = barrier

    def remove_entry(self, nuc: _c.Nuclide) -> None:
        """Remove an entry from the database for the provided nucleus (nuc). """
        del self.data[nuc]


class ExperimentalDatabase(BarrierDictDatabase):
    """An object which represents the RIPL experimental fission database with access via a dictionary. """

    def load(self, version: str = '3') -> None:
        """Load the database information from file into memory. """
        if str(version) == '3':
            self.read_ascii(_os.path.join(data_dir, "empirical-barriers.dat"))
        else:
            raise Exception(f"Version of RIPL ({version}) not supported!")

    def read_ascii(self, fpath: str) -> None:
        """Read data into the database object from an ASCII file. """
        reader = _ff.FortranRecordReader(EXP_DB_FORTRAN_FORMAT)

        with open(fpath, 'r') as fp:
            # Skip header lines
            for _ in range(EXP_DB_HEADER_LINES):
                fp.readline()
            # Read the remainder of the data contents, splitting by n
            for line in fp.readlines():
                section = reader.read(line)
                # Define nucleus
                Z   = section[0]
                A   = section[1]
                sym = section[2].replace(' ', '').capitalize()
                nuc = _c.Nuclide(Z=Z, A=A)
                # Check if nucleus is consistent with RIPL mappings
                if nuc.element_symbol != sym:
                    raise Exception("Nucleus entry inconsistent!")

                # Define first barrier information
                sp_sym_A    = parse_barrier_sp_sym(section[3])
                height_A    = parse_float(section[4])
                curvature_A = parse_float(section[5])
                input_A     = (height_A, curvature_A, sp_sym_A)

                # Define second barrier information
                sp_sym_B    = parse_barrier_sp_sym(section[6])
                height_B    = parse_float(section[7])
                curvature_B = parse_float(section[8])
                input_B     = (height_B, curvature_B, sp_sym_B)

                # Set barriers
                fb_A = _f.ParabolicBarrierWithInfo(*input_A)
                fb_B = _f.ParabolicBarrierWithInfo(*input_B)

                # Define the delta f parameter
                deltaf = parse_float(section[-1])

                # Add entry to the database
                self.add_entry(nuc, _f.DoubleHumpBarrier(fb_A, fb_B, deltaf))

    def write_ascii(self, fpath: str) -> None:
        """Write data in the class dictionary to ASCII file. """
        with open(fpath, 'w') as fp:
            # Write the header
            fp.write(EXP_DB_ASCII_HEADER)
            # Loop over data
            for n, v in self.data.items():
                #@TODO: Finish
                pass

    @property
    def heights(self, ) -> list:
        """Return the first and second barrier heights in the database as a list of tuples (Z,A,F_A,F_B). """
        ret = []
        for nuc in self.data.keys():
            Z, A = nuc.Z, nuc.A
            ret.append((Z,A,self.data[nuc].A.height,self.data[nuc].B.height))
        return ret
    
    @property
    def curvatures(self, ) -> list:
        """Return the first and second barrier curvatures in the database as list of tuples (Z,A,C_A,C_B). """
        ret = []
        for nuc in self.data.keys():
            Z, A = nuc.Z, nuc.A
            ret.append((Z,A,self.data[nuc].A.curvature,self.data[nuc].B.curvature))
        return ret

    @property
    def heights_and_curvatures(self, ) -> list:
        """Return the first and second barrier heights and curvatures in the database as list of tuples (Z,A,F_A,C_A,F_B,C_B). """
        ret = []
        for nuc in self.data.keys():
            Z, A = nuc.Z, nuc.A
            ret.append((Z,A,self.data[nuc].A.height,self.data[nuc].A.curvature,self.data[nuc].B.height,self.data[nuc].B.curvature))
        return ret

    def first_barrier(self, nuc: _c.Nuclide) -> _f.ParabolicBarrierWithInfo:
        """Return the first barrier properties of the provided nucleus (nuc). """
        return self.data[nuc].A
    
    def second_barrier(self, nuc: _c.Nuclide) -> _f.ParabolicBarrierWithInfo:
        """Return the second barrier properties of the provided nucleus (nuc). """
        return self.data[nuc].B

    @property
    def as_structured_numpy_array(self, ) -> _np.array:
        """Return the database as a structured Numpy array. """
        ret = []
        for n, v in self.data.items():
            # Define nucleus information
            Z,N,A,sym = n.Z,n.N,n.A,n.element_symbol
            # First barrier
            Syma, Ea, hwa = v.A.sp_sym, v.A.height, v.A.curvature
            # Second barrier
            Symb, Eb, hwb = v.B.sp_sym, v.B.height, v.B.curvature
            # Deltaf
            deltaf = v.deltaf
            # Append row
            ret.append((Z,N,A,sym,Syma,Ea,hwa,Symb,Eb,hwb,deltaf))
        return _np.array(ret, dtype=EXP_DB_NUMPY_DTYPE)

    @property
    def as_numpy_array(self, ) -> _np.array:
        """Return the database as a Numpy array. """
        ret = []
        for n, v in self.data.items():
            # Define nucleus information
            Z,N,A,sym = n.Z,n.N,n.A,n.element_symbol
            # First barrier
            Syma, Ea, hwa = v.A.sp_sym, v.A.height, v.A.curvature
            # Second barrier
            Symb, Eb, hwb = v.B.sp_sym, v.B.height, v.B.curvature
            # Deltaf
            deltaf = v.deltaf
            # Append row
            ret.append((Z,N,A,sym,Syma,Ea,hwa,Symb,Eb,hwb,deltaf))
        return _np.array(ret, dtype=object)

    @property
    def as_nuclides(self, ) -> list:
        """Return the database as a list of Nuclides. Each nuclide contains the relevant barrier properties. """
        ret = []
        for _n, _v in self.data.items():
            # Copy nucleus to a new memory location
            n = _copy.deepcopy(_n)
            # First barrier
            n.Syma, n.Ea, n.hwa = _v.A.sp_sym, _v.A.height, _v.A.curvature
            # Second barrier
            n.Symb, n.Eb, n.hwb = _v.B.sp_sym, _v.B.height, _v.B.curvature
            # Deltaf
            n.deltaf = _v.deltaf
            ret.append(n)
        return ret


class HFB_Database(BarrierDictDatabase):
    """An object which holds HFB (theoretical) fission barriers with access via a dictionary. """

    def load(self, version: str = '3') -> None:
        """Load the database information from file into memory. """
        if str(version) == '3':
            self.read_ascii(_os.path.join(data_dir, "empirical-hfb-barriers.dat"))
        else:
            raise Exception(f"Version of RIPL ({version}) not supported!")

    def read_ascii(self, fpath: str) -> None:
        """Read data into the database object from an ASCII file. """
        reader = _ff.FortranRecordReader(HFB_DB_FORTRAN_FORMAT)

        with open(fpath, 'r') as fp:
            # Skip header lines
            for _ in range(HFB_DB_HEADER_LINES):
                fp.readline()
            # Read the remainder of the data contents, splitting by n
            for line in fp.readlines():
                section = reader.read(line)
                # Define nucleus
                Z   = section[0]
                A   = section[2]
                sym = section[3].replace(' ', '').capitalize()
                nuc = _c.Nuclide(Z=Z, A=A)
                # Check if nucleus is consistent with RIPL mappings
                if nuc.element_symbol != sym:
                    raise Exception("Nucleus entry inconsistent!")
                
                # Attempt to read barrier information
                barriers = {'A': None, 'B': None, 'C': None}
                columns  = ((4,5,6,7), (8,9,10,11), (12,13,14,15))
                for i,k in enumerate(barriers.keys()):
                    input = []
                    for s in columns[i]:
                        input.append(parse_float(section[s]))
                    barriers[k] = _f.ParabolicBarrierWithTheory(*input)
                
                # Add entry to the database
                self.add_entry(nuc, _f.ThreeParabolicBarriers(**barriers))

    @property
    def heights(self, ) -> list:
        """Return the barrier heights in the database as a list of tuples (Z,A,F_A,F_B,F_C). """
        ret = []
        for nuc in self.data.keys():
            Z, A = nuc.Z, nuc.A
            ret.append((Z,A,self.data[nuc].A.height,self.data[nuc].B.height,self.data[nuc].C.height))
        return ret

    @property
    def curvatures(self, ) -> list:
        """Return the barrier curvatures in the database as list of tuples (Z,A,C_A,C_B,C_C). """
        ret = []
        for nuc in self.data.keys():
            Z, A = nuc.Z, nuc.A
            ret.append((Z,A,self.data[nuc].A.curvature,self.data[nuc].B.curvature,self.data[nuc].C.curvature))
        return ret

    @property
    def as_numpy_array(self, ) -> _np.array:
        """Return the database as a structured Numpy array. """
        ret = []
        for n, v in self.data.items():
            # Define nucleus information
            Z, N, A, sym = n.Z, n.N, n.A, n.element_symbol
            # First barrier
            Bin, hwin, alphain, deltain = v.A.height, v.A.curvature, v.A.alpha, v.A.delta
            # Second barrier
            Bout, hwout, alphaout, deltaout = v.B.height, v.B.curvature, v.B.alpha, v.B.delta
            # Third barrier
            Bout2, hwout2, alphaout2, deltaout2 = v.C.height, v.C.curvature, v.C.alpha, v.C.delta
            ret.append((Z,N,A,sym,Bin,hwin,alphain,deltain,Bout,hwout,alphaout,deltaout,Bout2,hwout2,alphaout2,deltaout2))
        return _np.array(ret, dtype=HFB_DB_NUMPY_DTYPE)

    @property
    def as_nuclides(self, ) -> list:
        """Return the database as a list of Nuclides. Each nuclide contains the relevant barrier properties. """
        ret = []
        for _n, _v in self.data.items():
            # Copy nucleus to a new memory location
            n = _copy.deepcopy(_n)
            # First barrier
            n.Bin, n.hwin, n.alphain, n.deltain = _v.A.height, _v.A.curvature, _v.A.alpha, _v.A.delta
            # Second barrier
            n.Bout, n.hwout, n.alphaout, n.deltaout = _v.B.height, _v.B.curvature, _v.B.alpha, _v.B.delta
            # Third barrier
            n.Bout2, n.hwout2, n.alphaout2, n.deltaout2 = _v.C.height, _v.C.curvature, _v.C.alpha, _v.C.delta
            ret.append(n)
        return ret


#hfbdb = HFB_Database()
#hfbdb.load()
#print(hfbdb.data.keys())
#n = list(hfbdb.data.keys())[0]
#print(hfbdb.data[n])
#print(hfbdb.as_numpy_array)
#print(hfbdb.nuclei)
#print(hfbdb.as_nuclides[0])

# expdb = ExperimentalDatabase()
# expdb.load()
# print(expdb.as_numpy_array)
# n = list(expdb.data.keys())[0]
# print(expdb.data[n])
