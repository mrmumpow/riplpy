
from dataclasses import dataclass, fields

@dataclass
class DatabaseEntry(object):
    """A generic database entry. This class is expected to be extended. """

    @property
    def as_list(self, ) -> list:
        """Return a list representation of the object. Useful for writing to file. """
        return [getattr(self, f.name) for f in fields(self.__class__)]

    @property
    def as_tuple(self, ) -> tuple:
        """Return a tuple representation of the object. Useful for writing to file. """
        return tuple(self.as_list)

    @property
    def as_dict(self, ) -> dict:
        """Return a dictionary representation of the object. Useful packaging for other objects. """
        d = {}
        for f in fields(self.__class__):
            d[f.name] = getattr(self, f.name)
        return d


class Database(object):
    """A generic representation of a RIPL database that accesses information from a single ASCII file. 
    
    Data in all RIPL databases are associated with a single nucleus.
    """

    reader: object = None # The method to read data from a specified ASCII file
    entry : object = None # The object which represents an entry in the database
    writer: object = None # The method to write data to a specified ASCII file

    def __init__(self, data: dict = {}) -> None:
        """Initialize the object. """
        self.data = data

    @property
    def nuclei(self, ) -> list:
        """Return the list of nuclei in the database. """
        return list(self.data.keys())

    def load(self, fpath: str) -> None:
        """Load the database from an ASCII file into the data dictionary. """
        data = type(self).reader(fpath) # This call returns the data dictionary, but not yet formatted for the db
        # Loop over the data entries
        for n in data.keys():
            # Properly format each entry for the specified db
            self.data[n] = self.entry(**data[n])

    def save(self, fpath: str) -> None:
        """Save the database to an ASCII file. """
        type(self).writer(fpath, self.data)

    def get(self, key: object) -> object:
        """Return the entry from the database given the key. """
        return self.data[key]

    def set(self, key: object, value: object) -> None:
        """Set the entry in the database given the key and value. """
        self.data[key] = value

    def insert(self, entry: object) -> None:
        """Insert a new entry into the database. """
        # Check that a proper entry has been provided
        if isinstance(entry, self.entry):
            # Insert the entry by its nucleus; this may overwrite an existing entry
            self.data[entry.n] = entry
        else:
            raise TypeError(f"Entry must be of type = ({type(self.entry)}); given = ({type(entry)})!")

    def remove(self, entry: object) -> None:
        """Remove an existing entry in the database. """
        # Check that a proper entry has been provided
        if hasattr(entry, 'n'):
            self.data.pop(entry.n)
        else:
            raise Exception("Entry object must have a nucleus property!")

    def remove_by_nucleus(self, n: object) -> None:
        """Remove an existing entry in the database by providing a nucleus-like object. """
        self.data.pop(n)
