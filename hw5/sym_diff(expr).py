def sym_diff(expr, var='x'):
    """
    符號微分：expr 支援常數(int/float)、變數(str)、二元運算 tuple ('+', u, v) 等
    """
    # 1. 常數規則
    if isinstance(expr, (int, float)):
        return 0
    
    # 2. 變數規則
    if isinstance(expr, str):
        return 1 if expr == var else 0

    # 3. 複合運算式：(運算子, 左子式, 右子式)
    op, u, v = expr[0], expr[1], expr[2]

    if op == '+':
        # (u + v)' = u' + v'
        return ('+', sym_diff(u, var), sym_diff(v, var))
    
    elif op == '-':
        # (u - v)' = u' - v'
        return ('-', sym_diff(u, var), sym_diff(v, var))
    
    elif op == '*':
        # 積的微分：(u * v)' = u' * v + u * v'
        return ('+', ('*', sym_diff(u, var), v), ('*', u, sym_diff(v, var)))
    
    elif op == '**':
        # 冪次微分（假設次方 v 為常數）：(u^v)' = v * (u^(v-1)) * u'
        return ('*', ('*', v, ('**', u, v - 1)), sym_diff(u, var))
    
    else:
        raise ValueError(f"未支援的運算子: {op}")

# 範例測試：微分 f(x) = x^2 + 3*x + 5
# 表示為 ('+', ('+', ('**', 'x', 2), ('*', 3, 'x')), 5)
if __name__ == '__main__':
    f = ('+', ('+', ('**', 'x', 2), ('*', 3, 'x')), 5)
    df = sym_diff(f, 'x')
    print("符號微分結果 (AST):", df)
    # 結果對應：(2 * x^1 * 1) + (0 * x + 3 * 1) + 0 = 2x + 3
