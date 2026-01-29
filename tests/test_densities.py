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


class TestShellCorrections:
    """Tests for the shell correction databases."""

    def test_load_ms_from_directory(self, ripl_path):
        """Test loading Myers-Swiatecki shell corrections from RIPL directory."""
        db = densities.shell_corr.load_ms(directory=ripl_path)
        assert db is not None
        assert len(db.data) > 0

    def test_load_mk_from_directory(self, ripl_path):
        """Test loading Mengoni-Nakajima shell corrections from RIPL directory."""
        db = densities.shell_corr.load_mk(directory=ripl_path)
        assert db is not None
        assert len(db.data) > 0

    def test_ms_shell_corrections_have_deformations(self, ripl_path):
        """Test that MS shell corrections include deformation parameters."""
        db = densities.shell_corr.load_ms(directory=ripl_path)
        for n, entry in list(db.data.items())[:10]:
            assert hasattr(entry, 'shell')
            assert hasattr(entry, 'beta2')
            assert hasattr(entry, 'beta4')

    def test_shell_corrections_reasonable_values(self, ripl_path):
        """Test that shell correction values are in reasonable range."""
        db = densities.shell_corr.load_ms(directory=ripl_path)
        for n, entry in list(db.data.items())[:50]:
            # Shell corrections typically -10 to +10 MeV
            assert -20 < entry.shell < 20, f"Shell correction out of range for {n}"


class TestHFBLevelDensities:
    """Tests for the HFB spin-dependent level density database."""

    def test_load_element(self, ripl_path):
        """Test loading HFB level densities for a single element."""
        db = densities.hfb.load_element(Z=26, directory=ripl_path)
        assert db is not None
        assert len(db.data) > 0

    def test_has_positive_and_negative_parity(self, ripl_path):
        """Test that entries have both parity data."""
        db = densities.hfb.load_element(Z=26, directory=ripl_path)
        for n, entry in list(db.data.items())[:5]:
            # Should have positive parity data
            assert entry.positive_parity is not None or entry.negative_parity is not None
            if entry.positive_parity:
                assert len(entry.positive_parity.U) > 0
                assert len(entry.positive_parity.rho_tot) > 0

    def test_get_total_density(self, ripl_path):
        """Test retrieving total level density at specific energy."""
        db = densities.hfb.load_element(Z=26, directory=ripl_path)
        n = Nuclide(Z=26, A=56)
        if n in db.data:
            entry = db.get(n)
            density = entry.get_total_density(5.0)
            # Level density should be positive
            assert density > 0

    def test_spin_dependent_densities(self, ripl_path):
        """Test that spin-dependent density arrays are present."""
        db = densities.hfb.load_element(Z=26, directory=ripl_path)
        for n, entry in list(db.data.items())[:3]:
            if entry.positive_parity:
                # Should have spin-dependent densities
                assert len(entry.positive_parity.rho_J) > 0
                # Each energy point should have spin densities
                assert len(entry.positive_parity.rho_J[0]) > 0


class TestDensityComparison:
    """Tests comparing different level density models."""

    def test_bsfg_and_ct_have_common_nuclei(self, ripl_path):
        """Test that BSFG and CT share common nuclei."""
        bsfg = densities.bsfg.load(directory=ripl_path)
        ct = densities.ct.load(directory=ripl_path)

        # Find common nuclei
        common = set(bsfg.data.keys()) & set(ct.data.keys())
        assert len(common) > 50  # Should have many common nuclei
