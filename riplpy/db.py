
from dataclasses import dataclass, fields

@dataclass
class DatabaseEntry(object):
    """A generic database entry. This class is expected to be extended. """

    @property
    def as_list(self, ) -> list:
        """Return a list representation of the object. """
        return [getattr(self, f.name) for f in fields(self.__class__)]

    @property
    def as_tuple(self, ) -> tuple:
        """Return a tuple representation of the object. Intended for writing to file. """
        return tuple(self.as_list)

    @property
    def as_dict(self, ) -> dict:
        """Return a dictionary representation of the object. Useful packaging for other objects. """
        d = {}
        for f in fields(self.__class__):
            d[f.name] = getattr(self, f.name)
        return d

@dataclass
class NuclideDatabaseEntry(DatabaseEntry):

    @property
    def as_tuple(self, ) -> tuple:
        """Return a tuple representation of the object. Intended for writing to file. """
        lst = [self.n.Z, self.n.A, self.n.element_symbol]
        for f in fields(self.__class__):
            if f.name != 'n':
                lst.append(getattr(self, f.name))
        return tuple(lst)


class Database(object):
    """A generic representation of a RIPL database that accesses information from a single ASCII file. """

    reader: object = None # The method to read data from a specified ASCII file
    entry : object = None # The object which represents an entry in the database
    writer: object = None # The method to write data to a specified ASCII file

    def __init__(self, data: dict = {}) -> None:
        """Initialize the object. """
        self.data = data

    def load(self, fpath: str) -> None:
        """Load the database from an ASCII file into the data dictionary. """
        self.data = {}
        data = type(self).reader(fpath) # This call returns the data dictionary, but not yet formatted for the db
        # Loop over the data entries
        for key in data.keys():
            # Properly format each entry for the specified db
            self.data[key] = self.entry(**data[key])

    def save(self, fpath: str) -> None:
        """Save the database to an ASCII file. """
        type(self).writer(fpath, self.data)

    def get(self, key: object) -> object:
        """Return the entry from the database given the key. """
        return self.data[key]

    def set(self, key: object, value: object) -> None:
        """Set the entry in the database given the key and value. """
        self.data[key] = value

    def remove(self, key: object) -> None:
        """Remove an existing entry in the database by providing a key (typically a nucleus-like) object. """
        self.data.pop(key)

    def clear(self, ) -> None:
        """Clear the database. """
        del self.data
        self.data = {}


class NuclideDatabase(Database):
    """Data in this type of RIPL database are accessible via a single nucleus. """

    @property
    def nuclei(self, ) -> list:
        """Return the list of nuclei in the database. """
        return list(self.data.keys())

    def insert_by_entry(self, entry: object) -> None:
        """Insert a new entry into the database. """
        # Check that a proper entry has been provided
        if isinstance(entry, self.entry):
            # Insert the entry by its nucleus; this may overwrite an existing entry
            self.data[entry.n] = entry
        else:
            raise TypeError(f"Entry must be of type = ({type(self.entry)}); given = ({type(entry)})!")

    def remove_by_entry(self, entry: object) -> None:
        """Remove an existing entry in the database. """
        # Check that a proper entry has been provided
        if hasattr(entry, 'n'):
            self.data.pop(entry.n)
        else:
            raise Exception("Entry object must have a nucleus property!")


class ElementDatabase(Database):
    """Data  in this type of RIPL database are accessible through an element number. """

    @property
    def elements(self, ) -> list:
        """Return the list of elements in the database. """
        return list(self.data.keys())

    def insert_by_entry(self, entry: object) -> None:
        """Insert a new entry into the database. """
        # Check that a proper entry has been provided
        if isinstance(entry, self.entry):
            # Insert the entry by its nucleus; this may overwrite an existing entry
            self.data[entry.Z] = entry
        else:
            raise TypeError(f"Entry must be of type = ({type(self.entry)}); given = ({type(entry)})!")

    def remove_by_entry(self, entry: object) -> None:
        """Remove an existing entry in the database. """
        # Check that a proper entry has been provided
        if hasattr(entry, 'Z'):
            self.data.pop(entry.Z)
        elif hasattr(entry, 'sym'):
            self.data.pop(entry.Z)
        elif hasattr(entry, 'symbol'):
            self.data.pop(entry.Z)
        elif hasattr(entry, 'name'):
            self.data.pop(entry.Z)
        else:
            raise Exception("Entry object must have an element number!")
