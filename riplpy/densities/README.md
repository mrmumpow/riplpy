# Densities Section

Nuclear level density parameters from various models.

## Overview

The densities section provides level density model parameters used in nuclear reaction calculations. Level densities describe the number of nuclear states per unit energy interval.

**Available Models:**
- **BSFG** - Back-Shifted Fermi Gas model
- **CT** - Constant Temperature model
- **EGSM** - Enhanced Generalized Superfluid Model
- **EGSM_NORM** - EGSM normalization parameters
- **HFB** - Hartree-Fock-Bogoliubov combinatorial model
- **Shell Corrections** - Microscopic shell correction energies

## Quick Start

```python
import riplpy
import riplpy.densities as densities
from riplpy import Nuclide

# Load level density data
densities.load(riplpy.get_path())

# Get BSFG parameters for Fe-57 (compound nucleus)
fe57 = Nuclide(Z=26, A=57)
entry = densities.db.bsfg.get(fe57)
print(f"Level density parameter a: {entry.ainf:.3f} MeV^-1")
print(f"Pairing shift: {entry.pairing:.3f} MeV")
```

## Available Models

| Model | Attribute | Description |
|-------|-----------|-------------|
| BSFG | `bsfg` | Back-Shifted Fermi Gas |
| CT | `ct` | Constant Temperature |
| EGSM | `egsm` | Enhanced Generalized Superfluid |
| EGSM Norm | `egsm_norm` | EGSM normalization |
| HFB | `hfb` | HFB combinatorial |
| Shell Corr. (MS) | `shellcorr_ms` | Möller-Swiatecki shell corrections |
| Shell Corr. (MK) | `shellcorr_mk` | Möller-Kratz shell corrections |

## Examples

### Basic Level Density Parameters

```python
import riplpy
import riplpy.densities as densities
from riplpy import Nuclide

densities.load(riplpy.get_path())

# Get BSFG parameters for Ni-60
ni60 = Nuclide(Z=28, A=60)
bsfg = densities.db.bsfg.get(ni60)

print(f"Ni-60 BSFG parameters:")
print(f"  Ground state spin: {bsfg.Io}")
print(f"  Neutron binding energy: {bsfg.Bn:.3f} MeV")
print(f"  Average s-wave spacing: {bsfg.Do:.1f} eV")
print(f"  Level density parameter: {bsfg.ainf:.3f} MeV^-1")
print(f"  Shell correction: {bsfg.dW:.3f} MeV")
print(f"  Pairing energy: {bsfg.pairing:.3f} MeV")
```

### Compare BSFG and CT Models

```python
import riplpy
import riplpy.densities as densities
from riplpy import Nuclide

densities.load(riplpy.get_path())

# Compare models for Sn isotopes
print("Sn isotope level density parameters:")
print(f"{'A':>4} {'a_BSFG':>10} {'T_CT':>10}")

for A in range(112, 126, 2):
    sn = Nuclide(Z=50, A=A)
    try:
        bsfg = densities.db.bsfg.get(sn)
        ct = densities.db.ct.get(sn)
        print(f"{A:4d} {bsfg.ainf:10.3f} {ct.T:10.3f}")
    except KeyError:
        pass
```

### Calculate Level Density (Fermi Gas)

```python
import riplpy
import riplpy.densities as densities
from riplpy import Nuclide
import math

densities.load(riplpy.get_path())

def fermi_gas_level_density(Z, A, U):
    """
    Calculate level density using Fermi gas formula.

    Args:
        Z: Atomic number
        A: Mass number
        U: Excitation energy above pairing [MeV]

    Returns:
        Level density [MeV^-1]
    """
    n = Nuclide(Z=Z, A=A)
    params = densities.db.bsfg.get(n)

    a = params.ainf  # Level density parameter [MeV^-1]

    if U <= 0:
        return 0.0

    # Fermi gas formula
    sqrt_aU = math.sqrt(a * U)
    rho = math.exp(2 * sqrt_aU) / (12 * math.sqrt(2) * a**0.25 * U**1.25)

    return rho

# Calculate level density for Fe-57 at various excitation energies
print("Fe-57 level density vs excitation energy:")
print(f"{'U (MeV)':>10} {'rho (MeV^-1)':>15}")
for U in [1, 2, 5, 10, 15, 20]:
    rho = fermi_gas_level_density(26, 57, U)
    print(f"{U:10.1f} {rho:15.2e}")
```

### Shell Corrections

```python
import riplpy
import riplpy.densities as densities
from riplpy import Nuclide

densities.load(riplpy.get_path())

# Get shell corrections for various nuclei
# (shell correction database uses compound nuclei)
nuclei = [
    (20, 41, "Ca-41"),
    (26, 57, "Fe-57"),
    (50, 119, "Sn-119"),
    (82, 209, "Pb-209"),
]

print("Shell correction energies (Möller-Swiatecki):")
for Z, A, name in nuclei:
    n = Nuclide(Z=Z, A=A)
    try:
        entry = densities.db.shellcorr_ms.get(n)
        print(f"  {name}: shell = {entry.shell:.3f}, corr = {entry.corr:.3f} MeV")
    except KeyError:
        print(f"  {name}: Not available")
```

### Spin-Dependent Level Densities (HFB)

```python
import riplpy
import riplpy.densities as densities
from riplpy import Nuclide

densities.load(riplpy.get_path())

# Get HFB level density table
fe56 = Nuclide(Z=26, A=56)
hfb = densities.db.hfb.get(fe56)

# Access positive parity data
pp = hfb.positive_parity

print(f"Fe-56 HFB level density (positive parity, first few values):")
print(f"{'U (MeV)':>10} {'rho_tot':>12} {'T (MeV)':>10}")
for i in range(min(10, len(pp.U))):
    print(f"{pp.U[i]:10.2f} {pp.rho_tot[i]:12.2e} {pp.T[i]:10.3f}")
```

### Filter Nuclei by Properties

```python
import riplpy
import riplpy.densities as densities

densities.load(riplpy.get_path())

# Find nuclei with large level density parameter
large_a = densities.db.bsfg.filter(lambda e: e.ainf > 20)
print(f"Nuclei with a > 20 MeV^-1: {len(large_a.data)}")

# Find nuclei with small pairing energy
small_pair = densities.db.bsfg.filter(lambda e: abs(e.pairing) < 0.5)
print(f"Nuclei with |pairing| < 0.5 MeV: {len(small_pair.data)}")
```

## Entry Fields

### BSFG Entry
| Field | Description |
|-------|-------------|
| `n` | Nuclide object |
| `Io` | Ground state spin |
| `Bn` | Neutron binding energy [MeV] |
| `Do` | Average s-wave resonance spacing [eV] |
| `Derr` | Uncertainty on spacing |
| `Nlow`, `Ulow` | Lowest discrete level used in fit |
| `Ntop`, `Utop` | Highest discrete level used in fit |
| `dW` | Shell correction energy [MeV] |
| `gamma` | Ignatyuk damping parameter |
| `ainf` | Asymptotic level density parameter [MeV^-1] |
| `aerr` | Uncertainty on ainf |
| `pairing` | Pairing energy shift [MeV] |

### CT Entry
| Field | Description |
|-------|-------------|
| `n` | Nuclide object |
| `T` | Nuclear temperature [MeV] |
| `E0` | Energy backshift [MeV] |

## Using with Main API

```python
import riplpy

riplpy.load()

# Get level density parameters
params = riplpy.get_level_density(26, 56, model='bsfg')
print(f"a = {params.ainf} MeV^-1")

# Batch operations
nuclei = [(26, 56), (28, 58), (50, 120)]
ld_params = riplpy.get_level_densities(nuclei, model='bsfg', skip_missing=True)
```

## Physical Background

The nuclear level density ρ(U, J, π) describes the number of nuclear states per unit energy at excitation energy U with spin J and parity π. It is a crucial ingredient in statistical nuclear reaction calculations.

**BSFG Model:**
```
ρ(U) = exp(2√(aU)) / (12√2 · a^(1/4) · U^(5/4) · σ)
```
where `a` is the level density parameter and `σ` is the spin cutoff parameter.

**CT Model:**
At low energies, level density follows:
```
ρ(U) = (1/T) · exp((U - E0)/T)
```
where `T` is the nuclear temperature.
