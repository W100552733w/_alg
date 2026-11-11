import itertools
import re

def solve_sat_by_truth_table(formula_str):
    """
    使用系統性真值表列舉求解 SAT 問題。
    輸入布林運算式字串，例如：
      "(A or B) and (not A or C) and (not B or not C)"
    """
    # 提取所有變數名稱（過濾掉 Python 邏輯關鍵字）
    tokens = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', formula_str)
    keywords = {'and', 'or', 'not', 'True', 'False'}
    variables = sorted(list(set(t for t in tokens if t not in keywords)))
    
    n = len(variables)
    print(f"布林運算式: {formula_str}")
    print(f"變數列表: {variables} (共 {n} 個變數，總組合數: 2^{n} = {2**n})\n")
    
    # 印出真值表表頭
    header = " | ".join(variables) + " | Result"
    print(header)
    print("-" * len(header))
    
    satisfiable = False
    satisfying_assignments = []
    
    # 系統性列舉所有布林值組合 (0/1 或 True/False)
    for combination in itertools.product([False, True], repeat=n):
        # 建立變數賦值字典
        assignment = dict(zip(variables, combination))
        
        # 評估運算式的值
        result = eval(formula_str, {}, assignment)
        
        # 印出當前列
        row_str = " | ".join(f"{int(assignment[v]):^len(v)}" if len(v) > 1 else str(int(assignment[v])) for v in variables)
        row_str += f" |   {int(result)}"
        print(row_str)
        
        if result:
            satisfiable = True
            satisfying_assignments.append(assignment)
            
    print("-" * len(header))
    if satisfiable:
        print(f"\n[可滿足 (SAT)] 共找到 {len(satisfying_assignments)} 組可滿足解：")
        for ans in satisfying_assignments:
            print("  ", {k: bool(v) for k, v in ans.items()})
    else:
        print("\n[不可滿足 (UNSAT)] 無任何賦值可使該運算式為 True。")

if __name__ == '__main__':
    # 測試範例 1：可滿足的 3-CNF 運算式
    print("================== 測試 1 (SAT) ==================")
    expr1 = "(A or B) and (not A or C) and (not B or not C)"
    solve_sat_by_truth_table(expr1)

    # 測試範例 2：矛盾式（不可滿足）
    print("\n================== 測試 2 (UNSAT) ==================")
    expr2 = "(A) and (not A)"
    solve_sat_by_truth_table(expr2)
