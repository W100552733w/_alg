import numpy as np

# =====================================================================
# 1. Core Abstract Framework
# =====================================================================
def generic_iterator(transition_func, is_converged, initial_state, max_iter=1000):
    """
    Generic Iterative Framework
    :param transition_func: State advancement function g(state) -> next_state
    :param is_converged: Convergence check function is_converged(state, next_state, iteration) -> bool
    :param initial_state: The starting state (scalar, vector, matrix, or tuple)
    :return: final_state, actual_iterations
    """
    state = initial_state
    
    for iteration in range(max_iter):
        next_state = transition_func(state)
        
        if is_converged(state, next_state, iteration):
            return next_state, iteration + 1
            
        state = next_state
        
    print("  [Warning] Maximum iterations reached without full convergence.")
    return state, max_iter


# =====================================================================
# 2. Concrete Implementations
# =====================================================================
def demo_fixed_point():
    print("--- 1. Fixed-Point Iteration ---")
    transition = lambda X: np.array([0.5 * X[0] - 0.2 * X[1] + 0.3, 0.2 * X[0] + 0.5 * X[1] + 0.4])
    converged = lambda old, new, i: np.linalg.norm(new - old) < 1e-6
    result, iters = generic_iterator(transition, converged, initial_state=np.array([0.0, 0.0]))
    print(f"Result: {np.round(result, 6)} (Took {iters} iterations)\n")


def demo_newton():
    print("--- 2. Newton's Method (x^2 - 4 = 0) ---")
    f = lambda x: x**2 - 4.0
    df = lambda x: 2.0 * x
    transition = lambda x: x - f(x) / df(x)
    converged = lambda old, new, i: abs(new - old) < 1e-6
    result, iters = generic_iterator(transition, converged, initial_state=1.0)
    print(f"Result: Root x = {result:.6f} (Took {iters} iterations)\n")


def demo_gauss_seidel():
    print("--- 3. Gauss-Seidel Linear Solver ---")
    A = np.array([[4.0, -1.0, 0.0], [-1.0, 4.0, -1.0], [0.0, -1.0, 4.0]])
    b = np.array([7.0, 2.0, 13.0])
    n = len(b)
    
    def transition(x):
        x_new = x.copy()
        for i in range(n):
            s = sum(A[i, j] * x_new[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i, i]
        return x_new
        
    converged = lambda old, new, i: np.max(np.abs(new - old)) < 1e-6
    result, iters = generic_iterator(transition, converged, initial_state=np.zeros(n))
    print(f"Result: x = {np.round(result, 6)} (Took {iters} iterations)\n")


def demo_power_iteration():
    print("--- 4. Power Iteration (Largest Eigenvalue) ---")
    A = np.array([[4.0, 1.0, 0.5], [1.0, 3.0, 0.2], [0.5, 0.2, 2.0]])
    n = A.shape[0]
    transition = lambda v: np.dot(A, v) / np.linalg.norm(np.dot(A, v))
    converged = lambda old, new, i: np.allclose(old, new, atol=1e-6)
    
    np.random.seed(42)
    v_init = np.random.rand(n)
    v_init /= np.linalg.norm(v_init)
    
    v_result, iters = generic_iterator(transition, converged, initial_state=v_init)
    eigenval = np.dot(v_result, np.dot(A, v_result))
    print(f"Result: Max Eigenvalue = {eigenval:.6f} (Took {iters} iterations)\n")


def demo_qr_algorithm():
    print("--- 5. QR Algorithm (All Eigenvalues) ---")
    A = np.array([[4.0, 1.0, -2.0], [1.0, 2.0, 0.0], [-2.0, 0.0, 3.0]], dtype=float)
    transition = lambda Ak: np.dot(*reversed(np.linalg.qr(Ak)))
    converged = lambda old, new, i: np.sum(np.abs(new - np.diag(np.diagonal(new)))) < 1e-6
    
    A_final, iters = generic_iterator(transition, converged, initial_state=A)
    print(f"Result: All Eigenvalues = {np.round(np.diagonal(A_final), 6)} (Took {iters} iterations)\n")


def demo_rk4():
    print("--- 6. Runge-Kutta 4 (RK4 ODE Solver: dy/dt = y - t + 1) ---")
    f = lambda t, y: y - t + 1
    t_end, h = 2.0, 0.2
    
    def transition(state):
        t, y = state
        k1 = f(t, y)
        k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
        k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
        k4 = f(t + h, y + h * k3)
        return (t + h, y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4))
        
    converged = lambda old, new, i: new[0] >= t_end - 1e-9
    final_state, iters = generic_iterator(transition, converged, initial_state=(0.0, 1.0))
    print(f"Result: At t = {final_state[0]:.1f}, y = {final_state[1]:.6f} (Took {iters} steps)\n")


def demo_pagerank():
    print("--- 7. PageRank (Random Surfer Model) ---")
    M = np.array([[0.0, 0.0, 1.0, 0.5],
                  [1/3, 0.0, 0.0, 0.5],
                  [1/3, 0.5, 0.0, 0.0],
                  [1/3, 0.5, 0.0, 0.0]])
    d = 0.85
    n = M.shape[0]
    G = d * M + (1 - d) / n * np.ones((n, n)) 
    
    transition = lambda r: np.dot(G, r)
    converged = lambda old, new, i: np.linalg.norm(new - old) < 1e-6
    
    r_init = np.ones(n) / n
    r_result, iters = generic_iterator(transition, converged, initial_state=r_init)
    print(f"Result: Page Weights = {np.round(r_result, 4)} (Took {iters} iterations)\n")


def demo_kmeans():
    print("--- 8. K-Means Clustering (Hard EM) ---")
    np.random.seed(42)
    X = np.vstack([np.random.randn(15, 2) + np.array([2, 2]),
                   np.random.randn(15, 2) + np.array([-2, -2])])
    k = 2
    init_centroids = X[:k].copy()
    
    def transition(centroids):
        distances = np.linalg.norm(X[:, np.newaxis] - centroids, axis=2)
        labels = np.argmin(distances, axis=1)
        return np.array([X[labels == j].mean(axis=0) for j in range(k)])
        
    converged = lambda old, new, i: np.max(np.abs(new - old)) < 1e-6
    centroids_result, iters = generic_iterator(transition, converged, initial_state=init_centroids)
    print(f"Result: Final Centroids = \n{np.round(centroids_result, 4)} (Took {iters} iterations)\n")


def demo_em_two_coin():
    print("--- 9. EM Algorithm (Two-Coin Problem) ---")
    trials = np.array([[5, 5], [9, 1], [8, 2], [4, 6], [7, 3]])
    init_theta = (0.6, 0.5) 
    
    def transition(theta):
        theta_A, theta_B = theta
        cA_h = cA_t = cB_h = cB_t = 0.0
        
        for h, t in trials:
            l_A = (theta_A ** h) * ((1 - theta_A) ** t)
            l_B = (theta_B ** h) * ((1 - theta_B) ** t)
            p_A = l_A / (l_A + l_B) if (l_A + l_B) > 0 else 0.5
            p_B = 1.0 - p_A
            
            cA_h += p_A * h; cA_t += p_A * t
            cB_h += p_B * h; cB_t += p_B * t
            
        return (cA_h / (cA_h + cA_t), cB_h / (cB_h + cB_t))
        
    converged = lambda old, new, i: abs(new[0] - old[0]) < 1e-6 and abs(new[1] - old[1]) < 1e-6
    theta_result, iters = generic_iterator(transition, converged, initial_state=init_theta)
    print(f"Result: Theta_A = {theta_result[0]:.4f}, Theta_B = {theta_result[1]:.4f} (Took {iters} iterations)\n")


# =====================================================================
# 3. Execute All
# =====================================================================
if __name__ == "__main__":
    print("=========================================================")
    print("   Unified Framework for Classical Iterative Methods")
    print("=========================================================\n")
    
    demo_fixed_point()
    demo_newton()
    demo_gauss_seidel()
    demo_power_iteration()
    demo_qr_algorithm()
    demo_rk4()
    demo_pagerank()
    demo_kmeans()
    demo_em_two_coin()
