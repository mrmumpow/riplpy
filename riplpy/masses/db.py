"""

"""


# ========================

# RIPLpy
import riplpy.collections as _c
import riplpy.db as _db
import riplpy.masses as _masses

# ========================

class MassDatabase(_db.NuclideDatabase):

    def mass_excess(self, n: _c.Nuclide) -> float:
        """Return the mass excess of the requested nucleus (n). """
        return self.data[n]['Mth']


class FRDM95Database(MassDatabase):

    reader: object = _masses.frdm.read_ascii_file
    entry : object = _masses.frdm.Entry
    writer: object = _masses.frdm.write_ascii_file


class HFB14Database(MassDatabase):

    reader: object = _masses.hfb.read_ascii_file
    entry : object = _masses.hfb.Entry
    writer: object = _masses.hfb.write_ascii_file


class NaturalAbundancesDatabase(_db.NuclideDatabase):

    reader: object = _masses.ab.read_ascii_file
    entry : object = _masses.ab.Entry
    writer: object = _masses.ab.write_ascii_file
