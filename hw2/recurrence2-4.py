import math

def solve_recursive(n):
    """
    T(n) = T(n/2) + 1, T(1) = 1
    Time Complexity: O(log n)
    """
    if n <= 1:
        return 1
    return solve_recursive(n // 2) + 1

def solve_closed_form(n):
    """Exact Closed-Form Solution: log2(n) + 1"""
    return int(math.log2(n)) + 1
