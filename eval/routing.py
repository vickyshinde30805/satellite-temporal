"""Gap-aware routing: pick an interpolation method from the time gap between frames.

  small gap       -> RIFE
  bigger gap      -> RAFT warp
  very large gap  -> RAFT warp, but flagged LOW CONFIDENCE with a warning

THE THRESHOLDS BELOW ARE PLACEHOLDERS. Replace them with values from real results.
"""

import math
from typing import NamedTuple, Optional

# ---- PLACEHOLDER THRESHOLDS (minutes) - change these after real experiments ----
RIFE_MAX_GAP = 15   # gap <= this                -> RIFE
RAFT_MAX_GAP = 40   # RIFE_MAX_GAP < gap <= this -> RAFT; above this -> low confidence
# --------------------------------------------------------------------------------


class RoutingDecision(NamedTuple):
    method: str                 # "RIFE" or "RAFT"
    low_confidence: bool        # True when the gap is beyond what we trust
    warning: Optional[str]      # message to show the user, or None


def choose_method(gap_minutes):
    """Return a RoutingDecision for a gap between two frames, in minutes."""
    if isinstance(gap_minutes, bool) or not isinstance(gap_minutes, (int, float)):
        raise TypeError(f"gap_minutes must be a number, got {type(gap_minutes).__name__}")
    if math.isnan(gap_minutes) or gap_minutes <= 0:
        raise ValueError(f"gap_minutes must be a positive number, got {gap_minutes}")

    if gap_minutes <= RIFE_MAX_GAP:
        return RoutingDecision("RIFE", False, None)

    if gap_minutes <= RAFT_MAX_GAP:
        return RoutingDecision("RAFT", False, None)

    warning = (
        f"Low confidence: a {gap_minutes:g}-minute gap is larger than the "
        f"{RAFT_MAX_GAP}-minute limit we have validated. Using RAFT warping as a "
        f"best effort; the interpolated frame may be inaccurate."
    )
    return RoutingDecision("RAFT", True, warning)


if __name__ == "__main__":
    for g in (5, 10, 15, 20, 40, 41, 90):
        d = choose_method(g)
        note = f"  <- {d.warning}" if d.warning else ""
        print(f"gap {g:>3} min -> {d.method:<4} low_confidence={d.low_confidence}{note}")