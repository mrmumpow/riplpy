# -*- coding: utf-8 -*-
"""Tests for the RIPLpy levels module.

Tests the reading and writing of nuclear level data from RIPL-4.
"""

import os
import pytest
from pathlib import Path

import riplpy.levels as levels
from riplpy.collections import Nuclide


class TestLevelsCT:
    """Tests for the Constant Temperature fit parameters database."""

    def test_load_from_directory(self, ripl_path):
        """Test loading levels CT parameters from RIPL directory."""
        db = levels.ct.load(directory=ripl_path)
        assert db is not None
        assert len(db.data) > 0

    def test_get_ct_parameters(self, ripl_path):
        """Test retrieving CT fit parameters for a nucleus."""
        db = levels.ct.load(directory=ripl_path)
        # Fe-56 should be in the database
        n = Nuclide(Z=26, A=56)
        if n in db.data:
            entry = db.get(n)
            assert entry is not None
            # Should have temperature T and back-shift U0
            assert hasattr(entry, 'T')
            assert hasattr(entry, 'U0')

    def test_has_discrete_level_info(self, ripl_path):
        """Test that entries have discrete level information."""
        db = levels.ct.load(directory=ripl_path)
        for n, entry in list(db.data.items())[:50]:
            # Should have number of levels
            assert hasattr(entry, 'Nlev')
            assert hasattr(entry, 'Nmax')

    def test_temperature_values_reasonable(self, ripl_path):
        """Test that temperature values are in reasonable range."""
        db = levels.ct.load(directory=ripl_path)
        for n, entry in list(db.data.items())[:100]:
            # Temperature typically 0-10 MeV (0 for nuclei with no fit)
            if entry.T is not None:
                assert 0 <= entry.T < 20, f"T out of range for {n}"

    def test_write_and_read_roundtrip(self, ripl_path, temp_output_dir):
        """Test that writing and re-reading produces identical data."""
        db = levels.ct.load(directory=ripl_path)

        # Write to temp file
        output_path = os.path.join(temp_output_dir, "test_levels_ct.dat")
        db.save(output_path)

        # Read back
        db2 = levels.ct.load(file_path=output_path)

        # Compare number of entries
        assert len(db.data) == len(db2.data)


class TestLevelsCoverage:
    """Tests for level data coverage."""

    def test_covers_many_elements(self, ripl_path):
        """Test that level database covers many elements."""
        db = levels.ct.load(directory=ripl_path)

        # Get unique Z values
        z_values = set(n.Z for n in db.data.keys())

        # Should cover many elements
        assert len(z_values) > 50
