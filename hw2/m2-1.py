def solve_recursive(n):
    """
    T(n) = T(n-1) + 8, T(1) = 1
    Time Complexity: O(n)
    """
    if n <= 1:
        return 1
    return solve_recursive(n - 1) + 8

def solve_closed_form(n):
    """Exact Closed-Form Solution: 8n - 7"""
    return 8 * n - 7
