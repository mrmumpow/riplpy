

# Code version 
__version__ = "0.2.4"


# Local
from .collections import *
from . import densities
from . import fission
from . import gamma
from . import levels
from . import masses
from . import resonances


# Supported RIPL sections
sections = ('densities', 'fission', 'gamma', 'levels', 'masses', 'resonances')


def load() -> None:
    """Load the entire RIPL database. 

       Once this method is called, the databases cannot be unloaded.
    """
    for section in sections:
        eval(f"{section}.load()")


def in_ripl(x: Nuclide | Element) -> bool:
   """Check if the given Nuclide (or Element) is in the RIPL database. Returns True if so, False otherwise. 
      This method may only be used once riplpy.load() has been issued.

      Input:
         x [Nuclide | Element]: a Nuclide or Element object that may be in the RIPL database

      Output:
         [bool]: True if x in RIPL, False otherwise
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
   """Check if the given Nuclide (or Element) is in various databases of RIPL. Returns a list of database names where the nucleus can be found.
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
