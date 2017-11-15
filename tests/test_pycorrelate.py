#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pycorrelate` package."""

import pytest
import h5py
import numpy as np

import pycorrelate as pyc


DATA_URL = 'http://files.figshare.com/4917046/smFRET_44f3da_P_20_s0_20_s20_D_6.0e11_6.0e11_E_75_30_EmTot_200k_200k_BgD1500_BgA800_t_max_600s.hdf5'


def load_dataset():
    pyc.utils.download_file(DATA_URL, save_dir='data')
    fname = './data/' + DATA_URL.split('/')[-1]
    h5 = h5py.File(fname)
    num_ph = int(10e3)
    timestamps = h5['photon_data']['timestamps'][:num_ph]
    detectors = h5['photon_data']['detectors'][:num_ph]
    unit = h5['photon_data']['timestamps_specs']['timestamps_unit'][()]
    t = timestamps[detectors == 0]
    u = timestamps[detectors == 1]
    return t, u, unit


@pytest.fixture()
def data():
    t, u, unit = load_dataset()
    return t, u, unit



def test_pcorrelate(data):
    """Test pcorrelate algorithm using np.histogram."""
    t, u, unit = data
    n = 10000  # ~ 3s of data
    t, u = t[:n], u[:n]
    bins = pyc.make_loglags(-6, 0, 20, base=10) / unit
    nbins = len(bins) - 1
    G = pyc.pcorrelate(t, u, bins)

    Y = np.zeros(nbins, dtype=np.int64)
    for ti in t:
        Yc, _ = np.histogram(u - ti, bins=bins)
        Y += Yc
    Gn = Y / np.diff(bins)

    # The last bin in np.histogram includes the right edge while pcorrelate
    # does not. This creates a potential discrepancy for the last bin.
    assert np.allclose(G, Gn)
    assert np.allclose(G[:-1], Gn[:-1])
    # However the value in the last bin when using np.histogram needs to be
    # >= than pcorrelate value.
    assert (Gn[-1] >= G[-1]).all()


def test_pcorrelate_normalization(data):
    """Test pcorrelate algorithm using np.histogram."""
    t, u, unit = data
    bins = pyc.make_loglags(-6, 0, 20, base=10) / unit
    Gn = pyc.pcorrelate(t, u, bins, normalize=True)
    G = pyc.pcorrelate(t, u, bins, normalize=False)
    Gn2 = pyc.pnormalize(G, t, u, bins)
    assert (Gn == Gn2).all()


def test_ucorrelate(data):
    """Test ucorrelate against np.correlate."""
    t, u, unit = data
    binwidth = 50e-6
    bins_tt = np.arange(0, t.max() * unit, binwidth) / unit
    bins_uu = np.arange(0, u.max() * unit, binwidth) / unit
    tx, _ = np.histogram(t, bins=bins_tt)
    ux, _ = np.histogram(u, bins=bins_uu)
    C = np.correlate(ux, tx, mode='full')
    Gn = C[tx.size - 1:]  # trim to positive time lags
    Gu = pyc.ucorrelate(tx, ux)
    assert (Gu == Gn).all()
    Gu2 = pyc.ucorrelate(tx, ux, maxlag=1000)
    assert (Gu2 == Gn[:1000]).all()


def test_pcorrelate_vs_ucorrelate(data):
    t, u, unit = data
    binwidth = 50e-6
    bins_tt = np.arange(0, t.max() * unit, binwidth) / unit
    bins_uu = np.arange(0, u.max() * unit, binwidth) / unit
    tx, _ = np.histogram(t, bins=bins_tt)
    ux, _ = np.histogram(u, bins=bins_uu)
    Gu = pyc.ucorrelate(tx, ux)
    maxlag_sec = 1.2  # seconds
    lagbins = (np.arange(0, maxlag_sec, binwidth) / unit).astype('int64')
    Gp = pyc.pcorrelate(t, u, lagbins) * int(binwidth / unit)
    n = 6000
    err = np.abs(Gp[:n] - Gu[:n]) / (0.5 * (Gp[:n] + Gu[:n]))
    assert err.max() < 0.23
    assert err.mean() < 0.05
