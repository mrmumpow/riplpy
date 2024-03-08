
# ========================

# OS
import os as _os

# Dataclasses
from dataclasses import dataclass as _dataclass

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.db as _db
import riplpy.collections as _c

# ========================

__all__ = ('db_ms_file_path', 'db_mk_file_path', 'FILE_MS_HEADER', 'FORTRAN_READ_MS_FORMAT', 'FORTRAN_WRITE_MS_FORMAT', 'FORTRAN_READ_MK_FORMAT', 'FORTRAN_WRITE_MK_FORMAT', 'reader_ms', 'reader_mk', 'writer_ms', 'writer_mk', 'read_mk_ascii_file', 'read_ms_ascii_file', 'write_ms_ascii_file', 'write_mk_ascii_file', 'Entry', 'ExtendedEntry', 'MS_Database', 'MK_Database', 'load_ms', 'load_mk')

# ========================

# Current location
__loc__ = _os.path.dirname(_os.path.realpath(__file__))

db_ms_file_path = _os.path.join(__loc__, "data", "shellcor-ms.dat")
db_mk_file_path = _os.path.join(__loc__, "data", "shellmengoninakajima.dat")

# ========================

FILE_MS_HEADER = "#     Myers-Swiatecki shell corrections \n#  Z   A El     Shell   Defcor  bet2  bet4\n#               [MeV]    [MeV]\n#========================================== \n"
FILE_MK_HEADER = ""
FORTRAN_READ_MS_FORMAT  = '(2i4,1x,a2,2(1x,f8.3),2(f6.3))'
FORTRAN_WRITE_MS_FORMAT = '(2i4,1x,a2,2(1x,f8.3),2(1x,f6.3))'
FORTRAN_READ_MK_FORMAT  = '(2i4,1f8.3)'
FORTRAN_WRITE_MK_FORMAT = '(2i4,1f8.3)'
reader_ms = _ff.FortranRecordReader(FORTRAN_READ_MS_FORMAT)
writer_ms = _ff.FortranRecordWriter(FORTRAN_WRITE_MS_FORMAT)
reader_mk = _ff.FortranRecordReader(FORTRAN_READ_MK_FORMAT)
writer_mk = _ff.FortranRecordWriter(FORTRAN_WRITE_MK_FORMAT)

# ========================


def read_mk_ascii_file(fpath: str) -> dict:
    """Read Mengonina-Kajima shell correction data from an ASCII formatted file and return as a dictionary. """

    # Placeholder dictionary
    d = {}

    # Read data from file
    with open(fpath, 'r') as fp:
        for i, line in enumerate(fp.readlines()):
            # Skip the header line(s)
            if "#" in line[0]:
                continue
            # data    = line.split()
            # Z       = int(data[0])
            # A       = int(data[1])
            data  = reader_mk.read(line)
            Z       = data[0]
            A       = data[1]
            n       = _c.Nuclide(Z=Z, A=A)
            package = {'n': n, 'shell': float(data[2])}
            d[n] = package
    return d


def read_ms_ascii_file(fpath: str) -> dict:
    """Read Myers-Swiatecki shell correction data from an ASCII formatted file and return as a dictionary. """

    # Placeholder dictionary
    d = {}

    # Read data from file
    with open(fpath, 'r') as fp:
        for i, line in enumerate(fp.readlines()):
            # Skip the header line(s)
            if "#" in line[0]:
                continue
            data  = reader_ms.read(line)
            Z       = data[0]
            A       = data[1]
            n       = _c.Nuclide(Z=Z, A=A)
            package = {'n': n, 'shell': data[3], 'corr': data[4], 'beta2': data[5], 'beta4': data[6]}
            d[n] = package
    return d


def write_ms_ascii_file(fpath: str, data: dict) -> None:
    """Write a shell correction ASCII file given a filename and a data dictionary. """

    # Write data to file
    with open(fpath, 'w') as fp:
        # Write header line
        fp.write(FILE_MS_HEADER)
        # Loop over data
        for n in data.keys():
            line = data[n].as_tuple
            fp.write(writer_ms.write(line)+"\n")


def write_mk_ascii_file(fpath: str, data: dict) -> None:
    """Write a shell correction ASCII file given a filename and a data dictionary. """

    # Write data to file
    with open(fpath, 'w') as fp:
        # Write header line
        fp.write(FILE_MK_HEADER)
        # Loop over data
        for n in data.keys():
            line = data[n].as_tuple
            line = f"{line[0]} {line[1]} {line[3]}"
            fp.write(line+"\n")


@_dataclass
class Entry(_db.NuclideDatabaseEntry):
    """An entry in the shell correction database. """
    
    n      : _c.Nuclide = None # Compound nucleus
    shell  : float      = None # Shell correction [MeV]


@_dataclass
class ExtendedEntry(Entry):
    """An extended entry in the shell correction database. """

    corr   : float      = None # Correction for the deformed nuclear shape [MeV]
    beta2  : float      = None # Quadrupole  parameter of the nuclear ground-state deformation
    beta4  : float      = None # Hexadecapole parameter of the nuclear ground-state deformation


class MS_Database(_db.NuclideDatabase):

    reader: object = read_ms_ascii_file
    entry : object = ExtendedEntry
    writer: object = write_ms_ascii_file


class MK_Database(_db.NuclideDatabase):

    reader: object = read_mk_ascii_file
    entry : object = Entry
    writer: object = write_mk_ascii_file


def load_ms() -> MS_Database:
    """Load the database into memeory and return it. """
    return _db.load(MS_Database, db_ms_file_path)


def load_mk() -> MK_Database:
    """Load the database into memeory and return it. """
    return _db.load(MK_Database, db_mk_file_path)
