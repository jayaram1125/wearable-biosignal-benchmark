import numpy as np
from common.signal import bandpass, resample, zscore, make_windows, window_starts


def test_bandpass_keeps_in_band_and_removes_out_of_band():
    fs, t = 64, np.arange(0, 20, 1 / 64)
    x = np.sin(2 * np.pi * 1.2 * t) + np.sin(2 * np.pi * 0.05 * t) + np.sin(2 * np.pi * 10 * t)
    y = bandpass(x, fs, 0.5, 3.5)
    f = np.fft.rfftfreq(len(t), 1 / fs); Y = np.abs(np.fft.rfft(y))
    assert f[np.argmax(Y)] == min(f, key=lambda v: abs(v - 1.2))


def test_resample_length_and_content():
    fs_in, fs_out = 64, 125
    x = np.sin(2 * np.pi * 1.0 * np.arange(0, 8, 1 / fs_in))
    y = resample(x, fs_in, fs_out)
    assert abs(len(y) - 8 * fs_out) <= 1
    f = np.fft.rfftfreq(len(y), 1 / fs_out); assert abs(f[np.argmax(np.abs(np.fft.rfft(y)))] - 1.0) < 0.2


def test_zscore_and_windows():
    x = np.random.default_rng(0).normal(size=(4, 512)) * 3 + 7
    z = zscore(x); assert np.allclose(z.mean(-1), 0, atol=1e-6) and np.allclose(z.std(-1), 1, atol=1e-3)
    sig = np.arange(64 * 30, dtype=float)
    w = make_windows(sig, 64, 8, 2)
    assert w.shape == (len(window_starts(len(sig), 64, 8, 2)), 512) and w[1, 0] == 128
    assert make_windows(sig, 64, 8, 2, n_windows=3).shape == (3, 512)
