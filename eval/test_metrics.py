import os
import sys

import numpy as np
from scipy.ndimage import gaussian_filter
from skimage import data

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from metrics import mae, psnr, rmse, ssim, temporal_consistency  # noqa: E402

IMG = data.camera()
BLURRED = gaussian_filter(IMG.astype(np.float64), sigma=3)


def test_same_image_gives_ssim_1():
    assert abs(ssim(IMG, IMG) - 1.0) < 1e-9


def test_blurred_copy_gives_lower_ssim():
    assert ssim(IMG, BLURRED) < 1.0


def test_more_blur_gives_lower_ssim():
    more = gaussian_filter(IMG.astype(np.float64), sigma=6)
    assert ssim(IMG, more) < ssim(IMG, BLURRED)


def test_identical_images_have_zero_error():
    assert mae(IMG, IMG) == 0.0
    assert rmse(IMG, IMG) == 0.0
    assert psnr(IMG, IMG) == float("inf")


def test_known_values():
    a = np.zeros((4, 4), dtype=np.uint8)
    b = np.full((4, 4), 10, dtype=np.uint8)
    assert mae(a, b) == 10.0
    assert rmse(a, b) == 10.0
    assert abs(psnr(a, b) - 20 * np.log10(255 / 10)) < 1e-9


def test_uint8_does_not_wrap():
    a = np.array([[100]], dtype=np.uint8)
    b = np.array([[110]], dtype=np.uint8)
    assert mae(a, b) == 10.0


def test_temporal_consistency_identical_frames_is_100():
    assert abs(temporal_consistency([IMG, IMG, IMG]) - 100.0) < 1e-7


def test_temporal_consistency_drops_with_flicker():
    rng = np.random.default_rng(0)
    steady = [IMG] * 4
    noisy = [np.clip(IMG + rng.normal(0, 25, IMG.shape), 0, 255) for _ in range(4)]
    assert temporal_consistency(noisy) < temporal_consistency(steady)


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    for name, fn in tests:
        fn()
        print(f"PASS  {name}")
    print(f"\nAll {len(tests)} tests passed.")
    print(f"SSIM same image : {ssim(IMG, IMG):.4f}")
    print(f"SSIM blurred    : {ssim(IMG, BLURRED):.4f}")