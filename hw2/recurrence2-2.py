def solve_recursive(n):
    """
    T(n) = 2T(n-1) + 9, T(1) = 1
    Time Complexity: O(2^n)
    """
    if n <= 1:
        return 1
    return 2 * solve_recursive(n - 1) + 9

def solve_closed_form(n):
    """Exact Closed-Form Solution: 5 * 2^n - 9"""
    return 5 * (2 ** n) - 9
