# Gamma Section

Giant Dipole Resonance (GDR) parameters and gamma-ray strength functions.

## Overview

The gamma section provides data for calculating gamma-ray emission in nuclear reactions, including:

- **GDR Parameters** - Giant Dipole Resonance energies and widths
- **Gamma Strength Functions** - E1 photon strength function tables
- **Experimental GDR** - Measured GDR parameters with uncertainties

**Available Databases:**
- **theory_gdr** - Theoretical GDR parameters (systematics)
- **experiment_slo** - Experimental Single Lorentzian fits
- **experiment_mlo** - Experimental Modified Lorentzian fits
- **gsf** - Tabulated gamma strength functions

## Quick Start

```python
import riplpy
import riplpy.gamma as gamma
from riplpy import Nuclide

# Load gamma data
gamma.load(riplpy.get_path())

# Get GDR parameters for Pb-208
pb208 = Nuclide(Z=82, A=208)
gdr = gamma.db.theory_gdr.get(pb208)
print(f"GDR energy: {gdr.E1:.2f} MeV")
print(f"GDR width: {gdr.W1:.2f} MeV")
```

## Available Databases

| Database | Attribute | Description |
|----------|-----------|-------------|
| Theory GDR | `theory_gdr` | Theoretical systematics |
| Exp. SLO | `experiment_slo` | Single Lorentzian fits |
| Exp. MLO | `experiment_mlo` | Modified Lorentzian fits |
| GSF | `gsf` | Tabulated strength functions |

## Examples

### Basic GDR Parameters

```python
import riplpy
import riplpy.gamma as gamma
from riplpy import Nuclide

gamma.load(riplpy.get_path())

# Get theoretical GDR for medium-mass nucleus
fe56 = Nuclide(Z=26, A=56)
gdr = gamma.db.theory_gdr.get(fe56)

print(f"Fe-56 Giant Dipole Resonance:")
print(f"  Energy E1: {gdr.E1:.2f} MeV")
print(f"  Width W1: {gdr.W1:.2f} MeV")
print(f"  Deformation eta: {gdr.eta:.3f}")
```

### GDR for Deformed Nuclei

```python
import riplpy
import riplpy.gamma as gamma
from riplpy import Nuclide

gamma.load(riplpy.get_path())

# Deformed nuclei have split GDR (two peaks)
u238 = Nuclide(Z=92, A=238)
gdr = gamma.db.theory_gdr.get(u238)

print(f"U-238 Giant Dipole Resonance (deformed nucleus):")
print(f"  First peak:  E1 = {gdr.E1:.2f} MeV, W1 = {gdr.W1:.2f} MeV")
print(f"  Second peak: E2 = {gdr.E2:.2f} MeV, W2 = {gdr.W2:.2f} MeV")
print(f"  Deformation: eta = {gdr.eta:.3f}")
```

### Compare Theory and Experiment

```python
import riplpy
import riplpy.gamma as gamma
from riplpy import Nuclide

gamma.load(riplpy.get_path())

# Compare for spherical nucleus (Pb-208)
pb208 = Nuclide(Z=82, A=208)

theory = gamma.db.theory_gdr.get(pb208)

print(f"Pb-208 GDR comparison:")
print(f"  Theory: E = {theory.E1:.2f} MeV, W = {theory.W1:.2f} MeV")

try:
    exp_slo = gamma.db.experiment_slo.get(pb208)
    print(f"  Exp SLO: E = {exp_slo.Er1:.2f} MeV, W = {exp_slo.Wr1:.2f} MeV")
except KeyError:
    print(f"  Exp SLO: Not available")
```

### GDR Systematics Across Isotopes

```python
import riplpy
import riplpy.gamma as gamma
from riplpy import Nuclide

gamma.load(riplpy.get_path())

# GDR parameters for Sn isotopes
print("GDR parameters for Sn isotopes:")
print(f"{'A':>4} {'E (MeV)':>10} {'W (MeV)':>10} {'eta':>8}")

for A in range(112, 130, 2):
    sn = Nuclide(Z=50, A=A)
    try:
        gdr = gamma.db.theory_gdr.get(sn)
        print(f"{A:4d} {gdr.E1:10.2f} {gdr.W1:10.2f} {gdr.eta:8.3f}")
    except KeyError:
        pass
```

### Calculate Lorentzian Strength Function

```python
import riplpy
import riplpy.gamma as gamma
from riplpy import Nuclide
import math

gamma.load(riplpy.get_path())

def standard_lorentzian(E_gamma, E_gdr, Gamma_gdr, sigma_gdr):
    """
    Calculate Standard Lorentzian E1 strength function.

    Args:
        E_gamma: Gamma-ray energy [MeV]
        E_gdr: GDR centroid energy [MeV]
        Gamma_gdr: GDR width [MeV]
        sigma_gdr: GDR peak cross section [mb]

    Returns:
        Strength function f_E1 [MeV^-3]
    """
    # SLO formula
    numer = sigma_gdr * Gamma_gdr**2 * E_gamma
    denom = (E_gamma**2 - E_gdr**2)**2 + (E_gamma * Gamma_gdr)**2

    # Convert mb to MeV^-3 (factor of 8.674e-8 * A^(-5/3))
    return numer / denom

# Get GDR for Fe-56
fe56 = Nuclide(Z=26, A=56)
gdr = gamma.db.theory_gdr.get(fe56)

# Approximate peak cross section from TRK sum rule
sigma_0 = 60 * 56 / 56  # mb (rough estimate)

print("Fe-56 E1 strength function:")
print(f"{'E_gamma (MeV)':>15} {'f_E1 (arb)':>12}")
for E in [5, 10, 15, 17, 20, 25]:
    f = standard_lorentzian(E, gdr.E1, gdr.W1, sigma_0)
    print(f"{E:15.1f} {f:12.4f}")
```

### Tabulated Gamma Strength Functions

```python
import riplpy
import riplpy.gamma as gamma
from riplpy import Nuclide

gamma.load(riplpy.get_path())

# Get tabulated GSF for a nucleus
fe56 = Nuclide(Z=26, A=56)

try:
    gsf = gamma.db.gsf.get(fe56)
    print(f"Fe-56 tabulated gamma strength function:")
    print(f"{'U (MeV)':>10} {'f_E1 (mb/MeV)':>15}")
    for i in range(min(10, len(gsf.U))):
        print(f"{gsf.U[i]:10.2f} {gsf.fE1[i]:15.6f}")
except KeyError:
    print("Tabulated GSF not available for Fe-56")
```

### Filter by GDR Properties

```python
import riplpy
import riplpy.gamma as gamma

gamma.load(riplpy.get_path())

# Find nuclei with narrow GDR (W < 3 MeV)
narrow_gdr = gamma.db.theory_gdr.filter(lambda e: e.W1 < 3.0)
print(f"Nuclei with GDR width < 3 MeV: {len(narrow_gdr.data)}")

# Find deformed nuclei (large eta)
deformed = gamma.db.theory_gdr.filter(lambda e: e.eta > 0.2)
print(f"Deformed nuclei (eta > 0.2): {len(deformed.data)}")

# List some deformed nuclei
for n, gdr in list(deformed.data.items())[:5]:
    print(f"  {n.sym}-{n.A}: eta = {gdr.eta:.3f}, E1 = {gdr.E1:.1f}, E2 = {gdr.E2:.1f} MeV")
```

## Entry Fields

### Theory GDR Entry
| Field | Description |
|-------|-------------|
| `n` | Nuclide object |
| `E1` | First GDR peak energy [MeV] |
| `W1` | First GDR peak width [MeV] |
| `E2` | Second GDR peak energy [MeV] (deformed) |
| `W2` | Second GDR peak width [MeV] (deformed) |
| `eta` | Deformation parameter |

### Experimental GDR Entry
| Field | Description |
|-------|-------------|
| `n` | Nuclide object |
| `Er1`, `dEr1` | First peak energy and uncertainty [MeV] |
| `Wr1`, `dWr1` | First peak width and uncertainty [MeV] |
| `Sr1`, `dSr1` | First peak strength and uncertainty |
| `Er2`, `Wr2`, `Sr2` | Second peak parameters |
| `Emin`, `Emax` | Energy range of fit [MeV] |
| `ref` | Reference string |

### GSF Entry
| Field | Description |
|-------|-------------|
| `n` | Nuclide object |
| `U` | Excitation energy grid [MeV] |
| `fE1` | E1 strength function values [mb/MeV] |

## Using with Main API

```python
import riplpy

riplpy.load()

# Get GDR parameters
gdr = riplpy.get_gdr(82, 208)
print(f"E = {gdr.E1} MeV, W = {gdr.W1} MeV")

# Batch operations
nuclei = [(82, 208), (50, 120), (26, 56)]
gdrs = riplpy.get_gdrs(nuclei, skip_missing=True)
```

## Physical Background

The Giant Dipole Resonance (GDR) is a collective nuclear excitation where protons oscillate against neutrons. It dominates the photoabsorption cross section at energies around 10-25 MeV.

**Systematics:**
- Spherical nuclei: Single peak at E ≈ 80/A^(1/3) MeV
- Deformed nuclei: Split into two peaks along major/minor axes
- Width: Γ ≈ 4-6 MeV (includes spreading width + escape width)

**Gamma Strength Function:**
The E1 strength function f_E1(E_γ) is related to the photoabsorption cross section:
```
f_E1(E_γ) = σ_abs(E_γ) / (3π²ℏ²c²E_γ)
```
