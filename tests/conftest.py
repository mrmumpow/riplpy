# -*- coding: utf-8 -*-
"""Pytest configuration and fixtures for RIPLpy tests.

This module provides common fixtures and configuration for testing
RIPLpy against the RIPL-4 nuclear data library.
"""

import os
import pytest

# RIPL-4 data directory
RIPL_PATH = "/path/to/RIPL-4"


@pytest.fixture(scope="session")
def ripl_path():
    """Return the path to the RIPL-4 data directory."""
    if not os.path.exists(RIPL_PATH):
        pytest.skip(f"RIPL-4 data directory not found: {RIPL_PATH}")
    return RIPL_PATH


@pytest.fixture(scope="session")
def temp_output_dir(tmp_path_factory):
    """Create a temporary directory for test output files."""
    return tmp_path_factory.mktemp("riplpy_test_output")


@pytest.fixture(scope="session", autouse=True)
def set_ripl_env():
    """Set the RIPL_LOCATION environment variable for tests."""
    old_value = os.environ.get("RIPL_LOCATION")
    os.environ["RIPL_LOCATION"] = RIPL_PATH
    yield
    if old_value is not None:
        os.environ["RIPL_LOCATION"] = old_value
    else:
        os.environ.pop("RIPL_LOCATION", None)
