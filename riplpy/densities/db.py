# Example usage: 

# d = read_bsfg_ascii_file("data/level-densities-bfmeff.dat")
# print(d)

# bsfg = BSFG_Database()
# bsfg.load("data/level-densities-bfmeff.dat")
# print(bsfg.data)
# bsfg.save("a-test.dat")

# ========================

# RIPLpy
import riplpy.db as _db
import riplpy.densities as _densities

# ========================

class BSFG_Database(_db.NuclideDatabase):

    reader: object = _densities.bsfg.read_ascii_file
    entry : object = _densities.bsfg.Entry
    writer: object = _densities.bsfg.write_ascii_file


class CT_Database(BSFG_Database):

    reader: object = _densities.ct.read_ascii_file
    entry : object = _densities.ct.Entry
    writer: object = _densities.ct.write_ascii_file


class EGSM_Database(_db.NuclideDatabase):

    reader: object = _densities.egsm.read_ascii_file
    entry : object = _densities.egsm.Entry
    writer: object = _densities.egsm.write_ascii_file


class EGSM_NormDatabase(_db.ElementDatabase):

    reader: object = _densities.egsm_norm.read_ascii_file
    entry : object = _densities.egsm_norm.Entry
    writer: object = _densities.egsm_norm.write_ascii_file


class ShellCorrDatabase(_db.NuclideDatabase):

    reader: object = _densities.shell_corr.read_ascii_file
    entry : object = _densities.shell_corr.Entry
    writer: object = _densities.shell_corr.write_ascii_file
