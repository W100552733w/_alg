import time
import sys

# ----------------------------
# 函數定義
# ----------------------------

# 方法 1：直接計算次方
def power2n_1(n):
    return 2**n

# 方法 2a：雙重遞迴（未優化）
def power2n_2a(n):
    if n == 0:
        return 1
    return power2n_2a(n - 1) + power2n_2a(n - 1)

# 方法 2b：單次遞迴
def power2n_2b(n):
    if n == 0:
        return 1
    return 2 * power2n_2b(n - 1)

# 方法 3：遞迴 + 查表法 (Memoization)
table = {}
def power2n_3(n):
    if n == 0:
        return 1
    if n in table:
        return table[n]
    
    # 依題目註解格式：雙重遞迴呼叫，但查表避免重複算
    table[n] = power2n_3(n - 1) + power2n_3(n - 1)
    return table[n]


# ----------------------------
# 效能測試主程式
# ----------------------------
if __name__ == '__main__':
    n = 100
    print(f"=== 測試 n = {n} ===")

    # 1. 測試方法 1
    start = time.perf_counter()
    ans1 = power2n_1(n)
    cost1 = time.perf_counter() - start
    print(f"方法 1  (2**n)            : 花費 {cost1:.8f} 秒")

    # 2. 測試方法 2b
    start = time.perf_counter()
    ans2b = power2n_2b(n)
    cost2b = time.perf_counter() - start
    print(f"方法 2b (2 * power(n-1))  : 花費 {cost2b:.8f} 秒")

    # 3. 測試方法 3
    start = time.perf_counter()
    ans3 = power2n_3(n)
    cost3 = time.perf_counter() - start
    print(f"方法 3  (遞迴+查表)        : 花費 {cost3:.8f} 秒")

    # 4. 測試方法 2a
    print("\n測試方法 2a (雙重遞迴)...")
    print("注意：當 n=100 時，需要進行 2^100 次計算，程式將無法在合理時間內完成！")
    print("以下改用 n = 30 示範其耗時：")
    
    start = time.perf_counter()
    ans2a_30 = power2n_2a(30)
    cost2a_30 = time.perf_counter() - start
    print(f"方法 2a (n = 30)          : 花費 {cost2a_30:.4f} 秒")
    print("如果 n=100，2^100 次運算大約需要上億億年，因此『出不來』。")
