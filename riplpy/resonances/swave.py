
# ========================

# OS
import os as _os

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.collections as _c
import riplpy.db as _db
from . import pwave as _pwave

# ========================

# Relative path to database file
local_file_path = _os.path.join('resonances', 'resonances0.dat')

# ========================

FILE_HEADER = "#                 Resonance data for s-wave resonances \n# Z El  A   Io     Bn        D0        dD      S0    dS    Gg   dG   Com.\n#                 [MeV]     [keV]     [keV]  [1E-4][1E-4][meV][meV]  &Ref\n#========================================================================\n"
FORTRAN_FORMAT   = '(i3,1x,a2,1x,i3,2x,f3.1,2x,f6.3,2x,2(e8.2,2x),1x,2(f4.2,2x),2(f4.1,1x),2x,a4)'
reader = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer = _ff.FortranRecordWriter(FORTRAN_FORMAT)

# ========================

read_ascii_file = _pwave.read_ascii_file
write_ascii_file = _pwave.write_ascii_file

Entry = _pwave.Entry


class Database(_db.NuclideDatabase):

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


def load(directory: str = None, file_path: str = None) -> Database:
    """Load the database into memory and return it. """
    if file_path is not None:
        return _db.load(Database, file_path)
    elif directory is not None:
        file_path = _os.path.join(directory, local_file_path)
        return _db.load(Database, file_path)
