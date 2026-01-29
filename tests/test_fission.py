# -*- coding: utf-8 -*-
"""Tests for the RIPLpy fission module.

Tests the reading and writing of fission barrier data from RIPL-4.
"""

import os
import pytest
from pathlib import Path

import riplpy.fission as fission
from riplpy.collections import Nuclide


class TestEmpiricalBarriers:
    """Tests for the empirical fission barrier database."""

    def test_load_from_directory(self, ripl_path):
        """Test loading empirical barriers from RIPL directory."""
        db = fission.empirical.load(directory=ripl_path)
        assert db is not None
        assert len(db.data) > 0

    def test_get_barrier_heights(self, ripl_path):
        """Test retrieving barrier heights for actinide nucleus."""
        db = fission.empirical.load(directory=ripl_path)
        # U-238 is a well-studied fissioning nucleus
        n = Nuclide(Z=92, A=238)
        if n in db.data:
            entry = db.get(n)
            assert entry is not None
            # Should have first barrier height
            assert entry.Ea is not None or entry.Eb is not None

    def test_barrier_values_reasonable(self, ripl_path):
        """Test that barrier heights are in reasonable range."""
        db = fission.empirical.load(directory=ripl_path)
        for n, entry in db.data.items():
            # Fission barrier heights typically 0-30 MeV
            if entry.Ea is not None:
                assert 0 < entry.Ea < 40, f"Barrier Ea out of range for {n}"
            if entry.Eb is not None:
                assert 0 < entry.Eb < 40, f"Barrier Eb out of range for {n}"


class TestEmpiricalNew:
    """Tests for the new empirical fission barrier database."""

    def test_load_from_directory(self, ripl_path):
        """Test loading new empirical barriers from RIPL directory."""
        db = fission.empirical_new.load(directory=ripl_path)
        assert db is not None
        assert len(db.data) > 0

    def test_has_uncertainties(self, ripl_path):
        """Test that new format includes uncertainties."""
        db = fission.empirical_new.load(directory=ripl_path)
        for n, entry in list(db.data.items())[:10]:
            # New format should have uncertainty estimates
            assert hasattr(entry, 'dVa') or hasattr(entry, 'dVb')


class TestHFBBarriers:
    """Tests for the HFB fission barrier database."""

    def test_load_from_directory(self, ripl_path):
        """Test loading HFB barriers from RIPL directory."""
        db = fission.hfb.load(directory=ripl_path)
        assert db is not None
        assert len(db.data) > 0

    def test_has_inner_outer_barriers(self, ripl_path):
        """Test that HFB data has inner and outer barrier info."""
        db = fission.hfb.load(directory=ripl_path)
        for n, entry in list(db.data.items())[:10]:
            # HFB should have inner (Bin) and outer (Bout) barriers
            assert hasattr(entry, 'Bin')
            assert hasattr(entry, 'Bout')


class TestBSkG3Barriers:
    """Tests for the BSkG3 fission barrier database."""

    def test_load_from_directory(self, ripl_path):
        """Test loading BSkG3 barriers from RIPL directory."""
        db = fission.bskg3.load(directory=ripl_path)
        assert db is not None
        assert len(db.data) > 0

    def test_has_deformation_parameters(self, ripl_path):
        """Test that BSkG3 data has deformation info."""
        db = fission.bskg3.load(directory=ripl_path)
        for n, entry in list(db.data.items())[:10]:
            # BSkG3 should have deformation info for barriers
            assert hasattr(entry, 'inner') or hasattr(entry, 'outer1')


class TestFissionComparison:
    """Tests comparing different fission barrier models."""

    def test_empirical_and_hfb_have_common_nuclei(self, ripl_path):
        """Test that empirical and HFB share common nuclei."""
        emp = fission.empirical.load(directory=ripl_path)
        hfb = fission.hfb.load(directory=ripl_path)

        # Find common nuclei
        common = set(emp.data.keys()) & set(hfb.data.keys())
        # Fission data is limited to heavy nuclei, so may have fewer common entries
        assert len(common) >= 10
