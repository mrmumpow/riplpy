# -*- coding: utf-8 -*-
"""Tests for the RIPLpy densities module.

Tests the reading and writing of nuclear level density data from RIPL-4.
"""

import os
import pytest
from pathlib import Path

import riplpy.densities as densities
from riplpy.collections import Nuclide


class TestBSFG:
    """Tests for the Back-Shifted Fermi Gas level density database."""

    def test_load_from_directory(self, ripl_path):
        """Test loading BSFG database from RIPL directory."""
        db = densities.bsfg.load(directory=ripl_path)
        assert db is not None
        assert len(db.data) > 0

    def test_get_entry(self, ripl_path):
        """Test retrieving a specific entry from the database."""
        db = densities.bsfg.load(directory=ripl_path)
        # Fe-56 is a common nucleus
        n = Nuclide(Z=26, A=56)
        if n in db.data:
            entry = db.get(n)
            assert entry is not None
            assert entry.n == n
            # Should have level density parameters
            assert entry.ainf is not None

    def test_write_and_read_roundtrip(self, ripl_path, temp_output_dir):
        """Test that writing and re-reading produces identical data."""
        db = densities.bsfg.load(directory=ripl_path)

        # Write to temp file
        output_path = os.path.join(temp_output_dir, "test_bsfg.dat")
        db.save(output_path)

        # Read back
        db2 = densities.bsfg.load(file_path=output_path)

        # Compare entries
        for n in list(db.data.keys())[:10]:
            orig = db.get(n)
            new = db2.get(n)
            if orig.ainf is not None and new.ainf is not None:
                assert orig.ainf == pytest.approx(new.ainf, rel=1e-4)


class TestCT:
    """Tests for the Constant Temperature level density database."""

    def test_load_from_directory(self, ripl_path):
        """Test loading CT database from RIPL directory."""
        db = densities.ct.load(directory=ripl_path)
        assert db is not None
        assert len(db.data) > 0

    def test_has_temperature_parameters(self, ripl_path):
        """Test that CT entries have temperature parameters."""
        db = densities.ct.load(directory=ripl_path)
        for n, entry in list(db.data.items())[:10]:
            # CT model should have T, E0, Ematch parameters
            assert hasattr(entry, 'T')
            assert hasattr(entry, 'E0')


class TestEGSM:
    """Tests for the Enhanced Generalized Superfluid Model database."""

    def test_load_from_directory(self, ripl_path):
        """Test loading EGSM database from RIPL directory."""
        db = densities.egsm.load(directory=ripl_path)
        assert db is not None
        assert len(db.data) > 0

    def test_get_level_density_parameter(self, ripl_path):
        """Test retrieving level density parameter 'a'."""
        db = densities.egsm.load(directory=ripl_path)
        for n, entry in list(db.data.items())[:10]:
            # EGSM should have level density parameter 'a'
            assert hasattr(entry, 'a')


class TestEGSMNorm:
    """Tests for the EGSM normalization factors database."""

    def test_load_from_directory(self, ripl_path):
        """Test loading EGSM normalization database from RIPL directory."""
        db = densities.egsm_norm.load(directory=ripl_path)
        assert db is not None
        assert len(db.data) > 0

    def test_normalization_factors_reasonable(self, ripl_path):
        """Test that normalization factors are close to 1.0."""
        db = densities.egsm_norm.load(directory=ripl_path)
        for ele, entry in db.data.items():
            # Normalization factors should be close to 1.0 (within ~20%)
            assert 0.5 < entry.factor < 1.5, f"Factor out of range for element {ele}"


class TestDensityComparison:
    """Tests comparing different level density models."""

    def test_bsfg_and_ct_have_common_nuclei(self, ripl_path):
        """Test that BSFG and CT share common nuclei."""
        bsfg = densities.bsfg.load(directory=ripl_path)
        ct = densities.ct.load(directory=ripl_path)

        # Find common nuclei
        common = set(bsfg.data.keys()) & set(ct.data.keys())
        assert len(common) > 50  # Should have many common nuclei
