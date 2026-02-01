# -*- coding: utf-8 -*-
"""Optical Model Potential (OMP) section of RIPL.

This module provides access to the RIPL optical model parameter library,
containing ~584 optical model potentials for various projectiles and targets.

Submodules:
    config: Configuration and file paths
    core: Base dataclasses for OMP components
    index: Index file parser
    spherical: Spherical potential parser
    omp: Main OMP database

Example:
    >>> import riplpy.optical as optical
    >>> optical.load(directory='/path/to/RIPL')
    >>> # Get a specific potential by reference number
    >>> pot = optical.db.potentials.get(2405)
    >>> print(pot.projectile)
    'n'
"""

# RIPLpy
from riplpy.db import _DbAccessor

# Local imports
from . import config
from . import core
from . import index
from . import omp
from . import spherical

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
            - optical.db.potentials: Full potential data (currently spherical only)
    """
    from riplpy import config as riplpy_config

    if directory is None:
        directory = riplpy_config.get_path()

    # Load the index
    db.index = index.load(directory=directory)

    # Load the main OMP library
    db.potentials = omp.load(directory=directory)
