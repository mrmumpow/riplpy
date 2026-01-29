# -*- coding: utf-8 -*-
"""Tests for the RIPLpy gamma module.

Tests the reading and writing of gamma-ray strength function data from RIPL-4.
"""

import os
import pytest
from pathlib import Path

import riplpy.gamma as gamma
from riplpy.collections import Nuclide


class TestGDRTheoretical:
    """Tests for the theoretical Giant Dipole Resonance parameters."""

    def test_load_from_directory(self, ripl_path):
        """Test loading GDR theoretical parameters from RIPL directory."""
        db = gamma.gdr.load(directory=ripl_path)
        assert db is not None
        assert len(db.data) > 0

    def test_get_gdr_parameters(self, ripl_path):
        """Test retrieving GDR parameters for a nucleus."""
        db = gamma.gdr.load(directory=ripl_path)
        # Si-28 should be in the database
        n = Nuclide(Z=14, A=28)
        if n in db.data:
            entry = db.get(n)
            assert entry is not None
            # Should have GDR energies E1, E2 and widths W1, W2
            assert entry.E1 is not None
            assert entry.W1 is not None

    def test_gdr_values_reasonable(self, ripl_path):
        """Test that GDR parameters are in reasonable range."""
        db = gamma.gdr.load(directory=ripl_path)
        for n, entry in list(db.data.items())[:50]:
            # GDR energy typically 10-25 MeV
            if entry.E1 is not None:
                assert 5 < entry.E1 < 35, f"E1 out of range for {n}"
            if entry.E2 is not None:
                assert 5 < entry.E2 < 35, f"E2 out of range for {n}"
            # GDR width typically 2-15 MeV
            if entry.W1 is not None:
                assert 0 < entry.W1 < 20, f"W1 out of range for {n}"

    def test_write_and_read_roundtrip(self, ripl_path, temp_output_dir):
        """Test that writing and re-reading produces identical data."""
        db = gamma.gdr.load(directory=ripl_path)

        # Write to temp file
        output_path = os.path.join(temp_output_dir, "test_gdr.dat")
        db.save(output_path)

        # Read back
        db2 = gamma.gdr.load(file_path=output_path)

        # Compare entries
        for n in list(db.data.keys())[:10]:
            orig = db.get(n)
            new = db2.get(n)
            if orig.E1 is not None and new.E1 is not None:
                assert orig.E1 == pytest.approx(new.E1, rel=1e-3)
