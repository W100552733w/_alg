import numpy as np

# Custom Problem: Finding the Golden Ratio (phi = 1.6180339887...)
# Algebraic Equation: x^2 - x - 1 = 0

# Method 1: Divergent form (x = x^2 - 1)
f1 = lambda x: x**2 - 1.0

# Method 2: Linear convergence form (x = 1 + 1/x)
f2 = lambda x: 1.0 + 1.0 / x

# Method 3: Quadratic convergence form (Newton's Method: x = (x^2 + 1) / (2x - 1))
f3 = lambda x: (x**2 + 1.0) / (2.0 * x - 1.0)

# Initial guess
x1 = x2 = x3 = 2.0

print(f"{'Iteration':<10} | {'Method 1 (Divergent)':<25} | {'Method 2 (Linear)':<25} | {'Method 3 (Quadratic)':<25}")
print("-" * 90)

for i in range(1, 16):
    # Prevent overflow for the divergent method
    x1 = f1(x1) if abs(x1) < 1e6 else float('inf')
    x2 = f2(x2)
    x3 = f3(x3)
    print(f"{i:<10} | {x1:<25.6f} | {x2:<25.8f} | {x3:<25.10f}")
