
# TODO 01: Separate into modules
# TODO 02: Translate Spanish comments to English
# TODO 03: Clean up commented code
# TODO 04: Decide docstring format for consistency
# TODO 05: Decide if all functions are part of the public API
# TODO 06: Add docstrings to API functions
# TODO 07: Check for in-function TODOs
# TODO 08: Think about adding in __name__=='__main__'

#############################################
#               GLOBAL IMPORTS              #
#############################################

import numpy as np
import scipy.optimize as optimize


# #############################################
# #              GLOBAL CONSTANTS             #
# #############################################

# DEFAULT_NPOINTS = 100000  # ODE integration resolution
# DEFAULT_R0 = 1000.0  # Asymptotic boundary for initial conditions
# MINIMUM_R = 1e-6 # Minimum value of r for integration


# #############################################
# #            GEODESIC INTEGRATION           #
# #############################################

# import scipy.integrate as integrate
# from bisect import bisect_right


# def to_tuple(var) -> tuple:
#     if var.__class__ != tuple:
#         return (var,)
#     else:
#         return var
    
# def to_list(var) -> list:
#     if var.__class__ != list:
#         return [var]
#     else:
#         return var

# def potential(r, radial_fun, radial_params, areal, areal_params):
#     """ 
#     Effective potential of a spherically symmetric metric of the form:

#     ds^2 = - radial_fun(r; radial_params)dt^2 + 1/radial_fun(r; radial_params)dr^2 + areal(r; areal_params)dOmega^2

#     Parameters:
#         r (float): radial coordinate of the metric
#         radial_fun (callable): -gtt metric function. Its first argument must be r
#         radial_params (float | tuple): additional parameters for radial_fun
#         areal (callable): areal radius squared.  Its first argument must be r
#         areal_params (float | tuple): additional parameters for areal
#     """
#     return radial_fun(r,*to_tuple(radial_params)) / areal(r,*to_tuple(areal_params))
    
# def get_increasing_maxima(r_phs, potential):
#     """Returns increasing local maxima of the potential with their photon sphere values"""
#     if len(r_phs) >= 1: # There has to be at least 1 local maximum
#         r_phs = np.array(r_phs)
#         r_phs = np.sort(r_phs)[::-1] # descending order of 
#         photon_sph = r_phs[0].reshape(1,)
#         local_maxima = potential(photon_sph)
#         for r_ph in r_phs:
#             maximum = potential(r_ph)
#             if maximum > local_maxima.max(): # We take increasing local maxima
#                 local_maxima = np.append(local_maxima, maximum)
#                 photon_sph = np.append(photon_sph, r_ph)
#         return photon_sph[::-1], local_maxima[::-1] # Swap to ascending order of photon_spheres
#     else:
#         return np.array([]), np.array([])

# def find_interval(inverse_b2, photon_sph, local_maxima, lower_bound=1e-4, upper_bound=100):
#     """Returns the bounds (r1,r2) where the rmin is found for a given 1/b^2"""
#     # NOTE: photon_sph and local_maxima have to be ordered by get_increasing_maxima
#     if len(photon_sph)==0 and len(local_maxima)==0: # Case 1: there is no local maximum
#         return (lower_bound, upper_bound)
#     if inverse_b2 >= local_maxima[0]: # Case 2: 1/b^2 higher than all local maxima
#         return (lower_bound, photon_sph[0])
#     if inverse_b2 <= local_maxima[-1]: # Case 3: 1/b^2 lower than all local maxima
#         return (photon_sph[-1], upper_bound)

#     # Case 4: there are more than 1 local maximum and 1/b^2 lies between two of them
#     # We negate both the array elements and 1/b^2 so the logic mirrors an increasing array
#     idx = bisect_right(local_maxima, -inverse_b2, key=lambda x: -x)
#     return (photon_sph[idx - 1], photon_sph[idx])

# def find_rmin(b, r_phs, inner_edge, radial_fun, radial_params, areal, areal_params):
#     """
#     Finds the minimum radius of the trajectory using Brent's method. 

#     Parameters:
#         b (float): impact parameter of the photon trajectory
#         r_phs (array): array with the position of photon spheres (maxima) of the potential
#         inner_edge (float): value of the r coordinate of the inner edge (event horizon, throat, etc.)
#         potential (callable): effective potential

#     Returns:
#         i)  If b > bmin, then rmin is found by solving V(r)-1/b^2 = 0
#         ii) If b < bmin, then rmin = inner_edge.
#     """
#     pot = lambda r: potential(r, radial_fun, radial_params, areal, areal_params) # V(r)
#     photon_sph, local_maxima = get_increasing_maxima(r_phs, pot)
#     bounds = find_interval(1/b**2, photon_sph, local_maxima) # Interval for Brent's method
#     fun = lambda r: pot(r)-1/b**2
#     if fun(bounds[0])*fun(bounds[1]) >= 0: # No root if there is no sign change
#         root = 0
#     else:
#         root, results = optimize.brentq(fun, *bounds, full_output=True)
#     return max( max(root, inner_edge) , MINIMUM_R )

# def geodesic_in(phi, r, b, radial_fun, radial_params, areal, areal_params):
#     """Expression for dphi/dr in the incoming null geodesic equation"""
#     areal_params = to_tuple(areal_params)
#     radial_params = to_tuple(radial_params)
#     return -( b / np.sqrt(areal(r,*areal_params)) )/np.sqrt( areal(r,*areal_params) - b**2*radial_fun(r,*radial_params) )

# def geodesic_out(phi, r, b, radial_fun, radial_params, areal, areal_params):
#     """Expression for dphi/dr in the outgoing null geodesic equation"""
#     areal_params = to_tuple(areal_params)
#     radial_params = to_tuple(radial_params)
#     return +( b / np.sqrt(areal(r,*areal_params)) )/np.sqrt( areal(r,*areal_params) - b**2*radial_fun(r,*radial_params) )

# def compute_outgoing(r_phs, inner_edge, rmin) -> bool:
#     """Returns a boolean that tells whether to compute outgoing geodesic after reaching rmin"""
#     # TODO: Organizar esto para que sea más claro, que hasta ahora era prueba y error
#     compute = False
#     if (len(r_phs)>0): # There is at least 1 photon sphere
#         innermost_photon_sphere = np.array(r_phs).min()
#         if (innermost_photon_sphere < MINIMUM_R):
#             if (rmin > MINIMUM_R):
#                 compute = True
#         # if (rmin > inner_edge) and (innermost_photon_sphere > 0): # Probamos con inner_edge mejor
#         else:
#             # print('Hola')
#             if (rmin > inner_edge) and (rmin > MINIMUM_R): # Probamos con inner_edge mejor
#                 compute = True
#     else: # There is no photon sphere
#         compute = True
#     return compute

# def compute_geodesic(b, r_phs, inner_edge, radial_fun, radial_params, areal, areal_params,
#                      Npoints=DEFAULT_NPOINTS, r0=DEFAULT_R0):
#     """
#     Computes the null geodesic trajectory in Schwarzschild spacetime.
    
#     Integrates the geodesic equations to trace light ray paths. For incoming rays,
#     integrates from r0 down to rmin. For rays escaping to infinity (rmin > 3),
#     also integrates the outgoing trajectory from rmin back to r0.

#     Parameters:
#         b (float): Impact parameter in units of M=1
#         Npoints (int): Number of radial points for integration. Default: DEFAULT_NPOINTS
#         r0 (float): Starting radius. Default: DEFAULT_R0
    
#     Returns:
#         tuple[np.ndarray, np.ndarray]: (rr, phi) where rr is the radial coordinate 
#             array and phi is the azimuthal angle array along the geodesic
#     """ 
#     rmin = find_rmin(b, r_phs, inner_edge, radial_fun, radial_params, areal, areal_params)
#     rr = np.geomspace(r0, rmin, Npoints) # We must ensure rmin > 0 in find_rmin for np.geomspace

#     phi0 = b/rr[0] # good approximation for r0>>rSch and better than phi0=0
#     phi = integrate.odeint(
#         geodesic_in, phi0, rr, (b,radial_fun,radial_params,areal,areal_params)
#     ).reshape(-1,)
#     phi = phi[~np.isnan(phi)]
#     rr = rr[:len(phi)]

#     # NOTE: does not work properly with high r0 and low Npoints for outgoing geodesics
#     # FIXME: si len(r_phs)=0, solo integra incoming.
#     if compute_outgoing(r_phs, inner_edge, rmin):
#         rout = rr[::-1]
#         phi0 = 2*phi[-1]-phi[-2] # Linear approx. for next angle. Required for strict monotonicity!!
#         phi_out = integrate.odeint(
#             geodesic_out, phi0, rout, (b,radial_fun,radial_params,areal,areal_params)
#         ).reshape(-1,)
#         rr = np.concatenate([rr,rout])
#         phi = np.concatenate([phi,phi_out])

#     return (rr,phi)

#############################################
#                RAY TRACING                #
#############################################

from .geodesic_integration import compute_geodesic

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


#############################################
#                   RINGS                   #
#############################################

def find_ring_edge(fun, lower_bound, upper_bound, to_upper=True) -> float:
    """Returns the impact parameter value for which the number of turns is 0.75 or 1.25 (depending on fun)"""
    b = (upper_bound+lower_bound)/2.
    if not to_upper: # Bounds are reversed
        upper_bound, lower_bound = lower_bound, upper_bound
    a = lower_bound
    
    maxiter = 500
    success, iter = False, 0
    for iter in range(maxiter):
        success = fun(a)*fun(b) < 0
        if success:
            break
        a = b
        b = (upper_bound+b)/2.
    if success:
        return optimize.brentq(fun, a, b, full_output=False)  # type: ignore[index]
    else:
        raise ValueError(f'Invalid interval for ring edges. Iterations: {iter}')
    
def find_ring_bs(b_crit, ring_interval, epsilon, scalar_fun_nturns):
    """Returns the interval of impact parameters where lensed and photon rings are found around a single b_crit"""
    # TODO: considerar el caso en el que los lensed/photon rings se solapan
    fun_lensed = lambda b: scalar_fun_nturns(b)-0.75
    fun_p_ring = lambda b: scalar_fun_nturns(b)-1.25

    # retro
    bounds = ( ring_interval[0] , b_crit-epsilon )
    retro_lensed = find_ring_edge(fun_lensed, *bounds, to_upper=True)
    retro_p_ring = find_ring_edge(fun_p_ring, *bounds, to_upper=True)

    # non-retro
    bounds = ( b_crit+epsilon , ring_interval[1] )
    lensed = find_ring_edge(fun_lensed, *bounds, to_upper=False)
    p_ring = find_ring_edge(fun_p_ring, *bounds, to_upper=False)
    
    return {
        'retro_lensed': (retro_lensed,retro_p_ring), 
        'retro_p_ring': (retro_p_ring,b_crit),
        'p_ring': (b_crit,p_ring),
        'lensed': (p_ring,lensed) 
    }

def is_sorted(l):
    # Source - https://stackoverflow.com/a/3755251
    l = list(l)
    return all(l[i] <= l[i+1] for i in range(len(l) - 1))

def get_minima(b_crits, epsilon, scalar_fun_nturns):
    """Returns the local minima of the nturns function between a list of critical impact parameters"""
    if not is_sorted(b_crits):
        raise ValueError(f'List of b_crits is not sorted: {b_crits}')
    minima = []
    for i, b_crit in enumerate(b_crits[:-1]):
        bounds = ( b_crits[i]+epsilon , b_crits[i+1]-epsilon )
        result = optimize.minimize_scalar(scalar_fun_nturns, bounds=bounds)
        if result.success:  # type: ignore[index]
            minima.append(result.x)  # type: ignore[index]
        
    return minima

def find_rings_list(b_crits, kwargs):
    """Returns a list with all impact parameter intervals for each ring and for each b_crit"""
    epsilon = 1e-11 # Maybe toooo small
    max_value = max(b_crits) + 5
    scalar_fun_nturns = lambda b: compute_nturns_scalar(b, **kwargs)

    b_crits.sort() # We ensure that they are in increasing order
    minima = get_minima(b_crits, epsilon, scalar_fun_nturns)
    rings = []
    for i, b_crit in enumerate(b_crits):
        a = epsilon if i==0 else minima[i-1]
        b = max_value if i==len(b_crits)-1 else minima[i]
        rings.append( find_ring_bs(b_crit, (a,b), epsilon, scalar_fun_nturns) )
    return rings

def compute_optimal_array_steps(bmin, bmax, rings,
                                steps=(0.1,0.01,0.001), joint=True, fill=False):
    """
    Sample points with specified steps. 
    If joint=True (default), direct, lensed and photon ring contributions are
    returned in an ordered single array.
    If joint=False, these three contributions are returned as a triplet:
    ( bs_direct, bs_lensed, bs_p_ring )
    """
    # TODO: hacer docstring más explicativo (fill está sin explicar)
    bs_direct = []
    bs_lensed = []
    bs_p_ring = []

    if not fill:
        for i, ring in enumerate(rings):
            # array of impact parameters for the direct image
            start = bmin if i==0 else rings[i-1]["lensed"][1]
            stop = ring["retro_lensed"][0]
            bs_direct.append( np.arange(start, stop, steps[0])  )

            # array of impact parameters for the lensed image
            bs_lensed.append(
                np.concatenate([
                    np.arange(ring["retro_lensed"][0],ring["retro_lensed"][1],steps[1]) , 
                    np.arange(ring["lensed"][0],ring["lensed"][1],steps[1])
                ]).reshape(-1,)
            )

            # array of impact parameters for the ring image
            bs_p_ring.append(
                np.concatenate([
                    np.arange(ring["retro_p_ring"][0],ring["retro_p_ring"][1],steps[2]) , 
                    np.arange(ring["p_ring"][0],ring["p_ring"][1],steps[2])
                ]).reshape(-1,)
            )

        # right tail of array for the direct image    
        bs_direct.append( np.arange(rings[-1]["lensed"][1], bmax, steps[0])  )
    else:
        bs_direct.append( np.arange(bmin, bmax, steps[0]) )
        for i, ring in enumerate(rings):
            # array of impact parameters for the lensed image
            bs_lensed.append(
                np.arange(ring["retro_lensed"][0],ring["lensed"][1],steps[1])
            )

            # array of impact parameters for the ring image
            bs_p_ring.append(
                np.arange(ring["retro_p_ring"][0],ring["p_ring"][1],steps[2])
            )

    bs_direct = np.concat(bs_direct)
    bs_lensed = np.concat(bs_lensed)
    bs_p_ring = np.concat(bs_p_ring)

    if joint:
        total = np.sort( np.concatenate([bs_direct, bs_lensed, bs_p_ring]) )
        return total[(total>=bmin) & (total<=bmax)]
    else:
        return [bs_direct, bs_lensed, bs_p_ring]

def compute_optimal_array_Npoints(bmin, bmax, rings,
                                  Npoints=100, joint=True, fill=False):
    """
    Sample points with specified number of points. 
    If joint=True (default), direct, lensed and photon ring contributions are
    returned in an ordered single array.
    If joint=False, these three contributions are returned as a triplet:
    ( bs_direct, bs_lensed, bs_p_ring )
    """
    # TODO: hacer docstring más explicativo (fill está sin explicar)
    bs_direct = []
    bs_lensed = []
    bs_p_ring = []

    if not fill:
        for i, ring in enumerate(rings):
            # array of impact parameters for the direct image
            start = bmin if i==0 else rings[i-1]["lensed"][1]
            stop = ring["retro_lensed"][0]
            bs_direct.append( np.linspace(start, stop, Npoints)  )

            # array of impact parameters for the lensed image
            bs_lensed.append(
                np.concatenate([
                    np.linspace(ring["retro_lensed"][0],ring["retro_lensed"][1],Npoints) , 
                    np.linspace(ring["lensed"][0],ring["lensed"][1],Npoints)
                ]).reshape(-1,)
            )

            # array of impact parameters for the ring image
            bs_p_ring.append(
                np.concatenate([
                    np.linspace(ring["retro_p_ring"][0],ring["retro_p_ring"][1],Npoints) , 
                    np.linspace(ring["p_ring"][0],ring["p_ring"][1],Npoints)
                ]).reshape(-1,)
            )

        # right tail of array for the direct image    
        bs_direct.append( np.linspace(rings[-1]["lensed"][1], bmax, Npoints)  )
    else:
        bs_direct.append( np.linspace(bmin, bmax, Npoints) )
        for i, ring in enumerate(rings):
            # array of impact parameters for the lensed image
            bs_lensed.append(
                np.linspace(ring["retro_lensed"][0],ring["lensed"][1],Npoints)
            )

            # array of impact parameters for the ring image
            bs_p_ring.append(
                np.linspace(ring["retro_p_ring"][0],ring["p_ring"][1],Npoints)
            )

    bs_direct = np.concat(bs_direct)
    bs_lensed = np.concat(bs_lensed)
    bs_p_ring = np.concat(bs_p_ring)

    if joint:
        total = np.sort( np.concatenate([bs_direct, bs_lensed, bs_p_ring]) )
        return total[(total>=bmin) & (total<=bmax)]
    else:
        return [bs_direct, bs_lensed, bs_p_ring]
    

#############################################
#             TRANSFER FUNCTIONS            #
#############################################

from scipy.interpolate import CubicSpline

def transfer_function(bb, order, correction: float=0, **kwargs):
    bs = []
    rbs = []

    for b in np.atleast_1d(bb):
        (rr,phi) = compute_geodesic(b, **kwargs)
        
        if abs(phi[-1]) > ( order*np.pi + np.pi/2 + correction ):
            f_hat = CubicSpline(phi,rr)
            r_b = f_hat(order*np.pi+np.pi/2+correction)
            rbs.append(r_b)
            bs.append(b)

    return ( np.array(bs), np.array(rbs) )

def compute_inner_shadow(bmin, bmax, Npoints=10, **kwargs):
    """Computes the minimum value of the impact parameter for which a light ray intersects the accretion disk"""
    maxiters = 500
    for i in range(maxiters):
        bs = np.linspace(bmin,bmax,Npoints)
        (b, _) = transfer_function(bs, order=0, **kwargs)
        inner_shadow = b[0]
        diff = abs(b[1]-b[0])
        if 2*diff < 1e-5:
            break
        bmin = inner_shadow-diff
        bmax = inner_shadow+diff
    if 2*diff < 1e-5:
        return inner_shadow
    else:
        raise ValueError(f'Inner shadow has not been found after {maxiters} iterations.')
    

#############################################
#              EMISSION MODELS              #
#############################################

def intensity_at_ISCO(r, r_ISCO):
    func = lambda x: (1./(x-(r_ISCO-1))**2) / (1./(r_ISCO-(r_ISCO-1))**2)
    return np.piecewise(r, [r>=r_ISCO,r<r_ISCO] , [func,0] )

def intensity_at_photon_ring(r, r_ph):
    func = lambda x: (1./(x-(r_ph-1))**3) / (1./(r_ph-(r_ph-1))**3)
    return np.piecewise(r, [r>=r_ph,r<r_ph] , [func,0] )

def intensity_at_inner_edge(r, inner_edge):
    func = lambda x: ( np.pi/2-np.arctan(x-5) ) / ( np.pi/2-np.arctan(inner_edge-5) )
    return np.piecewise(r, [r>=inner_edge,r<inner_edge] , [func,0] )

def standard_Unbound(r, mu: float=8., sigma: float=2., gamma: float=2.):
    return ( np.exp(-0.5*(gamma+np.arcsinh((r-mu)/sigma))**2) / 
            np.sqrt((r-mu)**2+sigma**2) )

def normalized_Standard_Unbound(r, mu: float=8., sigma: float=2., gamma: float=2.):
    # FIXME: for some values of params, it doesn't find the minimum
    neg_fun = lambda r: -standard_Unbound(r, mu, sigma, gamma)
    minimum = optimize.minimize(neg_fun, 0).fun
    return neg_fun(r)/minimum

def exponential(r):
    return np.exp(-r)

def uniform(r):
    return np.ones(shape=r.shape)

#############################################
#                  SHADOWS                  #
#############################################

from .utils import to_tuple

def redshift(r, radial_fun, radial_params):
    """Gravitational redshift"""
    return np.sqrt(radial_fun(r, *to_tuple(radial_params)))

def observed_intensity(eval_points, bs, rbs, emission_model, kwargs):
    radial_fun = kwargs['radial_fun']
    radial_params = kwargs['radial_params']
    intensity = emission_model(rbs)*redshift(rbs, radial_fun, radial_params)**4
    return np.interp(eval_points, bs, intensity, left=0, right=0)

def total_intensity(bs, bs_transfer_list, emission_model, kwargs, correction=0):
    # impact_param_list = [
    #     np.linspace(0, np.sqrt(2)*10, 100), # direct
    #     np.linspace(rings['retro_lensed'][0], rings['lensed'][1], 100), # lensed
    #     np.linspace(rings['retro_p_ring'][0], rings['p_ring'][1], 100) # photon ring
    # ]
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


#############################################
#                   PLOTS                   #
#############################################

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable

from .utils import to_list

def plot_metric_function(ax, r_range, fun, param, name):
    ax.plot(r_range, fun(r_range,param), label=f'{name}={param:.2f}')

def make_metric_function_plot(fun, params, r_range, figsize=(9,6), savepath=None):
    ax = plt.figure(figsize=figsize).add_subplot()
    ax.set_title(f'{fun.__name__[2:].capitalize()} metric function')

    for name, param_list in params.items():
        for param in param_list:
            plot_metric_function(ax, r_range, fun, param, name)

    ax.set_xlim(r_range[0], r_range[-1])
    ax.set_ylim(-1,1)
    ax.set_xlabel(r'$r/M$')
    ax.set_ylabel(r'$e^{2\nu}$')
    xticks = np.arange(r_range[0],r_range[-1]+1,2,dtype=int)
    yticks = np.arange(-1,1.5,0.5)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xticklabels(xticks)
    ax.set_yticklabels(yticks)
    ax.hlines(0, r_range[0], r_range[-1],color='black',linewidth=1)
    ax.legend()
    if savepath is not None:
        plt.savefig(savepath)
    plt.show()

def plot_half_graph(ax, bs, plot_label=False, **kwargs):
    """Auxiliary function for plot_nturns"""
    nturns = compute_nturns(bs, **kwargs)
    upper = 1.25
    lower = 0.75
    
    lines_data = {
        'Direct': (np.ma.masked_where(nturns >= lower, nturns), 'black'),
        'Lensed': (np.ma.masked_where((nturns < lower) | (nturns >= upper), nturns), 'orange'),
        'Photon ring': (np.ma.masked_where(nturns < upper, nturns), 'red')
    }

    for label, (y_data, color) in lines_data.items():
        plot_kwargs = {'color': color}
        if plot_label:
            plot_kwargs['label'] = label
        ax.plot(bs, y_data, **plot_kwargs)

def plot_nturns(bs, b_crits, figsize=(7,7), savepath=None, **kwargs):
    ax = plt.figure(figsize=figsize).add_subplot()
    xticks = [i for i in range(0,11,2)]
    xtick_labels = [f'{tick}' for tick in xticks]

    if len(b_crits)==0:
        plot_half_graph(ax, bs, plot_label=True, **kwargs)
    else:
        # Interval from 0 to first b_crit, plotting labels
        bs_interval = bs[ bs <= b_crits[0]]
        plot_half_graph(ax, bs_interval, plot_label=True, **kwargs)
        ax.vlines(b_crits[0],0,2,colors='gray',linestyles='dashed',zorder=0)
        xticks += [b_crits[0]]
        if len(b_crits)==1:
            xtick_labels += [rf'$b_c$']
        else:
            xtick_labels += [rf'$b_c^1$']

        # Intermediate intervals [b1,b2], [b2,b3], ...
        if len(b_crits) > 1:
            for i, b_crit in enumerate(b_crits[1:], start=1):
                bs_interval = bs[ (bs >= b_crits[i-1]) & (bs < b_crit) ]
                plot_half_graph(ax, bs_interval, plot_label=False, **kwargs)
                ax.vlines(b_crit,0,2,colors='gray',linestyles='dashed',zorder=0)
                xticks += [b_crit]
                xtick_labels += [rf'$b_c^{i+1}$']

        # Last interval from last b_crit to infinity
        bs_interval = bs[ bs >= b_crits[-1] ]
        plot_half_graph(ax, bs_interval, plot_label=False, **kwargs)

    ax.set_xlim(0,10)
    ax.set_ylim(0,2)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtick_labels)
    ax.set_yticks(np.arange(0,2.1,0.25))
    ax.set_xlabel(r'$b/M$')
    ax.set_ylabel(r'$n=\phi /(2\pi)$')
    ax.legend(loc='upper right')
    if savepath is not None:
        plt.savefig(savepath)
    plt.show()

def plot_geodesic(axes, areal, areal_params, rr, phi, color=None):
    # NOTE: the plotted coordinate refers to the areal radius
    if color is None:
        order = get_order(phi[-1])
        color = ['dodgerblue','orange','red'][order]

    areal_radius = np.sqrt( areal(rr,*to_tuple(areal_params)) )
    trajectory = (areal_radius*np.cos(phi), areal_radius*np.sin(phi))
    axes.plot(*trajectory, color=color, linewidth=0.5, alpha=1)

def plot_BH(axes, r_phs, inner_edge, areal, areal_params):
    # NOTE: Within this function, the variable r refers to the areal radius
    i_edge_kwargs = {'color':'black', 'fill':(inner_edge!=0)}
    p_ring_kwargs = {'color':'black', 'fill':False}

    r_i_edge = np.sqrt( areal(inner_edge, *to_tuple(areal_params)) )
    patch_i_edge = Circle((0, 0), r_i_edge, **i_edge_kwargs, zorder=3)
    axes.add_patch(patch_i_edge)
    for r_ph in r_phs:
        r_photon = np.sqrt( areal(r_ph, *to_tuple(areal_params)) )
        photon_ring = Circle((0, 0), r_photon, linestyle=(0,(5,2)), linewidth=2/3, zorder=3, **p_ring_kwargs)
        axes.add_patch(photon_ring)

def make_geodesics_plot(bs_dict, r_phs, inner_edge, radial_fun, radial_params, areal, areal_params,
                        figsize=(7,7), savepath=None):
    ax = plt.figure(figsize=figsize).add_subplot()

    if bs_dict.__class__ != dict:
        bs_dict = {'label': (None, bs_dict)} # Cast to dict
    for label, (color, bs) in bs_dict.items():
        for b in np.atleast_1d(bs):
            coords = compute_geodesic(
                b, r_phs, inner_edge, radial_fun, radial_params, areal, areal_params
            )
            plot_geodesic(ax, areal, areal_params, *coords, color)
        
    plot_BH(ax, r_phs, inner_edge, areal, areal_params)

    ax.set_xlim(-10,10)
    ax.set_ylim(-10,10)
    ax.set_xticks(np.arange(-10,11,5))
    ax.set_yticks(np.arange(-10,11,5))
    # ax.set_xlabel(r'$\mathrm{e}^{\xi}\cos\varphi$')
    # ax.set_ylabel(r'$\mathrm{e}^{\xi}\sin\varphi$')
    ax2 = ax.twinx() 
    ax2.set_ylim(-10, 10)                 # Keep limits synced with ax
    ax2.set_yticks(np.arange(0, 11, 2))   # Ticks: 0, 1, 2, ..., 10
    
    if savepath is not None:
        plt.savefig(savepath)
    plt.show()

def plot_transfer_function(axes, bs, order, correction: float=0, **kwargs):
    # NOTE: bs in bs_list can also be lists for lensed and photon ring, which will be plotted separately
    colors = ['dodgerblue','orange','red']
    image = ['Direct','Lensed','Photon ring']
    points = transfer_function(bs, order, correction, **kwargs)
    # axes.plot(*points, color=colors[order], label=f'{image[order]} image. Correction = {correction:.2f}')
    axes.plot(*points, color=colors[order], label=f'{image[order]}', linewidth=1)

def make_transfer_function_plot(b_crits, kwargs, bs_list,
                                correction=0, figsize=(7,7), savepath=None):
    fig, ax = plt.subplots(figsize=figsize)

    for order, bs in enumerate(bs_list):
        if order==0:
            plot_transfer_function(ax, bs, order, correction, **kwargs)
        else:
            for bs_ring in to_list(bs):
                plot_transfer_function(ax, bs_ring, order, correction, **kwargs)
            

    xticks = [i for i in range(0,11,2)]
    xticklabels = [f'{t}' for t in xticks]
    # xticks += [b_crit]
    # xticklabels += [r'$b_c$']

    ax.set_xlabel(r'$b/M$')
    ax.set_ylabel(r'$r_m/M$')
    ax.set_xlim(0,10)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels)
    ax.set_ylim(0,15)
    ax.set_yticks(np.arange(0,16,5))
    
    if savepath is not None:
        plt.savefig(savepath)
    plt.show()

## Intensity and shadows
def add_extra_tick(xticks, xticklabels, extra_tick=None, extra_ticklabel=None):
    if (extra_tick is not None) and (extra_ticklabel is not None):
        threshold = 0.6  # Minimum allowed distance between labels
        xticks = [t for t in xticks if abs(t - extra_tick) > threshold]
        xticklabels = [f'{t}' for t in xticks]
        xticks += [extra_tick]
        xticklabels += [extra_ticklabel]
    return xticks, xticklabels

def plot_emission_model(rs, emission_model, text_string=None,
                        tick=None, ticklabel=None, figsize=(7,7), savepath=None):
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(rs, emission_model(rs), label=r'$I_{\mathrm{em}}/I_0$')
    
    rmin = round(rs.min())
    rmax = round(rs.max())

    # Add an extra xtick placed at specified position
    xticks = [i for i in range(rmin,rmax,2)]
    xticklabels = [f'{t}' for t in xticks]
    xticks, xticklabels = add_extra_tick(xticks, xticklabels, tick, ticklabel)

    ax.set_xlabel(r'$r/M$')
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels)
    ax.set_xlim(rmin,rmax)
    # ax.set_ylabel(r'$I_\mathrm{em}/I_0$')
    ax.set_ylim(0,1)
    if text_string is not None:
        ax.text( 7.5, 0.8, s=text_string )
    ax.legend()
    if savepath is not None:
        plt.savefig(savepath)
    plt.show()

def plot_observed_intensity(bs, bs_transfer_list, emission_model, kwargs,
                            figsize=(7,7), savepath=None, y_range=None):
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(bs, total_intensity(bs, bs_transfer_list, emission_model, kwargs),
            label=r'$I_{\mathrm{ob}}/I_0$')
    
    bmin = round(bs.min())
    bmax = round(bs.max())
    ax.set_xlabel(r'$b/M$')
    ax.set_xticks(range(bmin,bmax+2,2))
    ax.set_xlim(bmin,bmax)
    ax.set_ylim(y_range)
    ax.legend()
    if savepath is not None:
        plt.savefig(savepath)
    plt.show()

def plot_intensities(ax, z, vmin=None, vmax=None):
    return ax.imshow(
        z,
        norm=colors.PowerNorm(1, vmin, vmax),
        cmap='inferno', 
        extent=(-10, 10, -10, 10), 
        origin='lower',
        interpolation='none',
        # vmin=vmin,
        # vmax=vmax
    )

def plot_colorbar(fig, ax, im):
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.15)
    cb = fig.colorbar(im, cax=cax)

def make_shadow_plot(bs_transfer_list, emission_model, kwargs,
                     figsize=(7,7), savepath=None, y_range=None, Npixels=1e6):
    
    Z = compute_points(bs_transfer_list, emission_model, kwargs, Npixels)

    fig, ax = plt.subplots(figsize=figsize)
    im = plot_intensities(ax, Z, *to_tuple(y_range))
    ax.set_xticks(np.arange(-10, 11, 5))
    ax.set_yticks(np.arange(-10, 11, 5))
    plot_colorbar(fig, ax, im)

    if savepath is not None:
        plt.savefig(savepath)
    plt.show()