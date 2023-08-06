def fibonacci(inp: int) -> list[int]:
    """Fibonacci

    Args:
        inp (int): TODO

    Returns:
        fibonacci_numbers (list[int])
    """
    if inp < 0:
        raise ValueError

    ret = [0 for _ in range(inp + 1)]

    if inp == 0:
        return ret

    ret[1] = 1

    for i in range(2, inp + 1):
        ret[i] = ret[i - 1] + ret[i - 2]

    return ret
