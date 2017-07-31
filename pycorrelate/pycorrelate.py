"""
The following functions to compute linear correlation on discrete signals
or on point-processes (e.g. timestamps).
"""

import numpy as np
import numba


@numba.jit(nopython=True)
def pcorrelate(t, u, bins):
    """Compute correlation of two arrays of descrete events (point-process).

    The input arrays need to be values of a point process, such as
    photon arrival times or positions. The correlation is efficiently
    computed on an arbitrary array of bins that can span several orders
    of magnitudes without actual binning the inputs according to
    `(Laurence 2006) <https://doi.org/10.1364/OL.31.000829>`__.

    Arguments:
        t (array): first timestamp array to correlate
        u (array): second timestamp array to correlate
        bins (array): bin edges for lags.

    Returns:
        Array containing the correlation of `t` and `u`.
        The size is `len(bins) - 1`.
    """
    nbins = len(bins) - 1

    # Array of counts (histogram)
    Y = np.zeros(nbins, dtype=np.int64)

    # For each bins, imin is the index of first `u` >= of each left bin edge
    imin = np.zeros(nbins, dtype=np.int64)
    # For each bins, imax is the index of first `u` >= of each right bin edge
    imax = np.zeros(nbins, dtype=np.int64)

    # For each ti, perform binning of (u - ti) and accumulate counts in Y
    for ti in t:
        for k, (tau_min, tau_max) in enumerate(zip(bins[:-1], bins[1:])):
            #print ('\nbin %d' % k)

            if k == 0:
                j = imin[k]
                # We start by finding the index of the first `u` element
                # which is >= of the first bin edge `tau_min`
                while j < len(u):
                    if u[j] - ti >= tau_min:
                        break
                    j += 1

            imin[k] = j
            if imax[k] > j:
                j = imax[k]
            while j < len(u):
                if u[j] - ti >= tau_max:
                    break
                j += 1
            imax[k] = j
            # Now j is the index of the first `u` element >= of
            # the next bin left edge
        Y += imax - imin
    return Y / np.diff(bins)


@numba.jit
def ucorrelate(t, u, maxlags=None):
    """Compute correlation of two signals defined at uniformly-spaced points.

    The correlation is defined only for positive lags (including zero).
    The input arrays represent signals defined at uniformily-spaced
    points. This function is equivalent to `numpy.correlate`, but can
    efficiently compute correlations on a limited number of lags.

    Note that binning point-processes with uniform bins, provides
    signals that can be passed as argument to this function.

    Arguments:
        tx (array): first signal to be correlated
        ux (array): second signal to be correlated
        maxlags (int): number of lags wher correlation is computed.
            If None, computes all the lags where signals overlap
            `min(tx.size, tu.size) - 1`.

    Returns:
        Array contained the correlation at different lags.
        The size of this array is `maxlags` (if defined) or
        `min(tx.size, tu.size) - 1`.

    Example:

        Correlation of two signals `t` and `u`::

            >>> t = np.array([1, 2, 0, 0])
            >>> u = np.array([0, 1, 1])
            >>> pycorrelate.ucorrelate(t, u)
            array([2, 3, 0])

        The same result can be obtained with numpy swapping `t` and `u` and
        restricting the results only to positive lags::

            >>> np.correlate(u, t, mode='full')[t.size - 1:]
            array([2, 3, 0])
    """
    if maxlags is None:
        maxlags = u.size
    maxlags = int(min(u.size, maxlags))
    C = np.zeros(maxlags, dtype=np.int64)
    for lag in range(maxlags):
        tmax = min(u.size - lag, t.size)
        umax = min(u.size, t.size + lag)
        C[lag] = (t[:tmax] * u[lag:umax]).sum()
    return C


def make_lags(exp_min, exp_max, points_per_base, base=10):
    """Make a log-spaced array useful as time-lags bins.

    Arguments:
        exp_min (int): exponent of the minimum value
        exp_max (int): exponent of the maximum value
        points_per_base (int): number of points per base
            (i.e. in a decade when `base = 10`)
        base (int): base of the exponent. Default 10.

    Returns:
        Array of log-spaced values with specified range and spacing.

    Example:

        Compute log10-spaced bins with 2 bins per decade, starting
        from 10^-1 and stopping at 10^3::

            >>> make_bins(-1, 3, 2)
            array([  1.00000000e-01,   3.16227766e-01,   1.00000000e+00,
                     3.16227766e+00,   1.00000000e+01,   3.16227766e+01,
                     1.00000000e+02,   3.16227766e+02,   1.00000000e+03])
    """
    num_points = points_per_base * (exp_max - exp_min) + 1
    bins = np.logspace(exp_min, exp_max, num_points, base=base)
    return bins
