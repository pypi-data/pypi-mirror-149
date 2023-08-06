def f_beta(p: float, r: float, beta: float = 1.0) -> float:
    """F-beta score

    Args:
        p (float): precision
        r (float): recall
        beta (float): beta

    Returns:
        f_beta_score (float): f-beta score
    """
    return (1 + beta**2) * p * r / (beta**2 * p + r)
