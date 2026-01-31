

# Code version
__version__ = "0.4.0"

# Logging
import logging as _logging

# Set up library-level logger with NullHandler (users can configure their own handlers)
logger = _logging.getLogger(__name__)
logger.addHandler(_logging.NullHandler())

# Importlib
import importlib as _im

# Local
from . import config as config
from .collections import *
from . import densities
from . import fission
from . import gamma
from . import levels
from . import masses
from . import resonances


# Supported RIPL sections
sections = ('densities', 'fission', 'gamma', 'levels', 'masses', 'resonances')


def _parallel_load(section: str) -> None:
   """An implicit method to load the given section in parallel. """
   if section in sections:
      i = _im.import_module(f"riplpy.{section}")
      i.load()


def load(directory: str, quick: bool = False) -> None:
   """Load the entire RIPL database from a specified directory on the local machine. 

      Once this method is called, the databases cannot be unloaded.
   """
   if quick:
      # @TODO: Re-evaluate the usefulness of this feature once database is complete
      import multiprocessing as _mp
      _pool = _mp.Pool(min(_mp.cpu_count(), len(sections)))
      _pool.map(_parallel_load, sections)
   else:
      for section in sections:
         module = globals()[section]
         module.load(directory=directory)


def in_ripl(x: Nuclide | Element) -> bool:
   """Check if the given Nuclide (or Element) appears anywhere in the RIPL database. Returns True if so, False otherwise. 
      This method may only be used once riplpy.load() has been issued.

      Input:
         x [Nuclide | Element]: a Nuclide or Element object that may be in the RIPL database

      Output:
         [bool]: True if x in RIPL, False otherwise

      Examples:
         (1) Check if input is in the RIPL database::
            $ import riplpy
            $ riplpy.load()
            $ n = riplpy.Nuclide(z=50, a=130)
            $ riplpy.in_ripl(n) # True
   """
   # Loop over each section of RIPL
   for section in sections:
      # Check the databases in this section
      for db in getattr(globals()[section], 'db')():
          if x in getattr(getattr(globals()[section], 'db'), db).data:
              return True
   return False


def in_sections(x: Nuclide | Element) -> list:
   """Check if the given Nuclide (or Element) is in various sections of the RIPL database. Returns a list of sections where True. 
      This method may only be used once riplpy.load() has been issued.

      Input:
         x [Nuclide | Element]: a Nuclide or Element object that may be in the RIPL database

      Output:
         [list]: A list of section names (as a string) x is in; empty otherwise

      Examples:
         (1) Return the section names that the input is in::
            $ import riplpy
            $ riplpy.load() # This will take some time
            $ n = riplpy.Nuclide(Z=46, a=119)
            $ riplpy.in_sections(n) # ['densities', 'gamma', 'levels', 'masses']
   """
   
   _sections = []
   # Loop over each section of RIPL
   for section in sections:
      # Check the databases in this section
      for db in getattr(globals()[section], 'db')():
          if x in getattr(getattr(globals()[section], 'db'), db).data:
              _sections.append(section)
              break
   return _sections


def in_dbs(x: Nuclide | Element) -> list:
   """Check if the given Nuclide (or Element) is in various databases of RIPL. Returns a list of database names where the object can be found.
      This method may only be used once riplpy.load() has been issued.

      Input:
         x [Nuclide | Element]: a Nuclide or Element object that may be in the RIPL database

      Output:
         [list]: A list of tuples that includes the section name (as a string) and the database name (as a string) that x is in; empty otherwise
   """
   dbs = []
   # Loop over each section of RIPL
   for section in sections:
      # Check the databases in this section
      for db in getattr(globals()[section], 'db')():
          if x in getattr(getattr(globals()[section], 'db'), db).data:
              dbs.append((section, db))
   return dbs


# ========================
# Convenience Functions
# ========================

def _resolve_nucleus(Z_or_nuclide, A=None) -> Nuclide:
    """Resolve input to a Nuclide object.

    Accepts either:
        - A Nuclide/Nucleus object directly
        - Z and A as separate arguments
    """
    if isinstance(Z_or_nuclide, (Nuclide, Nucleus)):
        return Z_or_nuclide
    if A is None:
        raise ValueError("Must provide either a Nuclide or both Z and A")
    return Nuclide(Z=Z_or_nuclide, A=A)


def get_mass(Z_or_nuclide, A: int = None, model: str = 'ame20') -> float:
    """Get the mass excess for a nucleus from a specified mass model.

    Args:
        Z_or_nuclide: Either a Nuclide/Nucleus object, or the atomic number Z
        A: Mass number (required if Z_or_nuclide is an integer)
        model: Mass model to use. Options: 'ame20', 'frdm12', 'frdm95',
               'hfb14', 'hfb27', 'bskg3', 'd1m'. Default: 'ame20'

    Returns:
        Mass excess in MeV

    Examples:
        >>> riplpy.get_mass(82, 208)  # Using Z, A
        -21.749
        >>> riplpy.get_mass(Nuclide(Z=82, A=208), model='frdm12')
        -21.352

    Raises:
        ValueError: If the model is not recognized
        NucleusNotFoundError: If the nucleus is not in the database
    """
    n = _resolve_nucleus(Z_or_nuclide, A)

    if model not in masses.MASS_MODELS:
        raise ValueError(f"Unknown mass model '{model}'. Available: {list(masses.MASS_MODELS.keys())}")

    db_name, field = masses.MASS_MODELS[model]
    db = getattr(masses.db, db_name)
    entry = db.get(n)
    return getattr(entry, field)


def get_mass_entry(Z_or_nuclide, A: int = None, model: str = 'ame20') -> object:
    """Get the full mass entry for a nucleus from a specified mass model.

    Args:
        Z_or_nuclide: Either a Nuclide/Nucleus object, or the atomic number Z
        A: Mass number (required if Z_or_nuclide is an integer)
        model: Mass model to use. Options: 'ame20', 'frdm12', 'frdm95',
               'hfb14', 'hfb27', 'bskg3', 'd1m'. Default: 'ame20'

    Returns:
        Entry object with all available mass data for that model

    Raises:
        ValueError: If the model is not recognized
        NucleusNotFoundError: If the nucleus is not in the database
    """
    n = _resolve_nucleus(Z_or_nuclide, A)

    if model not in masses.MASS_MODELS:
        raise ValueError(f"Unknown mass model '{model}'. Available: {list(masses.MASS_MODELS.keys())}")

    db_name, _ = masses.MASS_MODELS[model]
    db = getattr(masses.db, db_name)
    return db.get(n)


def get_level_density(Z_or_nuclide, A: int = None, model: str = 'bsfg') -> object:
    """Get level density parameters for a nucleus from a specified model.

    Args:
        Z_or_nuclide: Either a Nuclide/Nucleus object, or the atomic number Z
        A: Mass number (required if Z_or_nuclide is an integer)
        model: Level density model. Options: 'bsfg', 'ct', 'egsm', 'egsm_norm', 'hfb'. Default: 'bsfg'

    Returns:
        Entry object containing level density parameters (model-dependent fields)

    Raises:
        ValueError: If the model is not recognized
        NucleusNotFoundError: If the nucleus is not in the database
    """
    n = _resolve_nucleus(Z_or_nuclide, A)

    if model not in densities.LEVEL_DENSITY_MODELS:
        raise ValueError(f"Unknown level density model '{model}'. Available: {list(densities.LEVEL_DENSITY_MODELS.keys())}")

    db = getattr(densities.db, densities.LEVEL_DENSITY_MODELS[model])
    return db.get(n)


def get_gdr(Z_or_nuclide, A: int = None) -> object:
    """Get Giant Dipole Resonance (GDR) parameters for a nucleus.

    Args:
        Z_or_nuclide: Either a Nuclide/Nucleus object, or the atomic number Z
        A: Mass number (required if Z_or_nuclide is an integer)

    Returns:
        Entry object containing GDR parameters

    Raises:
        NucleusNotFoundError: If the nucleus is not in the database
    """
    n = _resolve_nucleus(Z_or_nuclide, A)
    return gamma.db.theory_gdr.get(n)


def get_resonance(Z_or_nuclide, A: int = None, wave: str = 's') -> object:
    """Get resonance parameters for a nucleus.

    Args:
        Z_or_nuclide: Either a Nuclide/Nucleus object, or the atomic number Z
        A: Mass number (required if Z_or_nuclide is an integer)
        wave: Resonance type - 's' (s-wave) or 'p' (p-wave). Default: 's'

    Returns:
        Entry object containing resonance parameters

    Raises:
        ValueError: If the wave type is not recognized
        NucleusNotFoundError: If the nucleus is not in the database
    """
    n = _resolve_nucleus(Z_or_nuclide, A)

    if wave == 's':
        return resonances.db.swave.get(n)
    elif wave == 'p':
        return resonances.db.pwave.get(n)
    else:
        raise ValueError(f"Unknown wave type '{wave}'. Available: 's', 'p'")


def get_fission_barrier(Z_or_nuclide, A: int = None, model: str = 'empirical') -> object:
    """Get fission barrier parameters for a nucleus.

    Args:
        Z_or_nuclide: Either a Nuclide/Nucleus object, or the atomic number Z
        A: Mass number (required if Z_or_nuclide is an integer)
        model: Barrier model. Options: 'empirical', 'empirical_new', 'empire',
               'hfb', 'bskg3'. Default: 'empirical'

    Returns:
        Entry object containing fission barrier parameters

    Raises:
        ValueError: If the model is not recognized
        NucleusNotFoundError: If the nucleus is not in the database
    """
    n = _resolve_nucleus(Z_or_nuclide, A)

    if model not in fission.BARRIER_MODELS:
        raise ValueError(f"Unknown fission barrier model '{model}'. Available: {list(fission.BARRIER_MODELS.keys())}")

    db = getattr(fission.db, fission.BARRIER_MODELS[model])
    return db.get(n)
