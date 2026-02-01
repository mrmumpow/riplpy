# -*- coding: utf-8 -*-
"""Main optical model potential database.

This module provides the primary interface for loading and accessing
optical model potentials from the RIPL library.
"""

import os as _os
from typing import Dict, List, Optional, Iterator

from riplpy.db import Database
from . import config
from .spherical import SphericalOMP, parse_spherical_omp
from .reader import OMPFileReader


class OMPDatabase(Database):
    """Database of optical model potentials.

    This class provides access to the full library of optical model potentials,
    supporting lookup by reference number and filtering by various criteria.

    Currently supports:
        - Spherical potentials (imodel=0): 461 potentials

    Planned support:
        - Rigid rotor (imodel=1): 99 potentials
        - Vibrational (imodel=2): 10 potentials
        - Soft rotor (imodel=3): 6 potentials
        - Combined (imodel=4,5): 5 potentials

    Example:
        >>> db = OMPDatabase()
        >>> db.load('/path/to/om-parameter-u.dat')
        >>> pot = db.get(2405)
        >>> print(pot.projectile)
        'n'
    """

    entry = SphericalOMP  # Default entry type

    def __init__(self, data: Dict[int, SphericalOMP] = None):
        """Initialize the OMP database.

        Args:
            data: Optional dictionary mapping iref -> potential
        """
        super().__init__(data)
        self._skipped_cc = 0  # Count of skipped coupled-channel potentials

    def __repr__(self) -> str:
        """Return string representation of the database."""
        n_spherical = sum(1 for v in self.data.values() if isinstance(v, SphericalOMP))
        return f"<OMPDatabase: {len(self.data)} potentials ({n_spherical} spherical)>"

    def load(self, fpath: str) -> None:
        """Load optical model potentials from the parameter file.

        Args:
            fpath: Path to om-parameter-u.dat file

        Note:
            Currently only loads spherical potentials (imodel=0).
            Coupled-channel potentials are skipped but counted.
        """
        self.data = {}
        self._skipped_cc = 0

        with OMPFileReader(fpath) as reader:
            for entry_lines in reader.entries():
                if not entry_lines:
                    continue

                try:
                    # Try to parse as spherical potential
                    omp = parse_spherical_omp(entry_lines)
                    self.data[omp.iref] = omp
                except ValueError:
                    # Not a spherical potential (coupled-channel)
                    self._skipped_cc += 1
                except Exception:
                    # Skip malformed entries
                    pass

    def get(self, iref: int) -> SphericalOMP:
        """Get a potential by its reference number.

        Args:
            iref: Library reference number

        Returns:
            SphericalOMP for the specified potential

        Raises:
            KeyError: If iref not found in database
        """
        if iref not in self.data:
            raise KeyError(f"OMP reference {iref} not found in database")
        return self.data[iref]

    def get_by_iref(self, iref: int) -> Optional[SphericalOMP]:
        """Get a potential by reference number, returning None if not found.

        Args:
            iref: Library reference number

        Returns:
            SphericalOMP if found, None otherwise
        """
        return self.data.get(iref)

    @property
    def irefs(self) -> List[int]:
        """Get list of all reference numbers in the database."""
        return sorted(self.data.keys())

    @property
    def n_spherical(self) -> int:
        """Get count of spherical potentials."""
        return sum(1 for v in self.data.values() if isinstance(v, SphericalOMP))

    @property
    def n_skipped(self) -> int:
        """Get count of skipped coupled-channel potentials."""
        return self._skipped_cc

    def filter_by_projectile(self, projectile: str) -> "OMPDatabase":
        """Filter potentials by projectile type.

        Args:
            projectile: Projectile name ('n', 'p', 'd', 't', 'He3', 'a')

        Returns:
            New OMPDatabase with filtered potentials
        """
        # Map projectile names to (Z, A) pairs
        proj_map = {
            'n': (0, 1),
            'p': (1, 1),
            'd': (1, 2),
            't': (1, 3),
            'He3': (2, 3),
            '3He': (2, 3),
            'a': (2, 4),
            'alpha': (2, 4),
        }

        if projectile not in proj_map:
            raise ValueError(f"Unknown projectile: {projectile}. "
                           f"Valid options: {list(proj_map.keys())}")

        iz, ia = proj_map[projectile]
        filtered = {
            k: v for k, v in self.data.items()
            if v.flags.iz_proj == iz and v.flags.ia_proj == ia
        }
        result = OMPDatabase(filtered)
        return result

    def filter_by_target(self, Z: int = None, A: int = None) -> "OMPDatabase":
        """Filter potentials by target nucleus.

        Args:
            Z: Target atomic number (filters Z_min <= Z <= Z_max)
            A: Target mass number (filters A_min <= A <= A_max)

        Returns:
            New OMPDatabase with filtered potentials
        """
        filtered = {}
        for k, v in self.data.items():
            if Z is not None:
                if not (v.validity.Z_min <= Z <= v.validity.Z_max):
                    continue
            if A is not None:
                if not (v.validity.A_min <= A <= v.validity.A_max):
                    continue
            filtered[k] = v
        return OMPDatabase(filtered)

    def filter_by_energy(self, E: float) -> "OMPDatabase":
        """Filter potentials by projectile energy.

        Args:
            E: Projectile energy [MeV]

        Returns:
            New OMPDatabase with filtered potentials
        """
        filtered = {
            k: v for k, v in self.data.items()
            if v.validity.E_min <= E <= v.validity.E_max
        }
        return OMPDatabase(filtered)

    def filter_relativistic(self) -> "OMPDatabase":
        """Filter to relativistic potentials only.

        Returns:
            New OMPDatabase with only relativistic potentials
        """
        filtered = {
            k: v for k, v in self.data.items()
            if v.flags.is_relativistic
        }
        return OMPDatabase(filtered)

    def filter_dispersive(self) -> "OMPDatabase":
        """Filter to dispersive potentials only.

        Returns:
            New OMPDatabase with only dispersive potentials
        """
        filtered = {
            k: v for k, v in self.data.items()
            if v.flags.uses_dispersion
        }
        return OMPDatabase(filtered)

    def find_for_reaction(self, projectile: str, Z: int, A: int, E: float) -> List[SphericalOMP]:
        """Find all potentials valid for a specific reaction.

        Args:
            projectile: Projectile type ('n', 'p', etc.)
            Z: Target atomic number
            A: Target mass number
            E: Projectile energy [MeV]

        Returns:
            List of SphericalOMP objects valid for this reaction
        """
        results = self.filter_by_projectile(projectile)
        results = results.filter_by_target(Z=Z, A=A)
        results = results.filter_by_energy(E)
        return list(results.data.values())

    def info(self) -> str:
        """Return detailed information about this database."""
        lines = ["OMP Database"]
        lines.append("-" * 40)
        lines.append(f"Total potentials: {len(self.data)}")
        lines.append(f"Spherical: {self.n_spherical}")
        lines.append(f"Skipped (coupled-channel): {self._skipped_cc}")

        # Count by projectile
        proj_counts = {}
        for v in self.data.values():
            proj = v.projectile
            proj_counts[proj] = proj_counts.get(proj, 0) + 1
        lines.append("\nBy projectile:")
        for proj, count in sorted(proj_counts.items()):
            lines.append(f"  {proj}: {count}")

        # Energy range
        if self.data:
            e_min = min(v.validity.E_min for v in self.data.values())
            e_max = max(v.validity.E_max for v in self.data.values())
            lines.append(f"\nEnergy range: {e_min:.1f} - {e_max:.1f} MeV")

        return "\n".join(lines)

    def __iter__(self) -> Iterator[int]:
        """Iterate over reference numbers."""
        return iter(self.data.keys())


def load(directory: str = None, file_path: str = None) -> OMPDatabase:
    """Load the optical model potential database.

    Args:
        directory: RIPL directory path. If provided, constructs full path.
        file_path: Direct path to parameter file. Takes precedence over directory.

    Returns:
        OMPDatabase with loaded potentials

    Raises:
        FileNotFoundError: If the parameter file cannot be found
    """
    if file_path:
        path = file_path
    elif directory:
        path = _os.path.join(directory, config.get_data_file_path('parameters'))
    else:
        # Try default RIPL path
        from riplpy import config as riplpy_config
        ripl_path = riplpy_config.get_path()
        if ripl_path:
            path = _os.path.join(ripl_path, config.get_data_file_path('parameters'))
        else:
            raise FileNotFoundError(
                "Cannot locate OMP parameter file. Please provide directory or file_path."
            )

    if not _os.path.exists(path):
        raise FileNotFoundError(f"OMP parameter file not found: {path}")

    db = OMPDatabase()
    db.load(path)
    return db
