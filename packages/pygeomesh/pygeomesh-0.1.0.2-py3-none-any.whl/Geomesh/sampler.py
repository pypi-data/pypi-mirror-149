import numpy as np
import scipy.stats as stats


def Sampler(ndim, n, l_bounds, u_bounds, samplingtype=None):
    if samplingtype is None:
        samplingtype = 'uniform'
    if samplingtype == 'uniform':
        return np.random.uniform(l_bounds, u_bounds, (n, ndim))
    elif samplingtype == 'grid':
        return np.linspace(l_bounds, u_bounds, n)
    elif samplingtype == 'normal':
        return stats.norm.rvs(size=(ndim, n))
    elif samplingtype == 'random':
        return np.random.random(size=(ndim,
                                      n)) * (u_bounds - l_bounds) + l_bounds
    elif samplingtype == 'arange':
        return np.arange(l_bounds, u_bounds, n)
