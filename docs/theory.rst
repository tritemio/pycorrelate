============
Theory
============

.. module:: pycorrelate.pycorrelate

Cross-correlation of point processes
====================================

In fluorescence correlation spectroscopy (FCS) the
(normalized) cross-correlation function (CCF)
of two continuous signals :math:`I_1(t)` and
:math:`I_2(t)` is defined as:

.. math::
    G(\tau) = \frac{\langle I_1(t)\; I_2(t) \rangle}
                   {\langle I_1(t)\rangle\langle I_2(t) \rangle}

The auto-correlation function (ACF) is just a special case where
:math:`I_1(t) = I_2(t)`.

In actual experiments, signals are not continuous but come from
single-photon detectors that produce a pulse for each photon. These pulses
are usually timestamped with ~10ns resolution. The series of photon
arrival times is used as input for ACF or CCF computations.

In principle, timestamps can be binned to produce a discrete-time signal.
In signal processing, the (non-normalized) cross-correlation of two
real discrete-time signals :math:`\{A_i\}` and
:math:`\{B_i\}` is defined as

.. math::
    c[k] = \sum_{i=0}^{N} A[i]\ B[i+k].

The previous formula is implemented by :func:`ucorrelate` and
`numpy.correlate <https://docs.scipy.org/doc/numpy/reference/generated/numpy.correlate.html#numpy.correlate>`__.
The difference is that :func:`ucorrelate` only computes positive lags and
allows setting a max lag for efficiency.

Binning timestamps to obtain timetraces would be very inefficient for FCS
analysis where time-lags span may orders of magnitude.
It is much more efficient to directly compute the cross-correlation function
from timestamps.
The popular multi-tau algorithm allows computing the correlation directly
from timestamps on a fixed arrangement of quasi-log-spaced bins.
More generally, Laurence algorithm
(`Laurence et al. Optics Letters (2006) <https://doi.org/10.1364/OL.31.000829>`__)
allows computing cross-correlation from timestamps on arbitrary bins of
time-lags, with similar performances as the multi-tau.
Computing cross-correlation :math:`C(\tau)` from timestamps is fundamentally
a counting tasks. Given two timestamps arrays *t* and *u* and
considering the k-th time-lag bin :math:`[\tau_k, \tau_{k+1})`,
:math:`C(k)` is equal to the number of pairs where:

.. math::
    \tau_k \le t_i - u_j < \tau_{k+1}

for all the possible *i* and *j* combinations.
The full expression for :math:`C(k)` is:

.. math::
    C(k) = \frac{n(\{(i,j) \ni t_i < u_i - \Delta\tau_k\})}{\Delta\tau_k}
    :label: Ck

where `n({})` is the operator counting the elements in a set,
:math:`\Delta\tau_k` is the duration of the k-th time-lag bin and *T*
is the measurement duration.
For FCS we normally want the normalized CCF, that is:

.. math::
    G(k) = \frac{n(\{(i,j) \ni t_i < u_i - \Delta\tau_k\})}
                {n(\{i \ni t_i \le T - \Delta\tau_k\})\:n(\{j \ni u_j \ge \Delta\tau_k\})}
           \frac{(T-\Delta\tau_k)}{\Delta\tau_k}
    :label: Gk

Both eq. :eq:`Ck` and :eq:`Gk` are implemented by :func:`pcorrelate`.
You can choose between the normalized and unnormalized version with the
input argument `normalize`.

.. note::
    Due to a typo, in *Laurence 2006*, the expression for *G(k)*
    (which they call :math:`C_{AB}(\tau)`) is missing the term
    :math:`\Delta\tau_k` in the denominator.

References
----------

- Laurence, T. A., Fore, S., Huser, T. (2006). Fast, flexible algorithm for
  calculating photon correlations. *Optics Letters* , *31* (6), 829–831.
  https://doi.org/10.1364/OL.31.000829

- Petra Schwille and Elke Haustein,
  `Fluorescence Correlation Spectroscopy  An Introduction to its Concepts and Applications <http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.405.2487&rep=rep1&type=pdf>`__

- Haustein, E., Schwille, P. (2003). Ultrasensitive investigations of biological
  systems by fluorescence correlation spectroscopy. *Methods*, *29* (2),
  153–166. https://doi.org/10.1016/S1046-2023(02)00306-7
