"""

"""


# ========================

# RIPLpy
import riplpy.collections as _c
import riplpy.db as _db
import riplpy.optical as _optical

# ========================

class DeformationDatabase(_db.NuclideDatabase):

    reader: object = _optical.deform.read_ascii_file
    entry : object = _optical.deform.Entry
    writer: object = _optical.deform.write_ascii_file

    @property
    def nuclei(self, ) -> list:
        """Return the unique list of nuclei in the database. """
        return list(set([k[0] for k in self.data.keys()]))

    @property
    def references(self, ) -> list:
        """Return the unique list of references in the database. """
        return list(set([k[1] for k in self.data.keys()]))

    def deformation(self, key: tuple) -> float:
        """Return the mass excess of the requested nucleus (n) and reference (ref) tuple key=(n,ref). """
        return self.data[key]['beta']

    def insert_by_entry(self, entry: object) -> None:
        """Insert a new entry into the database. """
        # Check that a proper entry has been provided
        if isinstance(entry, self.entry):
            # Insert the entry by its nucleus; this may overwrite an existing entry
            self.data[(entry.n, entry.ref)] = entry
        else:
            raise TypeError(f"Entry must be of type = ({type(self.entry)}); given = ({type(entry)})!")

    def remove_by_entry(self, entry: object) -> None:
        """Remove an existing entry in the database. """
        # Check that a proper entry has been provided
        if hasattr(entry, 'n') and hasattr(entry, 'ref'):
            self.data.pop((entry.n, entry.ref))
        else:
            raise Exception("Entry object must have a nucleus property!")
