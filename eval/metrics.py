"""Image quality metrics for the satellite-temporal project."""

import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity


def _prepare(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    if a.shape != b.shape:
        raise ValueError(f"Shape mismatch: {a.shape} vs {b.shape}")
    return a, b


def _channel_axis(img):
    return -1 if img.ndim == 3 else None


def mae(true, pred):
    """Mean absolute error. Lower is better, 0 is perfect."""
    true, pred = _prepare(true, pred)
    return float(np.mean(np.abs(true - pred)))


def rmse(true, pred):
    """Root mean squared error. Lower is better, 0 is perfect."""
    true, pred = _prepare(true, pred)
    return float(np.sqrt(np.mean((true - pred) ** 2)))


def psnr(true, pred, data_range=255):
    """Peak signal-to-noise ratio in dB. Higher is better."""
    true, pred = _prepare(true, pred)
    if np.array_equal(true, pred):
        return float("inf")
    return float(peak_signal_noise_ratio(true, pred, data_range=data_range))


def ssim(true, pred, data_range=255):
    """Structural similarity. 1 is perfect."""
    true, pred = _prepare(true, pred)
    return float(
        structural_similarity(
            true, pred, data_range=data_range, channel_axis=_channel_axis(true)
        )
    )


def temporal_consistency(frames, data_range=255):
    """Average SSIM between neighbouring frames, as a percent (0-100)."""
    frames = list(frames)
    if len(frames) < 2:
        raise ValueError("temporal_consistency needs at least 2 frames")
    scores = [
        ssim(frames[i], frames[i + 1], data_range=data_range)
        for i in range(len(frames) - 1)
    ]
    return float(np.mean(scores) * 100.0)