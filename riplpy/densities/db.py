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

class BSFG_Database(_db.Database):

    reader: object = _densities.bsfg.read_bsfg_ascii_file
    entry : object = _densities.bsfg.BSFG_Entry
    writer: object = _densities.bsfg.write_bsfg_ascii_file


class CT_Database(BSFG_Database):

    reader: object = _densities.ct.read_ct_ascii_file
    entry : object = _densities.ct.CT_Entry
    writer: object = _densities.ct.write_ct_ascii_file

