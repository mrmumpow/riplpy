# -*- coding: utf-8 -*-
"""A configuration file for RIPL database access.

This file provides a centralized location for managing file paths and other
configuration settings for the RIPLpy library. It includes a mechanism to
read the RIPL database location from an environment variable and issues a
warning if it is not set.

Attributes:
    RIPL_PATH (str): The local filesystem path to the RIPL database. This is 
        determined by the `RIPL_LOCATION` environment variable. If the 
        environment variable is not set, a warning is issued, and this 
        is set to an empty string.
"""

# OS
import os

# Warnings
import warnings

# Environment Variable for RIPL Database Location
RIPL_PATH = os.environ.get('RIPL_LOCATION', '')

if not RIPL_PATH:
    warnings.warn(
        "The 'RIPL_LOCATION' environment variable is not set. "
        "Without this, RIPLpy may not be able to locate the necessary data files. "
        "Please set this variable to the root directory of your RIPL database.",
        UserWarning
    )

# Standardized Relative Paths for ASCII Files

# This section provides a centralized mapping of descriptive names to the
# relative paths of the ASCII data files within the RIPL database. This
# helps to avoid hardcoding paths throughout the codebase.

DATA_FILES = {

    None: "", # Default key for no file path

    # Densities section
    # =================

    # Densities
    'densities': os.path.join('densities', 'data', 'densities.dat'),

    # Fission section
    # ===============

    # Fission Barriers
    'fission_barriers_empirical': os.path.join('fission', 'data', 'empirical-barriers.dat'),
    'fission_barriers_hfb': os.path.join('fission', 'data', 'empirical-hfb-barriers.dat'),

    # Gamma section
    # =============

    # Gamma-ray strength functions
    'gsf_data': os.path.join('gamma', 'data', 'gsf', 'gsf_Z{Z:03d}A{A:03d}.dat'),
    'gdr_parameters_exp': os.path.join('gamma', 'data', 'ripl3-gdr-parameters&errors-exp-SLO.dat'),
    'gdr_parameters_theor': os.path.join('gamma', 'data', 'ripl3_gdr-parameters-theor.dat'),

    # Levels section
    # ==============

    # Levels
    'levels_param': os.path.join('levels', 'data', 'levels-param.data'),
    'discrete_levels': os.path.join('levels', 'data', 'discrete', 'z{Z:03d}.dat'),

    # Masses section
    # ==============

    # Mass models
    'mass_ame20': os.path.join('masses', 'mass-ame20.dat'),
    'mass_bskg3': os.path.join('masses', 'mass-bskg3.dat'),
    'mass_d1m': os.path.join('masses', 'mass-d1m.dat'),
    'mass_frdm12': os.path.join('masses', 'mass-frdm12.dat'),
    'mass_frdm95': os.path.join('masses', 'mass-frdm95.dat'),
    'mass_hfb14': os.path.join('masses', 'mass-hfb14.dat'),
    'mass_hfb27': os.path.join('masses', 'mass-hfb27.dat'),
    'mass_ws4': os.path.join('masses', 'mass-ws4.dat'),
    
    # Deformations
    'deformations_gs_exp': os.path.join('masses', 'gs-deformations-exp.dat'),

    # Abundances
    'abundances': os.path.join('masses', 'abundance.dat'),

    # Optical Model section
    # =====================

    # Optical Model Parameters
    'om_deformations': os.path.join('optical', 'data', 'om-deformations.dat'),
    'om_parameter_u': os.path.join('optical', 'data', 'om-parameter-u.dat'),

    # Resonances section
    # ==================

    # Resonances
    'resonances0': os.path.join('resonances', 'data', 'resonances0.dat'),
    'resonances1': os.path.join('resonances', 'data', 'resonances1.dat'),
}

def get_data_file_path(key: str, **kwargs) -> str:
    """Constructs the full path to a data file.

    Arguments:
        key (str): The key corresponding to the data file in the DATA_FILES dict.
        **kwargs: Formatting arguments for paths that require them (e.g., Z and A).

    Returns:
        str: The absolute path to the data file.
    """
    if key not in DATA_FILES:
        raise KeyError(f"Data file key '{key}' not found in configuration.")
    
    relative_path = DATA_FILES[key]
    
    # Format the path if needed
    if '{' in relative_path:
        relative_path = relative_path.format(**kwargs)
        
    if not RIPL_PATH:
        # Return relative path if RIPL_PATH is not set, which might still work
        # if the application is run from a suitable directory.
        return relative_path

    return os.path.join(RIPL_PATH, relative_path)

