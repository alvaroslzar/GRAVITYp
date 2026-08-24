"""This module contains the implementation of the simulation of the optical
appearance of a compact object and observed intensity profile.
"""

import numpy as np

from .utils import to_tuple
from .transfer_functions import transfer_function


__all__ = ["redshift", "observed_intensity", "total_intensity", "compute_points"]


def redshift(r, radial_fun, radial_params):
    """Gravitational redshift"""
    return np.sqrt(radial_fun(r, *to_tuple(radial_params)))

def observed_intensity(eval_points, bs, rbs, emission_model, kwargs):
    radial_fun = kwargs['radial_fun']
    radial_params = kwargs['radial_params']
    intensity = emission_model(rbs)*redshift(rbs, radial_fun, radial_params)**4
    return np.interp(eval_points, bs, intensity, left=0, right=0)

def total_intensity(bs, bs_transfer_list, emission_model, kwargs, correction=0):
    intensity = np.zeros(shape=bs.shape) # Important to use bs.shape instead of len(bs)

    for order, bb in enumerate(bs_transfer_list):
        points = transfer_function(bb, order, correction, **kwargs)
        intensity += observed_intensity(bs, *points, emission_model, kwargs)

    return intensity

def compute_points(bs_transfer_list, emission_model, kwargs, Npixels):
    x = np.linspace(-10, 10, np.sqrt(Npixels).astype(int) )
    y = np.linspace(-10, 10, np.sqrt(Npixels).astype(int) )
    X,Y = np.meshgrid(x, y)
    B = np.sqrt(X**2 + Y**2)
    return total_intensity(B, bs_transfer_list, emission_model, kwargs)