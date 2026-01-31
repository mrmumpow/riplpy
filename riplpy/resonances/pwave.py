
# ========================

# Dataclass
from dataclasses import dataclass as _dataclass

# Typing
from typing import ClassVar as _ClassVar

# Functools
from functools import partial as _partial

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.config as _config
import riplpy.collections as _c
import riplpy.db as _db

# ========================

# Path key of the database file as defined in config.py
FILE_PATH_KEY = 'resonances_pwave'
LOCAL_FILE_PATH = _config.get_data_file_path(FILE_PATH_KEY)

# ========================

FILE_HEADER = "#                 Resonance data for p-wave resonances \n# Z El  A   Io     Bn        D1        dD      S1    dS    Gg   dG   Com.\n#                 [MeV]     [keV]     [keV]  [1E-4][1E-4][meV][meV]  &Ref\n#========================================================================\n"
FORTRAN_FORMAT   = '(i3,1x,a2,1x,i3,2x,f3.1,2x,f6.3,2x,2(e8.2,2x),1x,2(f4.2,2x),2(f5.1,1x),1x,a4)'
reader = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer = _ff.FortranRecordWriter(FORTRAN_FORMAT)

# ========================

def _parse_float(value):
    """Parse a float value, returning None for empty/invalid values."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value) if value == value else None  # NaN check
    s = str(value).strip()
    if s == '' or s == '****' or s == '*':
        return None
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def read_ascii_file(fpath: str) -> dict:
    """Read P-wave data from an ASCII file and return a dictionary. """
    # Placeholder dictionary
    d = {}

    # Read data from file
    with open(fpath, 'r') as fp:
        for i, line in enumerate(fp.readlines()):
            # Skip the header line(s)
            if "#" in line[0]:
                continue
            data  = reader.read(line)
            Z     = data[0]
            # @TODO: Inconsistent column ordering; this needs to be fixed in the ASCII file
            A = data[2]
            n       = _c.Nuclide(Z=Z, A=A)
            package = {
                'n': n,
                'Io': _parse_float(data[3]),
                'Bn': _parse_float(data[4]),
                'D': _parse_float(data[5]),
                'Derr': _parse_float(data[6]),
                'Str': _parse_float(data[7]),
                'Serr': _parse_float(data[8]),
                'Gam': _parse_float(data[9]),
                'Gerr': _parse_float(data[10]),
                'ref': data[11].strip() if data[11] else '',
            }
            d[n] = package
    return d


def _format_value(value, fmt_type, width, decimals=None):
    """Format a value for writing, handling None as blank spaces.

    Args:
        value: The value to format
        fmt_type: 'i' for integer, 'f' for float, 'e' for exponential, 'a' for string
        width: Total field width
        decimals: Number of decimal places (for float/exponential)
    """
    if value is None:
        return ' ' * width

    if fmt_type == 'i':
        return f"{int(value):>{width}d}"
    elif fmt_type == 'f':
        return f"{float(value):>{width}.{decimals}f}"
    elif fmt_type == 'e':
        return f"{float(value):>{width}.{decimals}E}"
    elif fmt_type == 'a':
        return f"{str(value):<{width}}"
    return str(value)


def write_ascii_file(fpath: str, data: dict) -> None:
    """Write P-wave ASCII file given a filename and a data dictionary. """

    # Write data to file
    with open(fpath, 'w') as fp:
        # Write header line
        fp.write(FILE_HEADER)
        # Loop over data
        for n in data.keys():
            entry = data[n]
            # Format: Z El A  Io  Bn  D  Derr  Str Serr Gam Gerr ref
            # Build line manually to handle None values
            line_parts = [
                _format_value(entry.n.Z, 'i', 3),           # Z
                ' ',                                         # 1x
                f"{entry.n.element_symbol:>2}",             # El (a2)
                ' ',                                         # 1x
                _format_value(entry.n.A, 'i', 3),           # A
                '  ',                                        # 2x
                _format_value(entry.Io, 'f', 3, 1),         # Io (f3.1)
                '  ',                                        # 2x
                _format_value(entry.Bn, 'f', 6, 3),         # Bn (f6.3)
                '  ',                                        # 2x
                _format_value(entry.D, 'e', 8, 2),          # D (e8.2)
                '  ',                                        # 2x
                _format_value(entry.Derr, 'e', 8, 2),       # Derr (e8.2)
                '  ',                                        # 2x
                ' ',                                         # 1x
                _format_value(entry.Str, 'f', 4, 2),        # Str (f4.2)
                '  ',                                        # 2x
                _format_value(entry.Serr, 'f', 4, 2),       # Serr (f4.2)
                '  ',                                        # 2x
                _format_value(entry.Gam, 'f', 5, 1),        # Gam (f5.1)
                ' ',                                         # 1x
                _format_value(entry.Gerr, 'f', 5, 1),       # Gerr (f5.1)
                ' ',                                         # 1x
                ' ',                                         # 1x
                _format_value(entry.ref, 'a', 4),           # ref (a4)
            ]
            fp.write(''.join(line_parts) + "\n")


@_dataclass
class Entry(_db.NuclideDatabaseEntry):
    """An entry in the neutron resonance database.

    Contains s-wave or p-wave neutron resonance parameters from
    evaluated experimental data.

    Attributes:
        n: Target nucleus (Nuclide object with Z, A, N properties)
        Io: Ground state spin of target nucleus
        Bn: Neutron binding energy [MeV]
        D: Average resonance spacing [keV]
        Derr: Uncertainty on D [keV]
        Str: Neutron strength function [10^-4]
        Serr: Uncertainty on Str [10^-4]
        Gam: Average radiative width [meV]
        Gerr: Uncertainty on Gam [meV]
        ref: Reference key
    """

    n     : _c.Nuclide = None
    Io    : float      = None
    Bn    : float      = None
    D     : float      = None
    Derr  : float      = None
    Str   : float      = None
    Serr  : float      = None
    Gam   : float      = None
    Gerr  : float      = None
    ref   : str        = None

    # Field descriptions for help/info display
    _field_info: _ClassVar[dict] = {
        'n': 'Target nucleus',
        'Io': 'Ground state spin of target nucleus',
        'Bn': 'Neutron binding energy [MeV]',
        'D': 'Average resonance spacing [keV]',
        'Derr': 'Uncertainty on D [keV]',
        'Str': 'Neutron strength function [10^-4]',
        'Serr': 'Uncertainty on Str [10^-4]',
        'Gam': 'Average radiative width [meV]',
        'Gerr': 'Uncertainty on Gam [meV]',
        'ref': 'Reference key',
    }

    @property
    def as_tuple(self) -> tuple:
        """Return a tuple representation matching the ASCII file format: Z, El, A, Io, Bn, D, Derr, Str, Serr, Gam, Gerr, ref"""
        return (self.n.Z, self.n.element_symbol, self.n.A, self.Io, self.Bn, self.D, self.Derr, self.Str, self.Serr, self.Gam, self.Gerr, self.ref)


class Database(_db.NuclideDatabase):

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


# Create the local 'load' function with config, database object, and file_path_key pre-filled
load = _partial(_db.loader, config=_config, db_obj=Database, file_path_key=FILE_PATH_KEY)
