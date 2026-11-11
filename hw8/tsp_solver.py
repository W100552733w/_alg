"""
第八週作業：旅行推銷員問題 (TSP) 的五種求解演算法實作
姓名：葉俊成  學號：111210544
"""

import math
import random
import time

# -------------------------------------------------------------
# 1. 基礎工具：距離計算與總路徑長度評估
# -------------------------------------------------------------
def euclidean_dist(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def total_distance(tour, cities):
    """計算閉合路徑的總歐幾里得距離"""
    d = 0.0
    n = len(tour)
    for i in range(n):
        c1 = cities[tour[i]]
        c2 = cities[tour[(i + 1) % n]]
        d += euclidean_dist(c1, c2)
    return d


# -------------------------------------------------------------
# 1. 改良法 (2-opt Improvement Method)
# -------------------------------------------------------------
def solve_2opt_improvement(cities, max_rounds=200):
    """
    2-opt 局部改良法：檢查所有邊對，若反轉子路徑能減少距離則進行反轉更新
    """
    n = len(cities)
    tour = list(range(n))
    improved = True
    rounds = 0

    while improved and rounds < max_rounds:
        improved = False
        rounds += 1
        for i in range(n - 1):
            for j in range(i + 2, n if i != 0 else n - 1):
                # 測試反轉 tour[i+1:j+1]
                a, b = tour[i], tour[(i + 1) % n]
                c, d = tour[j], tour[(j + 1) % n]
                cur_edges = euclidean_dist(cities[a], cities[b]) + euclidean_dist(cities[c], cities[d])
                new_edges = euclidean_dist(cities[a], cities[c]) + euclidean_dist(cities[b], cities[d])
                
                if new_edges < cur_edges - 1e-9:
                    tour[i + 1 : j + 1] = reversed(tour[i + 1 : j + 1])
                    improved = True
                    break
            if improved:
                break
    return tour, total_distance(tour, cities)


# -------------------------------------------------------------
# 2. 爬山演算法 (Hill Climbing)
# -------------------------------------------------------------
def solve_hill_climbing(cities, max_iter=2000):
    """
    爬山演算法：隨機產生鄰居（隨機交換兩城市），若嚴格更優則接受，否則放棄
    """
    n = len(cities)
    tour = list(range(n))
    random.shuffle(tour)
    best_dist = total_distance(tour, cities)

    for _ in range(max_iter):
        i, j = random.sample(range(n), 2)
        new_tour = tour[:]
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        new_dist = total_distance(new_tour, cities)

        # 僅在有進步時往「上」爬（目標為距離越短越好）
        if new_dist < best_dist:
            tour, best_dist = new_tour, new_dist

    return tour, best_dist


# -------------------------------------------------------------
# 3. 模擬退火法 (Simulated Annealing)
# -------------------------------------------------------------
def solve_simulated_annealing(cities, init_temp=1000.0, alpha=0.995, max_iter=5000):
    """
    模擬退火法：以波茲曼機率 exp(-delta / T) 接受較差解，跳脫局部最佳解
    """
    n = len(cities)
    tour = list(range(n))
    random.shuffle(tour)
    current_dist = total_distance(tour, cities)

    best_tour = tour[:]
    best_dist = current_dist
    temp = init_temp

    for _ in range(max_iter):
        if temp < 1e-6:
            break
        i, j = sorted(random.sample(range(n), 2))
        # 鄰域結構：區間翻轉
        new_tour = tour[:i] + list(reversed(tour[i : j + 1])) + tour[j + 1 :]
        new_dist = total_distance(new_tour, cities)

        delta = new_dist - current_dist
        # Metropilis 準則
        if delta < 0 or random.random() < math.exp(-delta / temp):
            tour = new_tour
            current_dist = new_dist
            if current_dist < best_dist:
                best_tour = tour[:]
                best_dist = current_dist

        temp *= alpha

    return best_tour, best_dist


# -------------------------------------------------------------
# 4. 梯度下降法 (連續鬆弛化連續空間數值梯度下降)
# -------------------------------------------------------------
def solve_gradient_descent(cities, lr=0.05, epochs=300):
    """
    梯度下降法求解 TSP：
    TSP 為離散組合問題，傳統梯度無法直接求導。
    本方法採用「連續座標鬆弛法（Continuous Relaxation）」：
    為每個拜訪順序分配 1D 實數潛在變數 theta_i，路徑即為 argsort(theta)。
    以數值微分 (Finite Difference) 估算梯度並沿著負梯度更新 theta。
    """
    n = len(cities)
    theta = [random.random() for _ in range(n)]

    def get_loss(t_vec):
        order = sorted(range(n), key=lambda idx: t_vec[idx])
        return total_distance(order, cities), order

    best_dist, best_order = get_loss(theta)

    for _ in range(epochs):
        # 估算數值梯度
        grad = [0.0] * n
        h = 1e-3
        base_loss, _ = get_loss(theta)

        for i in range(n):
            theta_step = theta[:]
            theta_step[i] += h
            loss_step, _ = get_loss(theta_step)
            grad[i] = (loss_step - base_loss) / h

        # 梯度更新
        for i in range(n):
            theta[i] -= lr * grad[i]

        cur_dist, cur_order = get_loss(theta)
        if cur_dist < best_dist:
            best_dist = cur_dist
            best_order = cur_order

    return best_order, best_dist


# -------------------------------------------------------------
# 5. 貪婪演算法 (Nearest Neighbor 最近鄰點法)
# -------------------------------------------------------------
def solve_greedy_nn(cities):
    """
    貪婪演算法：從起點開始，每一步都走向尚未造訪的最近城市
    """
    n = len(cities)
    unvisited = set(range(1, n))
    tour = [0]

    while unvisited:
        last = tour[-1]
        next_city = min(unvisited, key=lambda c: euclidean_dist(cities[last], cities[c]))
        tour.append(next_city)
        unvisited.remove(next_city)

    return tour, total_distance(tour, cities)


# -------------------------------------------------------------
# 主程式：測試並印出對比表格
# -------------------------------------------------------------
if __name__ == '__main__':
    random.seed(42)

    # 隨機產生 20 個城市的二維坐標 (x, y)
    num_cities = 20
    cities = {i: (random.uniform(0, 100), random.uniform(0, 100)) for i in range(num_cities)}

    print(f"=== 旅行推銷員問題 (TSP) 求解測試（城市數: {num_cities}）===\n")

    algorithms = [
        ("1. 改良法 (2-opt)", solve_2opt_improvement),
        ("2. 爬山演算法 (Hill Climbing)", solve_hill_climbing),
        ("3. 模擬退火法 (Simulated Annealing)", solve_simulated_annealing),
        ("4. 梯度下降法 (Gradient Descent)", solve_gradient_descent),
        ("5. 貪婪演算法 (Nearest Neighbor)", solve_greedy_nn),
    ]

    print(f"{'演算法':<32} | {'路徑長度 (Distance)':<18} | {'耗時 (秒)':<12}")
    print("-" * 68)

    for name, func in algorithms:
        start_time = time.perf_counter()
        tour, dist = func(cities)
        cost_time = time.perf_counter() - start_time
        print(f"{name:<32} | {dist:<18.3f} | {cost_time:<12.5f}")
