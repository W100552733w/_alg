def solve_recursive(n):
    """
    T(n) = 2T(n/2) + 1, T(1) = 1
    Time Complexity: O(n)
    """
    if n <= 1:
        return 1
    return 2 * solve_recursive(n // 2) + 1

def solve_closed_form(n):
    """Exact Closed-Form Solution: 2n - 1"""
    return 2 * n - 1
