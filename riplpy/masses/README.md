# Masses Section

Nuclear mass data from various theoretical models and experimental compilations.

## Overview

The masses section provides access to:
- **AME2020** - Atomic Mass Evaluation 2020 (experimental masses)
- **FRDM2012** - Finite Range Droplet Model 2012
- **FRDM1995** - Finite Range Droplet Model 1995
- **HFB14** - Hartree-Fock-Bogoliubov model (version 14)
- **HFB27** - Hartree-Fock-Bogoliubov model (version 27)
- **BSkG3** - Brussels-Skyrme model
- **D1M** - Gogny D1M interaction
- **Natural Abundances** - Isotopic abundances in nature
- **Deformations** - Ground-state nuclear deformations
- **Densities** - Nuclear density distributions

## Quick Start

```python
import riplpy
import riplpy.masses as masses
from riplpy import Nuclide

# Load all mass data
masses.load(riplpy.get_path())

# Get experimental mass excess for Pb-208
pb208 = Nuclide(Z=82, A=208)
entry = masses.db.ame20.get(pb208)
print(f"Mass excess: {entry.Mexp:.3f} +/- {entry.Err:.3f} MeV")
```

## Available Models

| Model | Attribute | Mass Field | Description |
|-------|-----------|------------|-------------|
| AME2020 | `ame20` | `Mexp` | Experimental masses |
| FRDM2012 | `frdm12` | `Mth` | Theoretical (FRDM) |
| FRDM1995 | `frdm95` | `Mth` | Theoretical (FRDM) |
| HFB14 | `hfb14` | `Mth` | Theoretical (HFB) |
| HFB27 | `hfb27` | `Mth` | Theoretical (HFB) |
| BSkG3 | `bskg3` | `Mth` | Theoretical (BSkG) |
| D1M | `d1m` | `Mth` | Theoretical (Gogny) |

## Examples

### Basic Mass Lookup

```python
import riplpy
import riplpy.masses as masses
from riplpy import Nuclide

masses.load(riplpy.get_path())

# Create nucleus
fe56 = Nuclide(Z=26, A=56)

# Get experimental mass
ame = masses.db.ame20.get(fe56)
print(f"Fe-56 mass excess: {ame.Mexp:.4f} MeV")
print(f"Uncertainty: {ame.Err:.4f} MeV")
```

### Compare Mass Models

```python
import riplpy
import riplpy.masses as masses
from riplpy import Nuclide

masses.load(riplpy.get_path())

# Compare models for Sn-132 (doubly magic)
sn132 = Nuclide(Z=50, A=132)

models = [
    ('AME2020', masses.db.ame20, 'Mexp'),
    ('FRDM2012', masses.db.frdm12, 'Mth'),
    ('HFB27', masses.db.hfb27, 'Mth'),
]

print(f"Mass excess for Sn-132:")
for name, db, field in models:
    try:
        entry = db.get(sn132)
        value = getattr(entry, field)
        print(f"  {name}: {value:.3f} MeV")
    except KeyError:
        print(f"  {name}: Not available")
```

### Calculate Separation Energies

```python
import riplpy.masses as masses
from riplpy import Nuclide

masses.load(riplpy.get_path())

def one_neutron_separation(Z, A):
    """Calculate one-neutron separation energy S_n."""
    parent = Nuclide(Z=Z, A=A)
    daughter = Nuclide(Z=Z, A=A-1)
    neutron_mass = 8.071  # MeV (mass excess of neutron)

    m_parent = masses.db.ame20.get(parent).Mexp
    m_daughter = masses.db.ame20.get(daughter).Mexp

    return m_daughter + neutron_mass - m_parent

def two_neutron_separation(Z, A):
    """Calculate two-neutron separation energy S_2n."""
    parent = Nuclide(Z=Z, A=A)
    daughter = Nuclide(Z=Z, A=A-2)
    neutron_mass = 8.071  # MeV

    m_parent = masses.db.ame20.get(parent).Mexp
    m_daughter = masses.db.ame20.get(daughter).Mexp

    return m_daughter + 2*neutron_mass - m_parent

# Calculate separation energies for Pb isotopes
print("Pb isotope separation energies:")
print(f"{'A':>4} {'S_n (MeV)':>12} {'S_2n (MeV)':>12}")
for A in range(204, 210):
    try:
        sn = one_neutron_separation(82, A)
        s2n = two_neutron_separation(82, A)
        print(f"{A:4d} {sn:12.3f} {s2n:12.3f}")
    except KeyError:
        pass
```

### Calculate Q-values

```python
import riplpy.masses as masses
from riplpy import Nuclide

masses.load(riplpy.get_path())

def reaction_q_value(target, projectile, residual, ejectile):
    """Calculate Q-value for a nuclear reaction."""
    m_target = masses.db.ame20.get(target).Mexp
    m_proj = masses.db.ame20.get(projectile).Mexp
    m_res = masses.db.ame20.get(residual).Mexp
    m_eject = masses.db.ame20.get(ejectile).Mexp

    return (m_target + m_proj) - (m_res + m_eject)

# Q-value for 12C(p,gamma)13N
C12 = Nuclide(Z=6, A=12)
proton = Nuclide(Z=1, A=1)
N13 = Nuclide(Z=7, A=13)
gamma = Nuclide(Z=0, A=0)  # Zero mass excess for photon

# Note: For (p,gamma), ejectile mass excess is 0
m_C12 = masses.db.ame20.get(C12).Mexp
m_p = masses.db.ame20.get(proton).Mexp
m_N13 = masses.db.ame20.get(N13).Mexp

Q = (m_C12 + m_p) - m_N13
print(f"Q-value for 12C(p,gamma)13N: {Q:.3f} MeV")
```

### Filter by Properties

```python
import riplpy.masses as masses

masses.load(riplpy.get_path())

# Get all known masses for Z=50 (Tin)
sn_isotopes = masses.db.ame20.filter(Z=50)
print(f"Found {len(sn_isotopes.data)} Sn isotopes in AME2020")

# Get neutron-rich nuclei (N > Z)
neutron_rich = masses.db.ame20.filter(lambda e: e.n.N > e.n.Z)
print(f"Found {len(neutron_rich.data)} neutron-rich nuclei")

# Get nuclei with small mass uncertainty
precise = masses.db.ame20.filter(lambda e: e.Err is not None and e.Err < 0.01)
print(f"Found {len(precise.data)} nuclei with uncertainty < 10 keV")
```

### Natural Abundances

```python
import riplpy.masses as masses
from riplpy import Nuclide

masses.load(riplpy.get_path())

# Get natural abundances for Pb isotopes
print("Natural abundances of Pb isotopes:")
for A in [204, 206, 207, 208]:
    pb = Nuclide(Z=82, A=A)
    try:
        entry = masses.db.natab.get(pb)
        print(f"  Pb-{A}: {entry.abundance:.2f}%")
    except KeyError:
        print(f"  Pb-{A}: Not naturally occurring")
```

### Ground State Deformations

```python
import riplpy.masses as masses
from riplpy import Nuclide

masses.load(riplpy.get_path())

# Get deformation for U-238
u238 = Nuclide(Z=92, A=238)
deform = masses.db.deformations.get(u238)
print(f"U-238 ground state deformation:")
print(f"  beta2: {deform.beta2:.3f}")
print(f"  beta4: {deform.beta4:.3f}")
```

## Entry Fields

### AME2020 Entry
| Field | Description |
|-------|-------------|
| `n` | Nuclide object |
| `Mexp` | Experimental mass excess [MeV] |
| `Err` | Uncertainty [MeV] |
| `BE` | Binding energy [MeV] |
| `source` | Data source flag |

### Theoretical Mass Entry
| Field | Description |
|-------|-------------|
| `n` | Nuclide object |
| `Mth` | Theoretical mass excess [MeV] |
| `Emic` | Microscopic correction [MeV] |
| `beta2`, `beta4`, ... | Deformation parameters |

## Using with Main API

```python
import riplpy

riplpy.load()

# Convenience function
mass = riplpy.get_mass(82, 208, model='ame20')  # Direct value

# Or get full entry
entry = riplpy.get_mass_entry(82, 208, model='frdm12')

# Batch operations
nuclei = [(26, 56), (28, 58), (82, 208)]
masses_dict = riplpy.get_masses(nuclei, model='ame20')
```
