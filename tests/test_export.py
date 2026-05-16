# -*- coding: utf-8 -*-
"""Tests for uniform ML/AI export across scalar and array/spectral databases.

These guard the cross-section ingestion guarantee: every database — whether it
stores scalar dataclass entries or array/spectral packets — must export
uniformly via to_dataframe()/to_json()/to_records(), and the top-level
riplpy.to_dataframe(spec)/to_records(spec) dispatch must work.
"""

import json
import os

import pytest

import riplpy
import riplpy.masses as masses
import riplpy.gamma as gamma
import riplpy.fission as fission
from riplpy.collections import Nuclide
from riplpy.db import PacketEntry


class TestScalarExport:
    """Scalar dataclass-entry databases (the original ML-ready path)."""

    def test_ame20_to_dataframe(self, ripl_path):
        db = masses.ame20.load(directory=ripl_path)
        df = db.to_dataframe()
        assert df.shape[0] == len(db.data)
        assert 'n.Z' in df.columns and 'n.A' in df.columns

    def test_ame20_to_json_none_safe(self, ripl_path, temp_output_dir):
        # frdm12 has None deformation fields - must serialize without crashing
        db = masses.frdm12.load(directory=ripl_path)
        out = os.path.join(temp_output_dir, "frdm12.json")
        db.to_json(out)
        records = json.load(open(out))
        assert isinstance(records, list) and len(records) > 0
        # at least one record should carry an explicit null
        assert any(any(v is None for v in r.values()) for r in records[:50])


class TestSpectralExport:
    """Array/spectral databases must now export uniformly (CR-1/CR-2/CR-4)."""

    def test_d1m_packetentry_uniform(self, ripl_path):
        db = gamma.d1m.load_element(Z=26, directory=ripl_path)
        n, entry = next(iter(db.data.items()))
        # Uniform entry interface
        assert isinstance(entry, PacketEntry)
        assert hasattr(entry, 'as_dict') and hasattr(entry, 'field_info')
        # Backwards-compatible dict-style AND attribute access
        assert entry['U'] is not None
        assert entry.U is entry['U']
        # _field_info is populated (ML/LLM schema)
        assert len(entry.field_info()) > 0

    def test_d1m_to_dataframe_and_records(self, ripl_path):
        db = gamma.d1m.load_element(Z=26, directory=ripl_path)
        df = db.to_dataframe()
        assert df.shape[0] == len(db.data)
        recs = db.to_list()
        assert len(recs) == len(db.data)
        # Array fields stay native lists (not JSON strings) for ML use
        assert isinstance(recs[0]['U'], list)

    def test_psf_list_valued_explodes(self, ripl_path):
        # PSF stores a list of measurements per nucleus; export must emit one
        # record per dataset, not one giant cell.
        db = gamma.psf.load_category('oslo', directory=ripl_path)
        n_datasets = sum(len(v) if isinstance(v, list) else 1
                         for v in db.data.values())
        df = db.to_dataframe()
        assert df.shape[0] == n_datasets
        recs = db.to_list()
        assert len(recs) == n_datasets


class TestUniformDispatch:
    """Top-level riplpy.to_dataframe(spec)/to_records(spec) (IM-3)."""

    def test_to_dataframe_spec(self, ripl_path):
        riplpy.set_path(ripl_path)
        masses.load(directory=ripl_path)
        df = riplpy.to_dataframe('masses.ame20')
        assert df.shape[0] > 0

    def test_to_records_spec(self, ripl_path):
        riplpy.set_path(ripl_path)
        fission.load(directory=ripl_path)
        recs = riplpy.to_records('fission.bskg3_barriers')
        assert isinstance(recs, list) and len(recs) > 0

    def test_to_dataframe_unloaded_raises(self, ripl_path):
        # A heavy DB that riplpy.load() leaves as None -> clear ValueError,
        # not a crash. (An empty-but-loaded legacy DB instead exports an
        # empty frame, which is the correct non-surprising behavior.)
        riplpy.set_path(ripl_path)
        gamma.load(directory=ripl_path)  # include_heavy=False -> smlo_e1 is None
        with pytest.raises(ValueError):
            riplpy.to_dataframe('gamma.smlo_e1')

    def test_empty_legacy_db_exports_empty_frame(self, ripl_path):
        # RIPL-3 legacy mass models load as an empty Database (not None);
        # exporting yields an empty DataFrame rather than raising.
        riplpy.set_path(ripl_path)
        masses.load(directory=ripl_path)
        df = riplpy.to_dataframe('masses.frdm1995')
        assert df.shape[0] == 0

    def test_public_api_surface(self):
        assert 'to_dataframe' in riplpy.__all__
        assert 'to_records' in riplpy.__all__
        assert 'Nuclide' in riplpy.__all__


class TestPacketEntry:
    """The generic uniform entry wrapper."""

    def test_dual_access_and_interface(self):
        e = PacketEntry({'U': [1.0, 2.0], 'fE1': [3.0, 4.0], 'n': Nuclide(Z=26, A=56)})
        assert e['U'] == [1.0, 2.0]
        assert e.U == [1.0, 2.0]
        assert 'U' in e
        assert set(e.fields()) == {'U', 'fE1', 'n'}
        d = e.as_dict
        assert d['fE1'] == [3.0, 4.0]
        assert 'U' in e.field_info()
