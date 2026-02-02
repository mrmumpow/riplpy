# Fission Section

Fission barrier heights and parameters for actinide and transactinide nuclei.

## Overview

The fission section provides fission barrier data from both experimental compilations and theoretical calculations. Barriers are crucial for calculating fission cross sections and fission probabilities.

**Available Models:**
- **Empirical** - Experimental barrier heights
- **Empirical (New)** - Updated experimental compilation
- **EMPIRE** - EMPIRE code evaluated barriers
- **HFB** - Hartree-Fock-Bogoliubov theoretical barriers
- **BSkG3** - Brussels-Skyrme theoretical barriers

## Quick Start

```python
import riplpy
import riplpy.fission as fission
from riplpy import Nuclide

# Load fission data
fission.load(riplpy.get_path())

# Get fission barrier for U-235
u235 = Nuclide(Z=92, A=235)
barrier = fission.db.empirical_barriers.get(u235)
print(f"U-235 inner barrier: {barrier.Ea:.2f} MeV")
print(f"U-235 outer barrier: {barrier.Eb:.2f} MeV")
```

## Available Models

| Model | Attribute | Type | Description |
|-------|-----------|------|-------------|
| Empirical | `empirical_barriers` | Experimental | Recommended experimental barriers |
| Empirical (New) | `empirical_barriers_new` | Experimental | Updated compilation |
| EMPIRE | `empire_barriers` | Experimental | EMPIRE evaluated |
| HFB | `hfb_barriers` | Theoretical | HFB calculations |
| BSkG3 | `bskg3_barriers` | Theoretical | BSkG3 calculations |

## Examples

### Basic Barrier Lookup

```python
import riplpy
import riplpy.fission as fission
from riplpy import Nuclide

fission.load(riplpy.get_path())

# Get empirical barrier for Pu-239
pu239 = Nuclide(Z=94, A=239)
entry = fission.db.empirical_barriers.get(pu239)

# Actinides have double-humped barriers
print(f"Pu-239 double-humped barrier:")
print(f"  Inner barrier (Ea): {entry.Ea:.2f} MeV")
print(f"  Outer barrier (Eb): {entry.Eb:.2f} MeV")
print(f"  Inner curvature (hwa): {entry.hwa:.2f} MeV")
print(f"  Outer curvature (hwb): {entry.hwb:.2f} MeV")
```

### Compare Barrier Models

```python
import riplpy
import riplpy.fission as fission
from riplpy import Nuclide

fission.load(riplpy.get_path())

# Compare models for U isotopes (inner barrier heights)
print("Uranium fission barriers - Inner barrier (MeV):")
print(f"{'Isotope':>10} {'Empirical':>12} {'HFB':>12} {'BSkG3':>12}")

for A in range(232, 240):
    u = Nuclide(Z=92, A=A)
    values = []

    # Empirical barriers
    try:
        entry = fission.db.empirical_barriers.get(u)
        values.append(f"{entry.Ea:12.2f}")
    except KeyError:
        values.append("         N/A")

    # HFB barriers
    try:
        entry = fission.db.hfb_barriers.get(u)
        values.append(f"{entry.Bin:12.2f}")
    except KeyError:
        values.append("         N/A")

    # BSkG3 barriers
    try:
        entry = fission.db.bskg3_barriers.get(u)
        values.append(f"{entry.Bin:12.2f}")
    except KeyError:
        values.append("         N/A")

    print(f"U-{A:3d}:   " + " ".join(values))
```

### Double-Humped Barriers

```python
import riplpy
import riplpy.fission as fission
from riplpy import Nuclide

fission.load(riplpy.get_path())

# Actinides typically have double-humped barriers
actinides = [
    (92, 235, "U-235"),
    (92, 238, "U-238"),
    (94, 239, "Pu-239"),
    (94, 241, "Pu-241"),
]

print("Double-humped fission barriers (empirical):")
print(f"{'Nucleus':>10} {'Ea (MeV)':>10} {'hwa':>8} {'Eb (MeV)':>10} {'hwb':>8} {'sym_a':>6} {'sym_b':>6}")

for Z, A, name in actinides:
    n = Nuclide(Z=Z, A=A)
    try:
        entry = fission.db.empirical_barriers.get(n)
        print(f"{name:>10} {entry.Ea:10.2f} {entry.hwa:8.2f} {entry.Eb:10.2f} {entry.hwb:8.2f} {entry.syma:>6} {entry.symb:>6}")
    except KeyError:
        print(f"{name:>10} Not available")
```

### Barrier Curvatures

```python
import riplpy
import riplpy.fission as fission
from riplpy import Nuclide

fission.load(riplpy.get_path())

# Barrier curvature determines the transmission probability shape
u238 = Nuclide(Z=92, A=238)
entry = fission.db.empirical_barriers.get(u238)

print("U-238 barrier parameters:")
print(f"  Inner barrier (A):")
print(f"    Height (Ea): {entry.Ea:.2f} MeV")
print(f"    Curvature (hwa): {entry.hwa:.2f} MeV")
print(f"    Symmetry: {entry.syma}")
print(f"  Outer barrier (B):")
print(f"    Height (Eb): {entry.Eb:.2f} MeV")
print(f"    Curvature (hwb): {entry.hwb:.2f} MeV")
print(f"    Symmetry: {entry.symb}")
```

### Calculate Barrier Penetrability

```python
import riplpy
import riplpy.fission as fission
from riplpy import Nuclide
import math

fission.load(riplpy.get_path())

def hill_wheeler_penetrability(E, E_B, hw):
    """
    Calculate fission barrier penetrability using Hill-Wheeler formula.

    Args:
        E: Excitation energy [MeV]
        E_B: Barrier height [MeV]
        hw: Barrier curvature [MeV]

    Returns:
        Transmission coefficient T_f
    """
    if hw <= 0:
        return 1.0 if E > E_B else 0.0

    x = 2 * math.pi * (E - E_B) / hw
    return 1.0 / (1.0 + math.exp(-x))

# Get U-238 inner barrier
u238 = Nuclide(Z=92, A=238)
entry = fission.db.empirical_barriers.get(u238)

E_B = entry.Ea  # Inner barrier height
hw = entry.hwa   # Inner barrier curvature

print(f"U-238 fission penetrability (inner barrier Ea = {E_B:.2f} MeV):")
print(f"{'E (MeV)':>10} {'T_f':>12}")
for E in [4.0, 5.0, 5.5, 6.0, 6.5, 7.0, 8.0]:
    T = hill_wheeler_penetrability(E, E_B, hw)
    print(f"{E:10.1f} {T:12.4f}")
```

### Filter by Barrier Height

```python
import riplpy
import riplpy.fission as fission

fission.load(riplpy.get_path())

# Find nuclei with relatively low fission barriers
# HFB barriers use Bin for inner barrier height
low_barrier = fission.db.hfb_barriers.filter(
    lambda e: e.Bin is not None and e.Bin < 5.5
)
print(f"Nuclei with inner barrier < 5.5 MeV: {len(low_barrier.data)}")

# List them
for n, entry in list(low_barrier.data.items())[:10]:
    print(f"  {n.sym}-{n.A}: Bin = {entry.Bin:.2f} MeV")
```

## Entry Fields

### Empirical Barrier Entry
| Field | Description |
|-------|-------------|
| `n` | Nuclide object |
| `Ea` | Inner barrier height [MeV] |
| `hwa` | Inner barrier curvature [MeV] |
| `syma` | Inner saddle point symmetry |
| `Eb` | Outer barrier height [MeV] |
| `hwb` | Outer barrier curvature [MeV] |
| `symb` | Outer saddle point symmetry |
| `deltaf` | Fission splitting parameter [MeV] |

### HFB/BSkG3 Barrier Entry
| Field | Description |
|-------|-------------|
| `n` | Nuclide object |
| `Bin` | Inner barrier height [MeV] |
| `hwin` | Inner barrier curvature [MeV] |
| `Bout` | Outer barrier height [MeV] |
| `hwout` | Outer barrier curvature [MeV] |
| `Bout2` | Third barrier (if present) [MeV] |

### Saddle Point Symmetries
| Code | Meaning |
|------|---------|
| `S` | Symmetric |
| `GA` | Axially asymmetric (triaxial) |
| `MA` | Mass asymmetric |

## Using with Main API

```python
import riplpy

riplpy.load()

# Get fission barrier
barrier = riplpy.get_fission_barrier(92, 235, model='empirical')

# Batch operations
actinides = [(92, 235), (92, 238), (94, 239)]
barriers = riplpy.get_fission_barriers(actinides, model='hfb', skip_missing=True)
```

## Physical Background

Fission barriers arise from the competition between the attractive nuclear force and the repulsive Coulomb force as a nucleus deforms toward scission. Heavy nuclei (Z ≥ 90) typically have:

- **Inner barrier (A)**: First saddle point, often axially symmetric
- **Second minimum**: Shape isomer state
- **Outer barrier (B)**: Second saddle point, often mass-asymmetric

The barrier transmission probability is approximately:
```
T_f ≈ 1 / (1 + exp(-2π(E - E_B)/ℏω))
```
where E is the excitation energy, E_B is the barrier height, and ℏω is the curvature parameter.
