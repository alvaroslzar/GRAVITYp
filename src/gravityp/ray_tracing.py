"""This module contains functions for computing the number of intersections
(a.k.a. order) of a geodesic with the accretion disk.
"""

import numpy as np

from .geodesic_integration import compute_geodesic


__all__ = ["compute_nturns_scalar", "compute_nturns", "get_order"]


def compute_nturns_scalar(b, **kwargs):
    (_,phi) = compute_geodesic(b, **kwargs)
    return np.abs(phi[-1])/(2*np.pi)
                            
def compute_nturns(bs, **kwargs):
    return np.array([compute_nturns_scalar(b, **kwargs) for b in np.atleast_1d(bs)])

def get_order(deviation: float, correction: float=0) -> int:
    """
    Computes the number of turns nturn = deviation/(2*pi) and maps:
    - n < 3/4 -> 0 (direct image)
    - 3/4 < n < 5/4 -> 1 (lensed image)
    - n > 5/4 -> 2 (photon ring)
    """
    nturns = abs(deviation - correction)/(2*np.pi) # We take absolute value for rays with b<0
    return int(nturns > 0.75) + int(nturns > 1.25)


if __name__=="__main__":

    def g_rr(r: float, dummy) -> float:
        """Radial function g^{rr} of the Schwarzschild metric in units of M=1"""
        return 1 - 2./r

    def g_thth(r: float, dummy) -> float:
        """Areal radius squared g^{theta theta} of the Schwarzschild in units of M=1"""
        return r**2

    # Dictionary codifying Schwarzschild metric and required params
    Schwarzschild_kwargs = {
        'r_phs': [3.,],         # Photon sphere at r=3M
        'inner_edge': 2.,       # Inner edge of disk at horizon r=2M
        'radial_fun': g_rr,     # Above defined radial function
        'radial_params': None,  # g_rr has no additional params
        'areal': g_thth,        # Above defined areal radius squared
        'areal_params': None,   # g_thth has no additional params
    }

    nturns = compute_nturns_scalar(3, **Schwarzschild_kwargs)
    order = get_order(nturns)
    print(f"nturns = {nturns:.2f}. Order = {order}")