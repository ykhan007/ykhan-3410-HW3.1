"""
SearchFunctions.py — helpers for searching in sorted Y values.
"""

from typing import List

def lower_bound(arr: List[float], target: float) -> int:
    """First index i where arr[i] >= target (or len(arr) if none)."""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo
