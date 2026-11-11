def hanoi_iterative(n, source, target, auxiliary):
    """
    使用 Stack 模擬遞迴展開，禁止使用函式遞迴
    """
    # 堆疊元素儲存 (盤子數, 起點, 目標, 輔助)
    stack = [(n, source, target, auxiliary)]
    
    while stack:
        curr_n, s, t, a = stack.pop()
        if curr_n == 1:
            print(f"盤子 1 : {s} -> {t}")
        else:
            # 由於 Stack 是 LIFO（後進先出），放入順序需反過來：
            # 3. 最後執行的步驟先壓棧：(n-1, a, t, s)
            stack.append((curr_n - 1, a, t, s))
            # 2. 中間搬動最大盤子：(1, s, t, a)
            stack.append((1, s, t, a))
            # 1. 最先執行的步驟最後壓棧：(n-1, s, a, t)
            stack.append((curr_n - 1, s, a, t))
