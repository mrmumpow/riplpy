
# RIPLpy
import riplpy as _riplpy
from riplpy.db import _DbAccessor
from riplpy.exceptions import RiplFileNotFoundError as _RiplFileNotFoundError

# Local
from .core import *
from . import bskg3 as bskg3
from . import d1m as d1m
from . import empirical as emp
from . import empirical_new as emp_new
from . import empire as empire
from . import hfb

# ========================

saddle_shorthand = {'S' : 'symmetric',
                    'GA': 'axially asymmetric (triaxial)',
                    'MA': 'mass asymmetric',
                    '  ': '',
                   }

db = _DbAccessor()

# ========================

# Model map: user-friendly name -> db attribute name
BARRIER_MODELS = {
    'empirical': 'empirical_barriers',
    'empirical_new': 'empirical_barriers_new',
    'empire': 'empire_barriers',
    'hfb': 'hfb_barriers',
    'bskg3': 'bskg3_barriers',
    'd1m': 'd1m_barriers',
}

# ========================


def _safe_load(loader, model_name: str, directory: str, db_cls):
    """Load a database, returning an empty instance if the data file is missing.

    Some RIPL-4 release layouts no longer include legacy data files. Rather
    than failing hard, we log a warning and proceed with an empty database so
    that other models remain usable.
    """
    try:
        return loader(directory=directory)
    except (FileNotFoundError, _RiplFileNotFoundError) as exc:
        _riplpy.logger.warning(
            "fission: %s data file not found (%s); using empty database.",
            model_name, exc,
        )
        return db_cls()


def load(directory: str) -> None:
    """Load the entire database of the Fission section of RIPL from a specified directory.

       Once this method is called, the databases cannot be unloaded.
    """

    # Empirical fission barrier databases (RIPL-4)
    db.empirical_barriers     = _safe_load(emp.load,     'empirical',     directory, emp.Database)
    db.empirical_barriers_new = _safe_load(emp_new.load, 'empirical_new', directory, emp_new.Database)
    db.empire_barriers        = _safe_load(empire.load,  'empire',        directory, empire.Database)

    # Theoretical BSkG3 fission barrier database
    db.bskg3_barriers = _safe_load(bskg3.load, 'bskg3', directory, bskg3.Database)

    # Theoretical HFB fission barrier database (legacy; file may be absent)
    db.hfb_barriers = _safe_load(hfb.load, 'hfb', directory, hfb.Database)

    # Theoretical D1M HFB fission barrier database (RIPL-4)
    db.d1m_barriers = _safe_load(d1m.load, 'd1m', directory, d1m.Database)
