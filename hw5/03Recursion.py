def my_map(func, lst):
    """自製遞迴版 map"""
    if not lst:
        return []
    return [func(lst[0])] + my_map(func, lst[1:])

def my_filter(predicate, lst):
    """自製遞迴版 filter"""
    if not lst:
        return []
    head, tail = lst[0], lst[1:]
    rest = my_filter(predicate, tail)
    return [head] + rest if predicate(head) else rest

def my_reduce(func, lst, initial=None):
    """自製遞迴版 reduce"""
    if not lst:
        return initial
    if initial is None:
        return my_reduce(func, lst[1:], lst[0])
    return my_reduce(func, lst[1:], func(initial, lst[0]))
