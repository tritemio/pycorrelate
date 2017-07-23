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


**Pycorrelate** computes fast and accurate correlations of timestamps
with arbitrary time lags.
This type of correlation is very common in physics or biophysics
for techniques such as
*fluorescence correlation spectroscopy* (`FCS <https://en.wikipedia.org/wiki/Fluorescence_correlation_spectroscopy>`__) or
*dynamic light scattering* (`DLS <https://en.wikipedia.org/wiki/Dynamic_light_scattering>`__).

Correlation is implemented using the algorithm described in
`Laurence et al. Optics Letters (2006) <https://doi.org/10.1364/OL.31.000829>`__.
This is a generalization of the multi-tau algorithm which retains
high execution speed while allowing arbitrary time-lag bins.

Pycorrelate is implemented in Python 3 and operates on standard numpy arrays.
If you need compute correlation of signals defined as function of time
(i.e. timetraces) you should use the standard functions
``numpy.correlate`` or ``scipy.signal.correlate``.
Pycorrelate is useful to efficiently compute correlation
when inputs are *timestamps of discrete events*, such as photon arrival times.

* Free software: GNU General Public License v3
* Documentation: https://pycorrelate.readthedocs.io.
