

# Code version 
__version__ = "0.2.4"

# Importlib
import importlib as _im

# Local
from .collections import *
from . import densities
from . import fission
from . import gamma
from . import levels
from . import masses
from . import resonances


# Supported RIPL sections
sections = ('densities', 'fission', 'gamma', 'levels')#, 'masses', 'resonances')


def _parallel_load(section: str) -> None:
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
         eval(f"{section}.load(directory='{directory}')")


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
      for db in eval(f"{section}.db.__all__"):
          if x in eval(f"{section}.db.{db}.data"):
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
      for db in eval(f"{section}.db.__all__"):
          if x in eval(f"{section}.db.{db}.data"):
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
      for db in eval(f"{section}.db.__all__"):
          if x in eval(f"{section}.db.{db}.data"):
              dbs.append((section, db))
   return dbs
