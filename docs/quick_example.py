import numpy as np
from gravityp import make_geodesics_plot

def g_rr(r: float, dummy) -> float:
    """Radial function g^{rr} of the Schwarzschild metric in units of M=1"""
    return 1 - 2./r

def g_thth(r: float, dummy) -> float:
    """Areal radius squared g^{theta theta} of the Schwarzschild in units of M=1"""
    return r**2

# Dictionary codifying Schwarzschild metric and required params
Schwarzschid_kwargs = {
    'r_phs': [3.,],         # Photon sphere at r=3M
    'inner_edge': 2.,       # Inner edge of disk at horizon r=2M
    'radial_fun': g_rr,     # Above defined radial function
    'radial_params': None,  # g_rr has no additional params
    'areal': g_thth,        # Above defined areal radius squared
    'areal_params': None,   # g_thth has no additional params
}

# Array of impact parameters from 0M to 10M
impact_parameters = np.arange(0,10,0.2)
make_geodesics_plot(impact_parameters, figsize=(4,4), **Schwarzschid_kwargs)