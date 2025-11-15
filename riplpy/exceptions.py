# -*- coding: utf-8 -*-
"""Custom exceptions for the RIPLpy library."""


class RIPLPyError(Exception):
    """Base class for exceptions in RIPLpy."""
    pass


class FileFormatError(RIPLPyError):
    """Raised when a file is not in the expected format."""
    pass


class RiplFileNotFoundError(RIPLPyError, FileNotFoundError):
    """Raised when a RIPL file is not found on the filesystem."""
    pass


class NucleusNotFoundError(RIPLPyError, KeyError):
    """Raised when a nucleus is not found in a database."""
    pass


class ElementNotFoundError(RIPLPyError, KeyError):
    """Raised when an element is not found in a database."""
    pass
