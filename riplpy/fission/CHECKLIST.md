# Fission section — release checklist

Status of readers, writers, and tests against the RIPL-4 GitHub release
layout (``RIPL-4/github/fission/``).

## Data files in the RIPL-4 GitHub release

| File / directory | Reader module | Status |
|------------------|---------------|--------|
| ``empirical-barriers-ripl4.dat``           | ``riplpy.fission.empirical``     | Wired |
| ``empirical-barriers-ripl4.dat`` (alias)   | ``riplpy.fission.empirical_new`` | Wired (alias of ``empirical``) |
| ``empirical-barriers-new-EMPIRE.dat``      | ``riplpy.fission.empire``        | Wired |
| ``barriers-bskg3.dat``                     | ``riplpy.fission.bskg3``         | Wired (5-section RIPL-4 layout) |
| ``barriers-d1m_lep.dat``                   | ``riplpy.fission.d1m``           | Wired (new in RIPL-4) |
| ``hfbpath-bskg3/zXXX.dat``                 | -                                | Deferred |
| ``hfbpath-d1m/zXXXnYYY.dat``               | -                                | Deferred |
| ``nld-fis-bskg3/{Max1,Max2,Max3,Min1,Min2}/zXXX.dat`` | -                     | Deferred |
| ``RMF/``                                   | -                                | Deferred |

## Legacy files removed from the RIPL-4 release

| File | Reader module | Behaviour |
|------|----------------|-----------|
| ``empirical-barriers.dat``        | ``riplpy.fission.empirical``       | Repointed to ``empirical-barriers-ripl4.dat`` |
| ``empirical-barriers-new.dat``    | ``riplpy.fission.empirical_new``   | Repointed to ``empirical-barriers-ripl4.dat`` (alias) |
| ``empirical-hfb-barriers.dat``    | ``riplpy.fission.hfb``             | Loader logs a warning and returns an empty database |
| ``HFB2007/``                      | -                                  | Deferred |
| ``leveldensities/``               | -                                  | Deferred |

## Config keys

In ``riplpy/config.py``:

| Key                                | Relative path                                |
|------------------------------------|----------------------------------------------|
| ``fission_barriers_empirical``     | ``fission/empirical-barriers-ripl4.dat``     |
| ``fission_barriers_empirical_new`` | ``fission/empirical-barriers-ripl4.dat``     |
| ``fission_barriers_empire``        | ``fission/empirical-barriers-new-EMPIRE.dat``|
| ``fission_barriers_hfb``           | ``fission/empirical-hfb-barriers.dat``       |
| ``fission_barriers_bskg3``         | ``fission/barriers-bskg3.dat``               |
| ``fission_barriers_d1m``           | ``fission/barriers-d1m_lep.dat``             |
| ``fission_path_bskg3_dir``         | ``fission/hfbpath-bskg3``                    |
| ``fission_path_d1m_dir``           | ``fission/hfbpath-d1m``                      |
| ``fission_nld_bskg3_dir``          | ``fission/nld-fis-bskg3``                    |

## API

``riplpy.get_fission_barrier(Z, A, model=...)`` supports the model keys:
``empirical``, ``empirical_new``, ``empire``, ``hfb``, ``bskg3``, ``d1m``.
The ``BARRIER_MODELS`` dictionary in ``riplpy/fission/__init__.py``
maps these to the corresponding ``db.*`` attributes.

## Tests

Located in ``tests/test_fission.py``:

- ``TestEmpiricalBarriers``   — loads and validates the new RIPL-4 file.
- ``TestEmpiricalNew``        — exercises the backwards-compatibility alias.
- ``TestEmpire``              — implicit via API tests.
- ``TestHFBBarriers``         — skipped when the legacy file is absent.
- ``TestBSkG3Barriers``       — loads the 5-section RIPL-4 layout.
- ``TestD1MBarriers``         — loads the new D1M LEP file.
- ``TestFissionComparison``   — skipped if HFB data is unavailable.

## Deferred work

These directories ship raw per-isotope tables; adding readers would be
useful but is not required for the initial RIPL-4 release. The config
already declares directory keys (``fission_path_bskg3_dir``,
``fission_path_d1m_dir``, ``fission_nld_bskg3_dir``) so a future reader
can pick them up without further config changes.

1. ``hfbpath-bskg3/zXXX.dat`` — BSkG3 fission paths (2500 nuclei,
   90 <= Z <= 118). Per-isotope multi-record format: title line plus
   ``nbeta`` deformation samples. Suggested reader returns a mapping of
   ``Nuclide -> list[FissionPathPoint]``.
2. ``hfbpath-d1m/zXXXnYYY.dat`` — D1M fission paths. Same per-isotope
   format but keyed by Z and N (one file per nuclide).
3. ``nld-fis-bskg3/{Max1,Max2,Max3,Min1,Min2}/zXXX.dat`` — fission-related
   nuclear level densities at saddles/wells. Each file holds positive and
   negative parity energy-spin grids (60 energy rows, 50 spins).
4. ``RMF/`` — Relativistic Mean Field deformations and energy surfaces.
5. ``HFB2007/`` and ``leveldensities/`` legacy directories (RIPL-3) are
   removed from the GitHub release; readers for these are not planned.
