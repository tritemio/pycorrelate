#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pycorrelate` package."""

import pytest
import h5py
import numpy as np

from pycorrelate import correlate


# data subdir in the notebook folder
DATASETS_DIR = u'notebooks/data/'


def load_dataset():
    fn = "0023uLRpitc_NTP_20dT_0.5GndCl.hdf5"
    fname = DATASETS_DIR + fn
    h5 = h5py.File(fname)
    num_ph = int(10e3)
    timestamps = h5['photon_data']['timestamps'][:num_ph]
    detectors = h5['photon_data']['detectors'][:num_ph]
    t = timestamps[detectors == 0]
    u = timestamps[detectors == 1]
    # In the algorithm I assume t[0] < u[0], if not true swap u and v
    if t[0] > u[0]:
        t, u = u, t
    return t, u


@pytest.fixture()
def data():
    t, u = load_dataset()
    return t, u


def test_correlate(data):
    """Test correlate."""
    t, u = data
    bins = np.logspace(0, 28, 29, base=2, dtype='int64')
    nbins = len(bins) - 1
    G = correlate(t, u, bins)

    Y = np.zeros(nbins, dtype=np.int64)
    for ti in t:
        Yc, _ = np.histogram(u - ti, bins=bins)
        Y += Yc
    Gn = Y / np.diff(bins)
    assert (G == Gn).all()
