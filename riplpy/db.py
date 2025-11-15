# -*- coding: utf-8 -*-
"""The base objects which define access to RIPL databases. 

Python 3.10+ is expected to run this code properly.

Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

"""

from dataclasses import dataclass as _dataclass, fields as _fields
from riplpy.exceptions import NucleusNotFoundError, ElementNotFoundError, FileFormatError

__all__ = ('DatabaseEntry', 'NuclideDatabaseEntry', 'Database', 'NuclideDatabase', 'ElementDatabase', '_DbAccessor', 'load')

@_dataclass
class DatabaseEntry:
    """A generic database entry. This class is expected to be extended. """

    @property
    def as_list(self, ) -> list:
        """Return a list representation of the object. """
        return [getattr(self, f.name) for f in _fields(self.__class__)]

    @property
    def as_tuple(self, ) -> tuple:
        """Return a tuple representation of the object. Intended for writing to file. """
        return tuple(self.as_list)

    @property
    def as_dict(self, ) -> dict:
        """Return a dictionary representation of the object. Useful packaging for other objects. """
        d = {}
        for f in _fields(self.__class__):
            d[f.name] = getattr(self, f.name)
        return d


@_dataclass
class NuclideDatabaseEntry(DatabaseEntry):

    @property
    def as_tuple(self, ) -> tuple:
        """Return a tuple representation of the object. Intended for writing to file. """
        lst = [self.n.Z, self.n.A, self.n.element_symbol]
        for f in _fields(self.__class__):
            if f.name != 'n':
                lst.append(getattr(self, f.name))
        return tuple(lst)


class Database:
    """A generic representation of a RIPL database that accesses information from a single ASCII file. 
    
       More complicated databases may have multiple reader and writer methods.
    """

    reader: object = None # The method to read data from a specified ASCII file
    entry : object = None # The object which represents an entry in the database
    writer: object = None # The method to write data to a specified ASCII file

    def __init__(self, data: dict = {}) -> None:
        """Initialize the object. """
        self.data = data

    def load(self, fpath: str) -> None:
        """A generic function for Loading the database from an ASCII file into the data dictionary. 
           This method may need to be extended; it may not work in every case. 
           The success of loading depends sensitively on the structure of the input file.
        """
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
        """Return the entry from the database given the key.

        Args:
            key (object): The key to retrieve the entry.

        Returns:
            object: The entry from the database.

        Raises:
            NucleusNotFoundError: If the key is not found in a NuclideDatabase.
            ElementNotFoundError: If the key is not found in an ElementDatabase.
            KeyError: If the key is not found in a generic Database.
        """
        try:
            return self.data[key]
        except KeyError:
            if isinstance(self, NuclideDatabase):
                raise NucleusNotFoundError(f"Nuclide with key {key} not found in database.")
            elif isinstance(self, ElementDatabase):
                raise ElementNotFoundError(f"Element with key {key} not found in database.")
            else:
                raise KeyError(f"Key {key} not found in database.")

    def set(self, key: object, value: object) -> None:
        """Set the entry in the database given the key and value. """
        self.data[key] = value

    def insert(self, key: object, value: object) -> None:
        """Insert the entry in the database given the key and value. """
        self.set(key, value)

    def remove(self, key: object) -> None:
        """Remove an existing entry in the database by providing a key (typically a nucleus-like) object. """
        self.data.pop(key)

    def clear(self, ) -> None:
        """Clear the database. """
        del self.data
        self.data = {}

    def __iter__(self, ) -> iter:
        """Return the list of keys for the data property as an iterable. """
        return iter(self.data.keys())


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
            try:
                self.data.pop(entry.n)
            except KeyError:
                raise NucleusNotFoundError(f"Nuclide {entry.n} not found in database.")
        else:
            raise TypeError("Entry object must have a nucleus property!")


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
            try:
                self.data.pop(entry.Z)
            except KeyError:
                raise ElementNotFoundError(f"Element {entry.Z} not found in database.")
        elif hasattr(entry, 'sym'):
            try:
                self.data.pop(entry.Z)
            except KeyError:
                raise ElementNotFoundError(f"Element with symbol {entry.sym} not found in database.")
        elif hasattr(entry, 'symbol'):
            try:
                self.data.pop(entry.Z)
            except KeyError:
                raise ElementNotFoundError(f"Element with symbol {entry.symbol} not found in database.")
        elif hasattr(entry, 'name'):
            try:
                self.data.pop(entry.Z)
            except KeyError:
                raise ElementNotFoundError(f"Element with name {entry.name} not found in database.")
        else:
            raise TypeError("Entry object must have an element number!")


class _DbAccessor:
    """A pass through object which enables dynamic Database access. """

    def __init__(self, ) -> None:
        """Store dynamically assigned attributes in a separate set. """
        self._attributes = set()

    def __setattr__(self, name, value):
        """Set attribute so long as it isn't protected. """
        if name not in ("_attributes", ) and not name.startswith("__"):
            self._attributes.add(name)
        super().__setattr__(name, value)

    def __call__(self):
        """Iterate over assigned attributes. """
        for attr_name in self._attributes:
            yield attr_name


def load(db_obj: object, db_file_path: str) -> object:
    """Load the database into memory and return it. """
    db = db_obj()
    db.load(db_file_path)
    return db
