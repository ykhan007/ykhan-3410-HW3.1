"""
SortFunctions.py — Iterative Merge Sort (G4G-style), adapted for Python lists.
We sort a list of tuples; Python's tuple comparison compares elementwise,
so if our element is ((y,i,q),(x,y)), sorting naturally orders by Y first.
"""

from typing import List, Any

def _merge(arr: List[Any], l: int, m: int, r: int) -> None:
    n1, n2 = m - l + 1, r - m
    L = arr[l : m + 1]
    R = arr[m + 1 : r + 1]

    i = j = 0
    k = l
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1; k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1; k += 1

def merge_sort_iterative(arr: List[Any]) -> None:
    """Bottom-up (iterative) merge sort."""
    n = len(arr)
    size = 1
    while size < n:
        left = 0
        while left < n - 1:
            mid = min(left + size - 1, n - 1)
            right = min(left + 2 * size - 1, n - 1)
            if mid < right:
                _merge(arr, left, mid, right)
            left += 2 * size
        size *= 2
