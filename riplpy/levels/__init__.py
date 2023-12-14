
# Dataclass
from dataclasses import dataclass

decay_modes = {'%B-'    : 'β- decay', 
               '%EC'    : 'electron capture',
               '%EC+%B+': 'electron capture and β+ decay',
               '%N'     : 'neutron decay',
               '%A'     : 'α decay',
               '%IT'    : 'isomeric transition',
               '%P'     : 'proton decay',
               '%3HE'   : '3He decay',
               '%B+P'   : 'β+ delayed proton decay',
               '%B-N'   : 'β- delayed neutron decay',
               '%SF'    : 'spontaneous fission',
               '%ECP'   : 'electron capture delayed proton decay',
               '%ECA'   : 'electron capture delayed alpha decay',
               '%G'     : 'gamma decay',
               '%B-2N'  : 'β- delayed double neutron decay',
               '%B+2P'  : 'β+ delayed double proton decay',
              }


decay_modes_shorthand   = tuple(decay_modes.keys())
decay_modes_description = tuple(decay_modes.values())


@dataclass
class DiscreteNuclearLevel(object):
    """A basic representation of a discrete nuclear level. """

    energy     : float = None # Energy, typically in [MeV]
    spin       : float = None # Spin as a float (with sign)
    parity     : int   = None # Either +1 or -1
