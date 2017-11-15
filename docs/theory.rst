============
Theory
============

.. module:: pycorrelate.pycorrelate

Cross-correlation of point processes
====================================

In fluorescence correlation spectroscopy (FCS) the
cross-correlation function (CCF)
of two continuous signals :math:`I_1(t)` and
:math:`I_2(t)` is defined as:

.. math::
    G(\tau) = \frac{\langle I_1(t)\; I_2(t) \rangle}
                   {\langle I_1(t)\rangle\langle I_2(t) \rangle}

The auto-correlation function (ACF) is just a special case where
:math:`I_1(t) = I_2(t)`.

In actual experiments, signals are not continuous but come from
single-photon detectors that produce a pulse for each photon. These pulses
are usually timestamped with ~10ns resolution and the series of photon
arrival times is used as input for ACF or CCF computation.

In principle timestamps can be binned as produce a discrete-time signal.
In signal processing, the (non-normalized) cross-correlation of two
real discrete-time signals :math:`\{A_i\}` and
:math:`\{B_i\}` is defined as

.. math::
    c[k] = \sum_{i=-\infty}^{\infty} A[i]\ B[i+k].

The previous formula is implemented by :func:`ucorrelate` and
`numpy.correlate <https://docs.scipy.org/doc/numpy/reference/generated/numpy.correlate.html#numpy.correlate>`__.

Binning timestamps to obtain timetraces would be very inefficient for FCS
analysis where time-lags spanning may orders of magnitude need to be computed.
It is more efficient to directly compute the cross-correlation function from
timestamps.
The popular multi-tau algorithm allows computing the correlation directly
from timestamps on a fixed arrangement of quasi-log-spaced bins.
More generally, Laurence algorithm
`Laurence et al. Optics Letters (2006) <https://doi.org/10.1364/OL.31.000829>`__
allows computing cross-correlation from timestamps on arbitrary lag-bins,
with similar performances as the multi-tau.
Computing cross-correlation :math:`C(\tau)` from timestamps is fundamentally
a counting tasks. Given two timestamps arrays *t* and *u* and
considering the k-th time-lag bin :math:`[\tau_k, \tau_{k+1})`,
:math:`C(k)` is the number of pairs where:

.. math::
    \tau_k \le t_i - u_j < \tau_{k+1}

for all the possible *i* and *j* combinations.

.. math::
    C(k) = n(\{(i,j) \ni t_i < u_i - \tau_k\})

where `n({})` is the operator counting the elements in a set,
:math:`\tau_k` is the duration of the k-th time lag and *T*
is the measurement duration.
Normally we want the normalized expression, that is:

.. math::
    G(k) = \frac{n(\{(i,j) \ni t_i < u_i - \Delta\tau_k\})(T-\Delta\tau_k)}
                {n(\{i \ni t_i \le T - \Delta\tau_k\})n(\{j \ni u_j \ge \Delta\tau_k\})}

The last two equations are implemented by :func:`pcorrelate`,
where the argument `normalized` allows choosing between the normalized
and unnormalized version.
