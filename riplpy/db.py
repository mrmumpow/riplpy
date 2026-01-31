# -*- coding: utf-8 -*-
"""The base objects which define access to RIPL databases.

Python 3.10+ is expected to run this code properly.

Authors:
    * Matthew Mumpower {mumpower@lanl.gov}

"""

# OS
import os as _os

# CSV
import csv as _csv

# JSON
import json as _json

# Dataclasses
from dataclasses import dataclass as _dataclass, fields as _fields, is_dataclass as _is_dataclass

# RIPLpy
from riplpy.exceptions import NucleusNotFoundError, ElementNotFoundError, FileFormatError, RiplFileNotFoundError

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

    def __init__(self, data: dict | None = None) -> None:
        """Initialize the object. """
        self.data = data if data is not None else {}

    def __repr__(self) -> str:
        """Return a string representation of the database."""
        class_name = type(self).__name__
        module_name = type(self).__module__

        # Try to get a short module path (e.g., 'masses.ame20' from 'riplpy.masses.ame20')
        if module_name.startswith('riplpy.'):
            module_name = module_name[7:]  # Remove 'riplpy.' prefix

        count = len(self.data)

        if count == 0:
            return f"<{class_name}: {module_name} (empty)>"

        # Try to get Z range for nuclide databases
        z_info = ""
        if self.data:
            keys = list(self.data.keys())
            if hasattr(keys[0], 'Z'):
                z_values = [k.Z for k in keys if hasattr(k, 'Z')]
                if z_values:
                    z_min, z_max = min(z_values), max(z_values)
                    z_info = f", Z={z_min}-{z_max}"

        return f"<{class_name}: {module_name} ({count} entries{z_info})>"

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

    def _serialize_value(self, value: object) -> object:
        """Serialize a value for export to JSON/CSV.

        Handles Nuclide/Nucleus objects, nested dicts, lists, and dataclasses.
        """
        if value is None:
            return None
        elif isinstance(value, (int, float, str, bool)):
            return value
        elif hasattr(value, 'Z') and hasattr(value, 'A'):
            # Nucleus-like object
            return {'Z': value.Z, 'A': value.A, 'symbol': value.element_symbol}
        elif _is_dataclass(value) and not isinstance(value, type):
            # Dataclass instance
            return {f.name: self._serialize_value(getattr(value, f.name)) for f in _fields(value)}
        elif isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple)):
            return [self._serialize_value(v) for v in value]
        else:
            return str(value)

    def _flatten_entry(self, entry: object, prefix: str = '') -> dict:
        """Flatten an entry into a single-level dictionary for CSV export.

        Nested structures are flattened with dot notation (e.g., 'inner.E[MeV]').
        """
        flat = {}
        entry_dict = entry.as_dict if hasattr(entry, 'as_dict') else vars(entry)

        for key, value in entry_dict.items():
            full_key = f"{prefix}{key}" if prefix else key

            if value is None:
                flat[full_key] = None
            elif isinstance(value, (int, float, str, bool)):
                flat[full_key] = value
            elif hasattr(value, 'Z') and hasattr(value, 'A'):
                # Nucleus-like object - expand to Z, A, symbol
                flat[f"{full_key}.Z"] = value.Z
                flat[f"{full_key}.A"] = value.A
                flat[f"{full_key}.symbol"] = value.element_symbol
            elif isinstance(value, dict):
                for k, v in value.items():
                    flat[f"{full_key}.{k}"] = v
            elif isinstance(value, (list, tuple)):
                # For lists, store as JSON string
                flat[full_key] = _json.dumps(value)
            elif _is_dataclass(value) and not isinstance(value, type):
                # Recursively flatten dataclass
                nested = self._flatten_entry(value, prefix=f"{full_key}.")
                flat.update(nested)
            else:
                flat[full_key] = str(value)

        return flat

    def to_csv(self, fpath: str) -> None:
        """Export the database to a CSV file.

        Args:
            fpath: Path to the output CSV file.
        """
        if not self.data:
            return

        # Collect all rows and determine all column names
        rows = []
        all_columns = set()

        for key, entry in self.data.items():
            row = self._flatten_entry(entry)
            rows.append(row)
            all_columns.update(row.keys())

        # Sort columns for consistent output
        # Put Z, A, symbol first if present, then sort alphabetically
        priority_cols = ['n.Z', 'n.A', 'n.symbol', 'Z', 'A', 'symbol']
        sorted_cols = []
        for col in priority_cols:
            if col in all_columns:
                sorted_cols.append(col)
                all_columns.discard(col)
        sorted_cols.extend(sorted(all_columns))

        # Write CSV
        with open(fpath, 'w', newline='') as fp:
            writer = _csv.DictWriter(fp, fieldnames=sorted_cols, extrasaction='ignore')
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

    def to_json(self, fpath: str, indent: int = 2) -> None:
        """Export the database to a JSON file.

        Args:
            fpath: Path to the output JSON file.
            indent: Number of spaces for indentation (default: 2).
        """
        if not self.data:
            with open(fpath, 'w') as fp:
                _json.dump([], fp)
            return

        # Serialize all entries
        entries = []
        for key, entry in self.data.items():
            serialized = self._serialize_value(entry.as_dict if hasattr(entry, 'as_dict') else vars(entry))
            entries.append(serialized)

        with open(fpath, 'w') as fp:
            _json.dump(entries, fp, indent=indent)

    def to_dataframe(self) -> "pandas.DataFrame":
        """Export the database to a pandas DataFrame.

        Returns:
            pandas.DataFrame: A DataFrame with flattened entry data.

        Raises:
            ImportError: If pandas is not installed.
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("pandas is required for to_dataframe(). Install with: pip install pandas")

        if not self.data:
            return pd.DataFrame()

        # Collect all rows
        rows = []
        for key, entry in self.data.items():
            row = self._flatten_entry(entry)
            rows.append(row)

        # Create DataFrame
        df = pd.DataFrame(rows)

        # Reorder columns: Z, A, symbol first
        priority_cols = ['n.Z', 'n.A', 'n.symbol', 'Z', 'A', 'symbol']
        existing_priority = [col for col in priority_cols if col in df.columns]
        other_cols = sorted([col for col in df.columns if col not in priority_cols])
        df = df[existing_priority + other_cols]

        return df

    def to_list(self) -> list:
        """Export the database as a list of serialized entry dictionaries.

        Returns:
            list: A list of dictionaries, one per entry.
        """
        entries = []
        for key, entry in self.data.items():
            serialized = self._serialize_value(entry.as_dict if hasattr(entry, 'as_dict') else vars(entry))
            entries.append(serialized)
        return entries

    def to_flat_list(self) -> list:
        """Export the database as a list of flattened entry dictionaries.

        Nested structures are flattened with dot notation (e.g., 'inner.E[MeV]').

        Returns:
            list: A list of flattened dictionaries, one per entry.
        """
        rows = []
        for key, entry in self.data.items():
            row = self._flatten_entry(entry)
            rows.append(row)
        return rows

    def filter(self, predicate=None, **kwargs) -> "Database":
        """Filter database entries and return a new database with matching entries.

        Can filter using a predicate function or keyword arguments for common filters.

        Args:
            predicate: A callable that takes an entry and returns True/False.
                       If provided, kwargs are ignored.
            **kwargs: Keyword filters. Supported filters depend on entry type:
                - Z: Filter by atomic number (for nuclide databases)
                - A: Filter by mass number (for nuclide databases)
                - N: Filter by neutron number (for nuclide databases)
                - Any entry attribute: Filter by exact value match

        Returns:
            A new Database instance containing only matching entries

        Examples:
            >>> # Filter by Z (all lead isotopes)
            >>> pb_db = db.filter(Z=82)

            >>> # Filter by predicate (neutron-rich nuclei)
            >>> neutron_rich = db.filter(lambda e: e.n.N > e.n.Z)

            >>> # Filter by multiple criteria
            >>> heavy_pb = db.filter(Z=82, A=lambda a: a > 200)

            >>> # Chain filters
            >>> result = db.filter(Z=82).filter(lambda e: e.Mth < -10)
        """
        # Create a new database of the same type
        result = type(self)()

        for key, entry in self.data.items():
            # If predicate is provided, use it directly
            if predicate is not None:
                if callable(predicate) and predicate(entry):
                    result.data[key] = entry
                continue

            # Otherwise, apply keyword filters
            if self._matches_filters(key, entry, **kwargs):
                result.data[key] = entry

        return result

    def _matches_filters(self, key, entry, **kwargs) -> bool:
        """Check if an entry matches the given keyword filters."""
        for filter_key, filter_value in kwargs.items():
            # Handle nucleus-related filters (Z, A, N)
            if filter_key in ('Z', 'A', 'N'):
                # Get the nucleus from either the key or entry
                nucleus = None
                if hasattr(key, filter_key):
                    nucleus = key
                elif hasattr(entry, 'n') and hasattr(entry.n, filter_key):
                    nucleus = entry.n

                if nucleus is None:
                    return False

                actual_value = getattr(nucleus, filter_key)

                # Support callable filter values
                if callable(filter_value):
                    if not filter_value(actual_value):
                        return False
                elif actual_value != filter_value:
                    return False

            # Handle entry attribute filters
            elif hasattr(entry, filter_key):
                actual_value = getattr(entry, filter_key)

                # Support callable filter values
                if callable(filter_value):
                    if not filter_value(actual_value):
                        return False
                elif actual_value != filter_value:
                    return False

            else:
                # Filter key not found on entry
                return False

        return True

    def filter_by_range(self, attr: str, min_val=None, max_val=None) -> "Database":
        """Filter entries where an attribute falls within a range.

        Args:
            attr: Attribute name to filter on (can use 'Z', 'A', 'N' for nucleus attrs)
            min_val: Minimum value (inclusive). If None, no lower bound.
            max_val: Maximum value (inclusive). If None, no upper bound.

        Returns:
            A new Database instance containing only matching entries

        Examples:
            >>> # Nuclei with Z between 80 and 90
            >>> db.filter_by_range('Z', 80, 90)

            >>> # Entries with mass excess less than 0
            >>> db.filter_by_range('Mth', max_val=0)
        """
        def in_range(entry):
            # Try to get value from nucleus first, then from entry
            value = None
            if attr in ('Z', 'A', 'N') and hasattr(entry, 'n'):
                value = getattr(entry.n, attr, None)
            if value is None:
                value = getattr(entry, attr, None)

            if value is None:
                return False

            if min_val is not None and value < min_val:
                return False
            if max_val is not None and value > max_val:
                return False
            return True

        return self.filter(in_range)

    def find(self, predicate) -> object | None:
        """Find the first entry matching the predicate.

        Args:
            predicate: A callable that takes an entry and returns True/False

        Returns:
            The first matching entry, or None if no match found

        Examples:
            >>> # Find the first nucleus with A > 250
            >>> entry = db.find(lambda e: e.n.A > 250)
        """
        for entry in self.data.values():
            if predicate(entry):
                return entry
        return None

    def count(self, predicate=None, **kwargs) -> int:
        """Count entries matching the filter criteria.

        Args:
            predicate: A callable that takes an entry and returns True/False
            **kwargs: Keyword filters (same as filter())

        Returns:
            Number of matching entries

        Examples:
            >>> # Count lead isotopes
            >>> db.count(Z=82)
            41
        """
        return len(self.filter(predicate, **kwargs).data)

    def __len__(self) -> int:
        """Return the number of entries in the database."""
        return len(self.data)

    def __contains__(self, key) -> bool:
        """Check if a key exists in the database."""
        return key in self.data

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


def load(db_obj: Database, db_file_path: str) -> "Database":
    """Load the database into memory from a file path and return it. """
    db = db_obj()
    db.load(db_file_path)
    return db


def loader(directory: str = None, file_path: str = None, config: object = None, db_obj: object = None, file_path_key: str = None) -> "Database":
    """Load the database into memory from file path, directory, or configuration and return it.

    This is a more complex loader method. 
    The loading mechanism prioritizes the `file_path` argument first. If `file_path`
    is not provided, it attempts to construct the path using the `directory` argument.
    If neither is provided, it falls back to the default path from the configuration.

    Arguments:
        directory (str, optional): Path to the directory containing the data file.
        file_path (str, optional): Direct path to the data file.
        config (object, optional): Configuration object containing the data file path.
        database (object, optional): Database object to load the data into.
        file_path_key (str, optional): Key for the data file path in the configuration.
    Returns:
        Database: An instance of the Database class with the loaded data.

    Raises:
        FileFormatError: If the database file cannot be loaded.
        RiplFileNotFoundError: If the database file cannot be found.
    """
    db_path = None
    if file_path:
        db_path = file_path
    elif directory:
        file_path = config.get_data_file_path(file_path_key)
        db_path = _os.path.join(directory, file_path)
    else:
        try:
            file_path = config.get_data_file_path(file_path_key)
            db_path = _os.path.join(config.RIPL_PATH, file_path)
        except (ImportError, KeyError):
            # Fallback if config is not available or the key is missing
            pass

    if db_path and _os.path.exists(db_path):
        try:
            return load(db_obj, db_path)
        except Exception as e:
            raise FileFormatError(f"Failed to load {file_path_key} data from {db_path}: {e}")

    raise RiplFileNotFoundError(f"Unable to find or load {file_path_key} data file. Please provide a valid path or set RIPL_LOCATION.")
