"""
作業：搜尋演算法綜合實作
姓名：葉俊成  學號：111210544
包含題目：
1. 老鼠走迷宮 (DFS)
2. 狼羊甘藍菜過河 (BFS)
3. 八皇后問題 (DFS / 回溯法)
4. NPC 搜尋玩家 (A* 演算法)
5. IC 設計電路繞線 (Lee Algorithm / 迷宮擴展繞線法)
"""

import collections
import heapq


# =============================================================
# 1. 老鼠走迷宮問題 (DFS)
# =============================================================
def solve_maze_dfs(maze, start, end):
    """0 代表可通行道路，1 代表障礙牆壁"""
    rows, cols = len(maze), len(maze[0])
    visited = set()
    path = []

    def dfs(r, c):
        if (r, c) == end:
            path.append((r, c))
            return True

        visited.add((r, c))
        path.append((r, c))

        # 上、右、下、左四個方向
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and maze[nr][nc] == 0
                and (nr, nc) not in visited
            ):
                if dfs(nr, nc):
                    return True

        path.pop()  # 回溯
        return False

    if dfs(start[0], start[1]):
        return path
    return None


# =============================================================
# 2. 狼羊甘藍菜過河問題 (BFS)
# =============================================================
def solve_river_crossing_bfs():
    """狀態表示：(人, 狼, 羊, 菜)，0 代表此岸，1 代表彼岸"""
    start_state = (0, 0, 0, 0)
    goal_state = (1, 1, 1, 1)

    def is_valid(state):
        farmer, wolf, sheep, cabbage = state
        # 當農夫不在時，狼和羊不能在一起
        if wolf == sheep and farmer != wolf:
            return False
        # 當農夫不在時，羊和菜不能在一起
        if sheep == cabbage and farmer != sheep:
            return False
        return True

    queue = collections.deque([[start_state]])
    visited = {start_state}

    item_names = ['獨自過河', '帶狼', '帶羊', '帶甘藍菜']

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == goal_state:
            return path

        farmer, wolf, sheep, cabbage = current
        next_farmer = 1 - farmer

        # 可能的動作：農夫自己過河，或帶狼、羊、甘藍菜（必須在同側才能帶）
        candidates = []
        # 1. 農夫單獨過河
        candidates.append((next_farmer, wolf, sheep, cabbage))
        # 2. 帶狼
        if wolf == farmer:
            candidates.append((next_farmer, next_farmer, sheep, cabbage))
        # 3. 帶羊
        if sheep == farmer:
            candidates.append((next_farmer, wolf, next_farmer, cabbage))
        # 4. 帶菜
        if cabbage == farmer:
            candidates.append((next_farmer, wolf, sheep, next_farmer))

        for nxt in candidates:
            if is_valid(nxt) and nxt not in visited:
                visited.add(nxt)
                queue.append(path + [nxt])
    return None


# =============================================================
# 3. 八皇后問題 (DFS / 回溯法)
# =============================================================
def solve_n_queens_dfs(n=8):
    """
    使用一維陣列 queens 表示狀態，queens[r] = c 代表第 r 列的皇后放在第 c 行
    """
    solutions = []

    def is_safe(queens, row, col):
        for r in range(row):
            c = queens[r]
            # 同行或是同一對角線衝突
            if c == col or abs(c - col) == abs(r - row):
                return False
        return True

    def dfs(row, current_board):
        if row == n:
            solutions.append(list(current_board))
            return

        for col in range(n):
            if is_safe(current_board, row, col):
                current_board.append(col)
                dfs(row + 1, current_board)
                current_board.pop()  # 回溯

    dfs(0, [])
    return solutions


# =============================================================
# 4. NPC 搜尋玩家問題 (A* 演算法)
# =============================================================
def solve_npc_path_astar(grid, start, goal):
    """
    使用曼哈頓距離作為啟發式函數 h(n)
    """
    rows, cols = len(grid), len(grid[0])

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # 優先佇列儲存：(f_score, g_score, (r, c))
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))

    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, cur_g, current = heapq.heappop(open_set)

        if current == goal:
            # 重建路徑
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        r, c = current
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (r + dr, c + dc)
            nr, nc = neighbor
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                tentative_g = cur_g + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, tentative_g, neighbor))

    return None


# =============================================================
# 5. IC 設計電路繞線問題 (Lee Algorithm / 迷宮繞線法)
# =============================================================
def solve_ic_routing_lee(grid, pin_a, pin_b):
    """
    Lee Algorithm：廣度優先波前擴展（Wavefront Expansion），保證能找到最短繞線路徑
    -1 代表障礙金屬層，0 代表未繞線自由空間
    """
    rows, cols = len(grid), len(grid[0])
    board = [row[:] for row in grid]

    # BFS 波前擴展
    queue = collections.deque([pin_a])
    board[pin_a[0]][pin_a[1]] = 1  # 步數標記起點為 1
    found = False

    while queue:
        r, c = queue.popleft()
        if (r, c) == pin_b:
            found = True
            break

        step = board[r][c]
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                # 只有空白處 (0) 才能擴展
                if board[nr][nc] == 0:
                    board[nr][nc] = step + 1
                    queue.append((nr, nc))

    if not found:
        return None

    # 回溯最短繞線
    wire_path = [pin_b]
    cur = pin_b
    while cur != pin_a:
        r, c = cur
        cur_step = board[r][c]
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and board[nr][nc] == cur_step - 1
            ):
                wire_path.append((nr, nc))
                cur = (nr, nc)
                break

    return wire_path[::-1]


# =============================================================
# 測試展示主程式
# =============================================================
if __name__ == '__main__':
    print('=== 1. 老鼠走迷宮 (DFS) ===')
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    path_dfs = solve_maze_dfs(maze, (0, 0), (4, 4))
    print(f'走訪路徑: {path_dfs}\n')

    print('=== 2. 狼羊甘藍菜過河問題 (BFS) ===')
    path_river = solve_river_crossing_bfs()
    print(f'最少過河步驟數: {len(path_river) - 1} 步')
    for idx, state in enumerate(path_river):
        f, w, s, c = state
        print(f'步驟 {idx}: 人={f}, 狼={w}, 羊={s}, 菜={c}')

    print('\n=== 3. 八皇后問題 (DFS) ===')
    queen_solutions = solve_n_queens_dfs(8)
    print(f'八皇后全部合法解總數: {len(queen_solutions)} 組')
    print(f'第一組解 (各列之行座標): {queen_solutions[0]}\n')

    print('=== 4. NPC 搜尋玩家問題 (A*) ===')
    game_map = [
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
    ]
    npc_start, player_pos = (0, 0), (4, 0)
    astar_path = solve_npc_path_astar(game_map, npc_start, player_pos)
    print(f'NPC 到達玩家的最短路徑: {astar_path}\n')

    print('=== 5. IC 設計電路繞線問題 (Lee Algorithm) ===')
    chip_grid = [
        [0, 0, 0, 0, 0],
        [0, -1, -1, -1, 0],
        [0, 0, 0, -1, 0],
        [0, -1, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    pin_1, pin_2 = (0, 1), (4, 3)
    wire = solve_ic_routing_lee(chip_grid, pin_1, pin_2)
    print(f'金屬繞線路徑: {wire}')
