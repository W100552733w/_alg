def bubble_pass(lst):
    """
    單趟泡沫排序（內層）：將較大元素一路往右浮動
    純遞迴實作，不使用迴圈
    """
    if len(lst) <= 1:
        return lst
    a, b = lst[0], lst[1]
    if a > b:
        # 交換後繼續對後面遞迴處理
        return [b] + bubble_pass([a] + lst[2:])
    else:
        return [a] + bubble_pass([b] + lst[2:])

def bubble_sort_functional(lst, n=None):
    """
    外層遞迴：重複執行 n 次 bubble_pass
    """
    if n is None:
        n = len(lst)
    if n <= 1:
        return lst
    # 每做一趟，最大的值會沉到最後，接著遞迴排序前 n-1 輪
    return bubble_sort_functional(bubble_pass(lst), n - 1)


# ---------------- 測試展示 ----------------
if __name__ == '__main__':
    data = [64, 34, 25, 12, 22, 11, 90]
    print("原始資料:", data)
    
    # 測試自製函數
    print("my_map (x*2):", my_map(lambda x: x * 2, [1, 2, 3]))
    print("my_filter (偶數):", my_filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))
    print("my_reduce (加總):", my_reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0))
    
    # 測試無迴圈泡沫排序
    sorted_data = bubble_sort_functional(data)
    print("無迴圈泡沫排序結果:", sorted_data)
