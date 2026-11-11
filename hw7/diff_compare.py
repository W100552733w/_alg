"""
作業：文字差異比對 (diff)
實作兩種演算法：
1. 動態規劃：最長公共子序列 (LCS - Longest Common Subsequence)
2. 非動態規劃：Myers 差異演算法 (Git 預設採用的貪婪 BFS 最短路徑法)
"""

import time


# =============================================================
# 方法 1：動態規劃 (LCS - Longest Common Subsequence)
# =============================================================
def diff_lcs(lines_a, lines_b):
    """使用 2D DP 表格計算 LCS，並回溯輸出差異"""
    n, m = len(lines_a), len(lines_b)

    # 1. 建立 DP 表格記錄長度
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if lines_a[i - 1] == lines_b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # 2. 回溯尋找差異操作序列
    i, j = n, m
    diff_result = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and lines_a[i - 1] == lines_b[j - 1]:
            diff_result.append(f'  {lines_a[i-1]}')
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            diff_result.append(f'+ {lines_b[j-1]}')
            j -= 1
        else:
            diff_result.append(f'- {lines_a[i-1]}')
            i -= 1

    diff_result.reverse()
    return diff_result


# =============================================================
# 方法 2：非動態規劃 (Myers Diff Algorithm - 貪婪 BFS 搜尋)
# =============================================================
def diff_myers(lines_a, lines_b):
    """Myers 差異演算法：在編輯圖 (Edit Graph) 上以 BFS 搜尋最少編輯步數 D"""
    n, m = len(lines_a), len(lines_b)
    max_d = n + m

    # v[k] 記錄對角線 k = x - y 所能到達的最大 x 座標
    v = {1: 0}
    trace = []

    for d in range(max_d + 1):
        trace.append(v.copy())
        # 在第 d 步，對角線 k 的範圍在 -d 到 d 之間，步長為 2
        for k in range(-d, d + 1, 2):
            # 決定從上方 (k+1) 往下走，還是從左方 (k-1) 往右走
            if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                x = v[k + 1]  # 往下移動 (插入)
            else:
                x = v[k - 1] + 1  # 往右移動 (刪除)

            y = x - k

            # 貪婪走「對角線」(吻合字元不需要消耗編輯距離)
            while x < n and y < m and lines_a[x] == lines_b[y]:
                x += 1
                y += 1

            v[k] = x

            # 到達終點 (N, M)
            if x >= n and y >= m:
                return _backtrack_myers(lines_a, lines_b, trace, d)
    return []


def _backtrack_myers(lines_a, lines_b, trace, d):
    """沿著 Myers 搜尋軌跡回溯產生 diff 標記"""
    x, y = len(lines_a), len(lines_b)
    diff_result = []

    for step in range(d, 0, -1):
        v = trace[step]
        k = x - y

        if k == -step or (
            k != step and v.get(k - 1, -1) < v.get(k + 1, -1)
        ):
            prev_k = k + 1
        else:
            prev_k = k - 1

        prev_x = v[prev_k]
        prev_y = prev_x - prev_k

        # 走對角線（相同內容）
        while x > prev_x and y > prev_y:
            diff_result.append(f'  {lines_a[x-1]}')
            x -= 1
            y -= 1

        # 刪除或新增
        if x > prev_x:
            diff_result.append(f'- {lines_a[x-1]}')
            x -= 1
        elif y > prev_y:
            diff_result.append(f'+ {lines_b[y-1]}')
            y -= 1

    while x > 0 and y > 0:
        diff_result.append(f'  {lines_a[x-1]}')
        x -= 1
        y -= 1

    diff_result.reverse()
    return diff_result


# =============================================================
# 效能比對測試主程式
# =============================================================
if __name__ == '__main__':
    doc_a = [
        'apple',
        'banana',
        'cat',
        'dog',
        'egg',
        'fox',
        'grape',
        'horse',
        'ice',
    ]
    doc_b = [
        'apple',
        'banana',
        'cheetah',
        'dog',
        'elephant',
        'fox',
        'grape',
        'ice',
    ]

    print('=== 原始文件 A ===')
    print(doc_a)
    print('\n=== 修改後文件 B ===')
    print(doc_b)

    # 1. 測試動態規劃 (LCS)
    t0 = time.perf_counter()
    diff_1 = diff_lcs(doc_a, doc_b)
    t_lcs = time.perf_counter() - t0

    # 2. 測試 Myers 演算法
    t0 = time.perf_counter()
    diff_2 = diff_myers(doc_a, doc_b)
    t_myers = time.perf_counter() - t0

    print('\n' + '=' * 40)
    print(f'【LCS (動態規劃)】耗時: {t_lcs:.6f} 秒')
    print('=' * 40)
    for line in diff_1:
        print(line)

    print('\n' + '=' * 40)
    print(f'【Myers (非動態規劃)】耗時: {t_myers:.6f} 秒')
    print('=' * 40)
    for line in diff_2:
        print(line)
