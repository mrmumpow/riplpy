# -*- coding: utf-8 -*-
"""Optical Model Potential (OMP) section of RIPL.

This module provides access to the RIPL optical model parameter library,
containing ~584 optical model potentials for various projectiles and targets.

Submodules:
    config: Configuration and file paths
    core: Base dataclasses for OMP components
    index: Index file parser
    spherical: Spherical potential parser
    coupled_channel: Coupled-channel potential parser
    omp: Main OMP database
    deformations: Excited-level deformation parameters
    references: Bibliographic references

Example:
    >>> import riplpy.optical as optical
    >>> optical.load(directory='/path/to/RIPL')
    >>> # Get a specific potential by reference number
    >>> pot = optical.db.potentials.get(2405)
    >>> print(pot.projectile)
    'n'
    >>> # Get deformation for Pu-239
    >>> deform = optical.db.deformations.get(94, 239)

    >>> # Load modified potentials
    >>> mod_db = optical.load_modified_potentials()
    >>> print(mod_db.irefs)  # [1480, 1481, 1482, 2412, 2415, 4609, 4610]
"""

# RIPLpy
from riplpy.db import _DbAccessor

# Local imports
from . import config
from . import core
from . import index
from . import omp
from . import spherical
from . import coupled_channel
from . import deformations
from . import references

# Database accessor
db = _DbAccessor()


def load(directory: str = None) -> None:
    """Load the optical model database from the RIPL directory.

    Args:
        directory: Path to the RIPL database directory. If not provided,
                   uses the configured path from riplpy.config.

    Note:
        Once loaded, databases are accessible via optical.db:
            - optical.db.index: Index of all potentials (metadata)
            - optical.db.potentials: Full potential data (spherical + CC)
            - optical.db.deformations: Excited-level deformation parameters
            - optical.db.references: Bibliographic references
    """
    from riplpy import config as riplpy_config

    if directory is None:
        directory = riplpy_config.get_path()

    # Load the index
    db.index = index.load(directory=directory)

    # Load the main OMP library
    db.potentials = omp.load(directory=directory)

    # Load deformations
    db.deformations = deformations.load(directory=directory)

    # Load references
    db.references = references.load(directory=directory)


def load_modified_potentials(directory: str = None):
    """Load modified optical model potentials from the mod-potentials directory.

    The mod-potentials directory contains individual OMP files (omp-XXXXXX.dat)
    that are updated or corrected versions of potentials in the main database.

    Args:
        directory: RIPL directory path. If None, uses configured path.

    Returns:
        OMPDatabase with modified potentials

    Example:
        >>> mod_db = optical.load_modified_potentials()
        >>> print(mod_db.irefs)
        [1480, 1481, 1482, 2412, 2415, 4609, 4610]
    """
    return omp.load_modified_potentials(directory=directory)


def load_with_modifications(directory: str = None, apply_modifications: bool = True):
    """Load the OMP database with optional modifications applied.

    This is a convenience function that loads the main database and optionally
    replaces entries with their modified versions from the mod-potentials directory.

    Args:
        directory: RIPL directory path. If None, uses configured path.
        apply_modifications: If True, replace potentials with modified versions
                            where available. Default True.

    Returns:
        OMPDatabase with potentials (modified versions applied if requested)

    Example:
        >>> db = optical.load_with_modifications()
        >>> # Potential 1480 will use the modified version if available
        >>> pot = db.get(1480)
    """
    return omp.load_with_modifications(directory=directory, apply_modifications=apply_modifications)
