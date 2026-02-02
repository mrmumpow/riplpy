# Resonances Section

Neutron resonance parameters for s-wave and p-wave capture.

## Overview

The resonances section provides average resonance parameters from neutron capture measurements, including:

- **S-wave (l=0)** - Average s-wave resonance spacing and strength functions
- **P-wave (l=1)** - Average p-wave resonance spacing and strength functions

These parameters are essential for calculating neutron capture cross sections and level densities at the neutron separation energy.

## Quick Start

```python
import riplpy
import riplpy.resonances as resonances
from riplpy import Nuclide

# Load resonance data
resonances.load(riplpy.get_path())

# Get s-wave parameters for U-238
u238 = Nuclide(Z=92, A=238)
swave = resonances.db.swave.get(u238)

print(f"U-238 s-wave resonance spacing: {swave.D:.4f} keV")
print(f"Neutron strength function: {swave.Str:.4f} × 10^-4")
```

## Available Databases

| Database | Attribute | Description |
|----------|-----------|-------------|
| S-wave | `swave` | S-wave (l=0) resonance parameters (~300 nuclei) |
| P-wave | `pwave` | P-wave (l=1) resonance parameters (~119 nuclei) |

## Examples

### Basic Resonance Parameters

```python
import riplpy
import riplpy.resonances as resonances
from riplpy import Nuclide

resonances.load(riplpy.get_path())

# Get resonance parameters for Fe-56
fe56 = Nuclide(Z=26, A=56)
swave = resonances.db.swave.get(fe56)

print(f"Fe-56 s-wave resonance parameters:")
print(f"  Target spin I_0: {swave.Io}")
print(f"  Neutron binding energy: {swave.Bn:.3f} MeV")
print(f"  Resonance spacing D_0: {swave.D:.2f} ± {swave.Derr:.2f} keV")
print(f"  Strength function S_0: {swave.Str:.4f} ± {swave.Serr:.4f} × 10^-4")
print(f"  Radiative width Γ_γ: {swave.Gam:.1f} ± {swave.Gerr:.1f} meV")
```

### Compare S-wave and P-wave

```python
import riplpy
import riplpy.resonances as resonances
from riplpy import Nuclide

resonances.load(riplpy.get_path())

# Compare s-wave and p-wave for various nuclei
nuclei = [
    (26, 56, "Fe-56"),
    (82, 208, "Pb-208"),
    (92, 238, "U-238"),
]

print("S-wave vs P-wave resonance spacing:")
print(f"{'Nucleus':>10} {'D_0 (keV)':>12} {'D_1 (keV)':>12} {'Ratio':>8}")

for Z, A, name in nuclei:
    n = Nuclide(Z=Z, A=A)
    try:
        swave = resonances.db.swave.get(n)
        D0 = swave.D
    except KeyError:
        D0 = None

    try:
        pwave = resonances.db.pwave.get(n)
        D1 = pwave.D
    except KeyError:
        D1 = None

    if D0 and D1:
        ratio = D0 / D1
        print(f"{name:>10} {D0:12.2f} {D1:12.2f} {ratio:8.2f}")
    elif D0:
        print(f"{name:>10} {D0:12.2f} {'N/A':>12} {'---':>8}")
```

### Neutron Strength Functions

```python
import riplpy
import riplpy.resonances as resonances
from riplpy import Nuclide

resonances.load(riplpy.get_path())

# S-wave strength function systematics
print("S-wave neutron strength functions:")
print(f"{'Nucleus':>10} {'S_0 (×10^-4)':>15}")

for Z in [26, 28, 29, 50, 82, 92]:
    for A in range(Z*2, Z*3, 4):  # Rough range
        n = Nuclide(Z=Z, A=A)
        try:
            swave = resonances.db.swave.get(n)
            print(f"{n.sym}-{n.A:3d}:   {swave.Str:15.4f}")
        except KeyError:
            pass
```

### Calculate Level Density at Bn

```python
import riplpy
import riplpy.resonances as resonances
from riplpy import Nuclide
import math

resonances.load(riplpy.get_path())

def level_density_at_Bn(Z, A):
    """
    Calculate level density at neutron separation energy from resonance spacing.

    The relationship is:
        ρ(B_n, J, π) = 1 / (D_0 × (2J+1))

    For s-wave neutrons on even-even target (I_0 = 0):
        ρ_tot(B_n) ≈ 2 / D_0

    Args:
        Z: Target atomic number
        A: Target mass number

    Returns:
        Level density at B_n [MeV^-1]
    """
    n = Nuclide(Z=Z, A=A)
    swave = resonances.db.swave.get(n)

    D0_keV = swave.D  # Resonance spacing in keV
    D0_MeV = D0_keV * 1e-3  # Convert to MeV
    I0 = swave.Io  # Target spin

    # For s-wave, compound nucleus has J = I_0 ± 1/2
    # Level density includes both spin states
    rho = 2.0 / D0_MeV  # Approximate total level density

    return rho, swave.Bn

# Calculate for several nuclei
print("Level density at neutron separation energy:")
print(f"{'Nucleus':>10} {'B_n (MeV)':>12} {'ρ (MeV^-1)':>15}")

for Z, A in [(26, 56), (50, 120), (82, 208), (92, 238)]:
    try:
        rho, Bn = level_density_at_Bn(Z, A)
        n = Nuclide(Z=Z, A=A)
        print(f"{n.sym}-{n.A:3d}:   {Bn:12.3f} {rho:15.2e}")
    except KeyError:
        pass
```

### Radiative Widths

```python
import riplpy
import riplpy.resonances as resonances
from riplpy import Nuclide

resonances.load(riplpy.get_path())

# Average radiative widths
print("Average radiative widths:")
print(f"{'Nucleus':>10} {'Γ_γ (meV)':>12} {'Uncertainty':>12}")

for Z, A in [(26, 56), (28, 60), (50, 120), (82, 208), (92, 238)]:
    n = Nuclide(Z=Z, A=A)
    try:
        swave = resonances.db.swave.get(n)
        print(f"{n.sym}-{n.A:3d}:   {swave.Gam:12.1f} {swave.Gerr:12.1f}")
    except KeyError:
        pass
```

### Filter by Properties

```python
import riplpy
import riplpy.resonances as resonances

resonances.load(riplpy.get_path())

# Find nuclei with large resonance spacing (sparse spectrum)
large_spacing = resonances.db.swave.filter(lambda e: e.D > 10)  # D > 10 keV
print(f"Nuclei with D_0 > 10 keV: {len(large_spacing.data)}")

for n, entry in list(large_spacing.data.items())[:5]:
    print(f"  {n.sym}-{n.A}: D_0 = {entry.D:.1f} keV")

# Find nuclei with large strength function (s-wave giant resonance)
large_S0 = resonances.db.swave.filter(lambda e: e.Str > 2.0)
print(f"\nNuclei with S_0 > 2 × 10^-4: {len(large_S0.data)}")

for n, entry in list(large_S0.data.items())[:5]:
    print(f"  {n.sym}-{n.A}: S_0 = {entry.Str:.2f} × 10^-4")
```

### Estimate Capture Cross Section

```python
import riplpy
import riplpy.resonances as resonances
from riplpy import Nuclide
import math

resonances.load(riplpy.get_path())

def thermal_capture_estimate(Z, A):
    """
    Rough estimate of thermal neutron capture cross section.

    Uses: σ_th ≈ 2.608 × 10^6 × (Γ_n × Γ_γ) / (D × E_n)

    This is a very rough approximation!
    """
    n = Nuclide(Z=Z, A=A)
    swave = resonances.db.swave.get(n)

    # Parameters
    D0 = swave.D * 1e3  # Convert keV to eV
    Gam_gamma = swave.Gam * 1e-3  # Convert meV to eV
    S0 = swave.Str * 1e-4  # Strength function

    # Estimate neutron width at thermal energy (0.0253 eV)
    E_th = 0.0253  # eV
    A_target = A
    Gam_n = 2 * S0 * E_th**0.5  # Approximate

    # Very rough cross section estimate
    sigma_approx = 2.608e6 * (Gam_n * Gam_gamma) / (D0 * E_th)

    return sigma_approx

# Note: This is just for illustration - real calculations are more complex
print("Rough thermal capture cross section estimates:")
for Z, A in [(26, 56), (50, 120), (92, 238)]:
    try:
        sigma = thermal_capture_estimate(Z, A)
        n = Nuclide(Z=Z, A=A)
        print(f"  {n.sym}-{n.A}: σ_th ≈ {sigma:.1f} barn (rough estimate)")
    except KeyError:
        pass
```

## Entry Fields

### S-wave Entry
| Field | Description |
|-------|-------------|
| `n` | Target nuclide |
| `Io` | Target ground state spin |
| `Bn` | Neutron binding energy [MeV] |
| `D` | Average s-wave resonance spacing [keV] |
| `Derr` | Uncertainty on D [keV] |
| `Str` | S-wave neutron strength function [×10^-4] |
| `Serr` | Uncertainty on strength function |
| `Gam` | Average radiative width [meV] |
| `Gerr` | Uncertainty on radiative width |
| `ref` | Reference string |

### P-wave Entry
| Field | Description |
|-------|-------------|
| `n` | Target nuclide |
| `Io` | Target ground state spin |
| `Bn` | Neutron binding energy [MeV] |
| `D` | Average p-wave resonance spacing [keV] |
| `Derr` | Uncertainty on D [keV] |
| `Str` | P-wave neutron strength function [×10^-4] |
| `Serr` | Uncertainty on strength function |
| `ref` | Reference string |

## Using with Main API

```python
import riplpy

riplpy.load()

# Get resonance parameters
res = riplpy.get_resonance(92, 238, wave='s')
print(f"D_0 = {res.D} keV")

# Batch operations
nuclei = [(26, 56), (50, 120), (82, 208)]
resonances_dict = riplpy.get_resonances(nuclei, wave='s', skip_missing=True)
```

## Physical Background

Average resonance parameters describe the statistical properties of neutron-induced compound nucleus resonances near the neutron separation energy.

**S-wave (l=0):**
- No centrifugal barrier
- Dominant at thermal energies
- Spacing D_0 inversely proportional to level density

**P-wave (l=1):**
- Centrifugal barrier suppresses thermal capture
- Becomes important at higher energies
- Generally D_1 < D_0 (more levels)

**Strength Function:**
The neutron strength function S_l is defined as:
```
S_l = ⟨Γ_n^l⟩ / D_l
```
where ⟨Γ_n^l⟩ is the average reduced neutron width. It shows systematic variations with mass number due to nuclear structure effects.
