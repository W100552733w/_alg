memo = {0: 1}

def power2n(n):
    if n in memo:
        return memo[n]
    memo[n] = power2n(n-1) + power2n(n-1)
    return memo[n]
