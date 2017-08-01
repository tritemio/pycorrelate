===========
Pycorrelate
===========


.. image:: https://img.shields.io/pypi/v/pycorrelate.svg
        :target: https://pypi.python.org/pypi/pycorrelate

.. image:: https://img.shields.io/travis/tritemio/pycorrelate.svg
        :target: https://travis-ci.org/tritemio/pycorrelate

.. image:: https://readthedocs.org/projects/pycorrelate/badge/?version=latest
        :target: https://pycorrelate.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/tritemio/pycorrelate/shield.svg
     :target: https://pyup.io/repos/github/tritemio/pycorrelate/
     :alt: Updates


**Pycorrelate** computes fast and accurate cross-correlation over
arbitrary time lags.
Cross-correlations can be calculated on "uniformly-sampled" signals
or on "point-processes", such as photon timestamps.
Pycorrelate allows computing cross-correlation at log-spaced lags covering
several orders of magnitude. This type of cross-correlation is
commonly used in physics or biophysics for techniques such as
*fluorescence correlation spectroscopy* (`FCS <https://en.wikipedia.org/wiki/Fluorescence_correlation_spectroscopy>`__) or
*dynamic light scattering* (`DLS <https://en.wikipedia.org/wiki/Dynamic_light_scattering>`__).

Two types of correlations are implemented:

- `ucorrelate <https://pycorrelate.readthedocs.io/en/latest/api.html#pycorrelate.pycorrelate.ucorrelate>`__:
  the classical text-book linear cross-correlation between two signals
  defined at **uniformly spaced** intervals.
  Only positive lags are computed and a max lag can be specified.
  Thanks to the limit in the computed lags, this function is much faster than
  `numpy.correlate <https://docs.scipy.org/doc/numpy/reference/generated/numpy.correlate.html#numpy.correlate>`__.

- `pcorrelate <https://pycorrelate.readthedocs.io/en/latest/api.html#pycorrelate.pycorrelate.pcorrelate>`__:
  cross-correlation of discrete events
  in a point-process. In this case input arrays can be timestamps or
  positions of "events", for example **photon arrival times**.
  This function implements the algorithm in
  `Laurence et al. Optics Letters (2006) <https://doi.org/10.1364/OL.31.000829>`__.
  This is a generalization of the multi-tau algorithm which retains
  high execution speed while allowing arbitrary time-lag bins.

Pycorrelate is implemented in Python 3 and operates on standard numpy arrays.
Execution speed is optimized using `numba <https://numba.pydata.org/>`__.

* Free software: GNU General Public License v3
* Documentation: https://pycorrelate.readthedocs.io.
