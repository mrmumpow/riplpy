# -*- coding: utf-8 -*-
"""Python objects which provide access to the giant dipole resonance (GDR) sector of the Reference Input Parameter Library (RIPL). 

Predictions of the Giant Dipole Resonance (GDR) energies and widths for about 6000 nuclei with 14<=Z<=110 lying between the proton and the neutron driplines. 
The GDR is represented in the Goldhaber-Teller model [1] where the neutron and proton densities perform an out-of-phase vibration around their centre of mass. 
The dynamics of the oscillation is assumed to be dominated by the np-interaction [2]. 
The present table gives the GDR energies predicted by [2] with a renormalized np-interaction of strength derived from a least-square fit to the experimental GDR energies [3]. 
The nucleon density distribution and ground-state deformation are taken from the Extended Thomas-Fermi plus Strutinsky Integral (ETFSI) compilation [4,5]. 
The expression for the shell-dependent GDR width is taken from [6] using the newly-determined GDR energies and the ETFSI shell corrections. 
Such predictions include the shell-dependent GDR broadening due to the coupling between the dipole oscillations and the quadrupole surface vibrations. 
Comparison between predicted and experimental GDR energies and widths can be found in [3]. 
In case of deformed nuclei, the GDR splits into two peaks for oscillations parallel to the axis of rotational symmetry and perpendicular to it.

Python 3.10+ is expected to run this code properly.

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

# Functools
from functools import partial as _partial

# Fortran format
import fortranformat as _ff

# RIPLpy
import riplpy.config as _config
import riplpy.collections as _c
import riplpy.db as _db
from . import core as _core

# ========================

__all__ = ('FILE_PATH_KEY', 'LOCAL_FILE_PATH', 'FILE_HEADER', 'FORTRAN_FORMAT', 'reader', 'writer', 'read_ascii_file', 'write_ascii_file', 'Entry', 'Database', 'load')

# ========================

# Path key of the database file as defined in config.py
FILE_PATH_KEY = 'gdr_parameters_theor'
LOCAL_FILE_PATH = _config.get_data_file_path(FILE_PATH_KEY)

# ========================

FILE_HEADER = "#  Theoretical Giant Dipole Resonance parameters\n#  Z   A El    Eta    E1     W1     E2     W2\n#                   [MeV]  [MeV]  [MeV]  [MeV] \n#--------------------------------------------------\n"
FORTRAN_FORMAT = '(2i4,1x,a2,f7.3,4f7.2)'
reader   = _ff.FortranRecordReader(FORTRAN_FORMAT)
writer   = _ff.FortranRecordWriter(FORTRAN_FORMAT)

# ========================

def read_ascii_file(fpath: str) -> dict:
    """Read data from an ASCII file and return a dictionary. """
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
            A     = data[1]
            n       = _c.Nuclide(Z=Z, A=A)
            package = {'n': n, 'eta': data[3], 
                       'E1': data[4], 'W1': data[5], 
                       'E2': data[6], 'W2': data[7],
                      }
            d[n] = package
    return d


def write_ascii_file(fpath: str, data: dict) -> None:
    """Write ASCII file given a filename and a data dictionary. """

    # Write data to file
    with open(fpath, 'w') as fp:
        # Write header line
        fp.write(FILE_HEADER)
        # Loop over data
        for n in data.keys():
            line = data[n].as_tuple
            fp.write(writer.write(line)+"\n")


class Entry(_core.Theory_GDR_Parameter, _db.NuclideDatabaseEntry):
    """An object which represents an entry in the theoretical GDR parameter database. """
    pass


class Database(_db.Database):

    reader: object = read_ascii_file
    entry : object = Entry
    writer: object = write_ascii_file


# Create the local 'load' function with config, database object, and file_path_key pre-filled
load = _partial(_db.loader, config=_config, db_obj=Database, file_path_key=FILE_PATH_KEY)
