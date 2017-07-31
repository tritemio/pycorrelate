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

The cross-correlation on uniformly-spaced signal is similar to the
`numpy.correlate` function, but allows defining a max lag for efficiency.

The point-process cross-correlation is implemented using the algorithm
described in
`Laurence et al. Optics Letters (2006) <https://doi.org/10.1364/OL.31.000829>`__.
This algorithm is a generalization of the multi-tau algorithm which retains
high execution speed while allowing arbitrary time-lag bins.

Pycorrelate is implemented in Python 3 and operates on standard numpy arrays.
Execution speed is optimized using `numba <https://numba.pydata.org/>`__.

* Free software: GNU General Public License v3
* Documentation: https://pycorrelate.readthedocs.io.
