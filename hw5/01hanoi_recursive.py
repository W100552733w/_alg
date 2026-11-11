def hanoi_recursive(n, source, target, auxiliary):
    """
    將 n 個盤子從 source 藉由 auxiliary 搬移到 target
    """
    if n == 1:
        print(f"盤子 1 : {source} -> {target}")
        return
    # 1. 先將前 n-1 個盤子從 source 搬到 auxiliary
    hanoi_recursive(n - 1, source, auxiliary, target)
    # 2. 將第 n 個盤子從 source 搬到 target
    print(f"盤子 {n} : {source} -> {target}")
    # 3. 最後將 n-1 個盤子從 auxiliary 搬到 target
    hanoi_recursive(n - 1, auxiliary, target, source)
