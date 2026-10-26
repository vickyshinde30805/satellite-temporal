import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import routing  # noqa: E402
from routing import RAFT_MAX_GAP, RIFE_MAX_GAP, choose_method  # noqa: E402


def test_small_gap_uses_rife():
    d = choose_method(5)
    assert d.method == "RIFE" and not d.low_confidence and d.warning is None


def test_rife_boundary_is_inclusive():
    assert choose_method(RIFE_MAX_GAP).method == "RIFE"


def test_just_above_rife_limit_uses_raft():
    d = choose_method(RIFE_MAX_GAP + 1)
    assert d.method == "RAFT" and not d.low_confidence and d.warning is None


def test_raft_boundary_is_inclusive():
    d = choose_method(RAFT_MAX_GAP)
    assert d.method == "RAFT" and not d.low_confidence


def test_very_large_gap_is_low_confidence_with_warning():
    d = choose_method(RAFT_MAX_GAP + 1)
    assert d.low_confidence is True
    assert d.warning and "Low confidence" in d.warning
    assert d.method == "RAFT"


def test_float_gap_works():
    assert choose_method(7.5).method == "RIFE"


def test_bad_values_raise():
    for bad in (0, -5, float("nan")):
        try:
            choose_method(bad)
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError for {bad}")
    for bad in ("10", None, True):
        try:
            choose_method(bad)
        except TypeError:
            continue
        raise AssertionError(f"expected TypeError for {bad!r}")


def test_thresholds_are_in_order():
    assert 0 < routing.RIFE_MAX_GAP < routing.RAFT_MAX_GAP


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    for name, fn in tests:
        fn()
        print(f"PASS  {name}")
    print(f"\nAll {len(tests)} tests passed.")
