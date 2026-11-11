"""
Lambda Calculus 解譯器 (具有逐步詳細計算過程輸出)
支援語法元素：
- 變數 (Variable): x, y, a
- 抽象 (Abstraction / 函數): \x. M 或 λx. M
- 應用 (Application / 呼叫): (M N)
"""

# -------------------------------------------------------------
# 1. 語法樹節點定義 (AST Node Definitions)
# -------------------------------------------------------------
class Term:
    def free_vars(self):
        raise NotImplementedError

    def substitute(self, var, replacement):
        raise NotImplementedError

class Var(Term):
    def __init__(self, name):
        self.name = name

    def free_vars(self):
        return {self.name}

    def substitute(self, var, replacement):
        return replacement if self.name == var else self

    def __str__(self):
        return self.name

class Abs(Term):
    def __init__(self, param, body):
        self.param = param
        self.body = body

    def free_vars(self):
        return self.body.free_vars() - {self.param}

    def substitute(self, var, replacement):
        if self.param == var:
            return self
        
        # 避免變數捕捉：若參數名稱出現在替換對象的自由變數中，進行 α-轉換 (重新命名參數)
        if self.param in replacement.free_vars():
            new_param = fresh_var(self.body.free_vars() | replacement.free_vars() | {var})
            new_body = self.body.substitute(self.param, Var(new_param))
            return Abs(new_param, new_body.substitute(var, replacement))
        
        return Abs(self.param, self.body.substitute(var, replacement))

    def __str__(self):
        return f"(λ{self.param}.{self.body})"

class App(Term):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def free_vars(self):
        return self.left.free_vars() | self.right.free_vars()

    def substitute(self, var, replacement):
        return App(self.left.substitute(var, replacement),
                   self.right.substitute(var, replacement))

    def __str__(self):
        return f"({self.left} {self.right})"

_var_counter = 0
def fresh_var(used):
    """產生一個未被使用過的唯一變數名稱 (α-conversion)"""
    global _var_counter
    while True:
        _var_counter += 1
        name = f"v{_var_counter}"
        if name not in used:
            return name

# -------------------------------------------------------------
# 2. 評估引擎：最左最外優先 (Normal Order Reduction)
# -------------------------------------------------------------
def reduce_one_step(term):
    """
    執行單一步驟的 β-歸約 (One-step Beta-reduction)。
    若已是最簡形式（無法再化簡），回傳 None。
    """
    if isinstance(term, Var):
        return None

    if isinstance(term, Abs):
        new_body = reduce_one_step(term.body)
        if new_body is not None:
            return Abs(term.param, new_body)
        return None

    if isinstance(term, App):
        # 核心歸約規則：(λx. M) N  ==>  M [x := N]
        if isinstance(term.left, Abs):
            return term.left.body.substitute(term.left.param, term.right)
        
        # 先嘗試化簡左側
        new_left = reduce_one_step(term.left)
        if new_left is not None:
            return App(new_left, term.right)
        
        # 左側無法化簡時，再化簡右側
        new_right = reduce_one_step(term.right)
        if new_right is not None:
            return App(term.left, new_right)

    return None

def evaluate(term, max_steps=100):
    """
    逐步求值並印出完整的計算過程
    """
    print("=" * 60)
    print(f"初始運算式 : {term}")
    print("-" * 60)
    
    current = term
    step = 0
    while step < max_steps:
        next_term = reduce_one_step(current)
        if next_term is None:
            print(f"\n[化簡完成] 最終正規形式 (Normal Form): {current}")
            print(f"總計算步數: {step} 步")
            return current
        step += 1
        print(f"步驟 {step:02d} => {next_term}")
        current = next_term

    print(f"\n[警告] 超過最大步數限制 ({max_steps})，可能為非終止運算式 (如 Ω combinator)！")
    return current


# -------------------------------------------------------------
# 3. 測試範例 (Church 編碼與邏輯運算)
# -------------------------------------------------------------
if __name__ == '__main__':
    # 經典組合子定義
    I = Abs('x', Var('x'))                          # Identity: λx. x
    TRUE = Abs('t', Abs('f', Var('t')))            # True: λt. λf. t
    FALSE = Abs('t', Abs('f', Var('f')))           # False: λt. λf. f
    NOT = Abs('b', App(App(Var('b'), FALSE), TRUE)) # NOT: λb. b False True
    
    # Church 數字
    ZERO = Abs('f', Abs('x', Var('x')))            # 0: λf. λx. x
    ONE = Abs('f', Abs('x', App(Var('f'), Var('x')))) # 1: λf. λx. f x
    SUCC = Abs('n', Abs('f', Abs('x', App(Var('f'), App(App(Var('n'), Var('f')), Var('x')))))) # 後繼函式

    # 範例 1：恆等函式應用 (I a)
    print("\n【範例 1】恆等式應用：(λx.x) a")
    evaluate(App(I, Var('a')))

    # 範例 2：布林邏輯運算 NOT TRUE
    print("\n【範例 2】布林否定運算：NOT TRUE  => 應求出 FALSE")
    evaluate(App(NOT, TRUE))

    # 範例 3：Church 數加 1 運算 (SUCC 0) => 應求出 1
    print("\n【範例 3】後繼數計算：SUCC 0  => 應求出 1")
    evaluate(App(SUCC, ZERO))
