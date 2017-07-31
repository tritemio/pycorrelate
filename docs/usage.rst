=====
Usage
=====

Imports::

    import numpy as np
    import pycorrelate as pyc

Create two arrays `t` and `u` of discrete events, exponentially correlated::

    np.random.seed(1)
    size = 10**4
    t = np.sort(np.random.randint(0, 10**5, size=size))
    u = np.sort(t + np.random.exponential(scale=10, size=t.size).astype(np.int64))

Compute correlation::

    lags = np.arange(0, 201)
    G = pyc.pcorrelate(t, u, lags)

`G` contains the cross-correlation of `t` and `u` at the defined `lags`.

For more examples see :doc:`notebooks/pycorrelate-examples`.
