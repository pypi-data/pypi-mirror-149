from dataclasses import dataclass

import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


@dataclass
class APRFSScores:
    # accuracy
    a: float
    # none
    p: list[float]
    r: list[float]
    f: list[float]
    s: list[float]
    # macro
    macro_p: float
    macro_r: float
    macro_f: float
    # mecro
    micro_p: float
    micro_r: float
    micro_f: float


def accuracy_precision_recall_fscore_support(
    y_true: np.ndarray,
    y_pred: np.ndarray,
):
    """TODO

    Args:
        y_true (np.ndarray):
        y_pred (np.ndarray):

    Returns:
        aprfs_scores (APRFSScores):
    """

    a = accuracy_score(y_true=y_true, y_pred=y_pred)
    p, r, f, s = precision_recall_fscore_support(y_true=y_true, y_pred=y_pred)
    macro_p, macro_r, macro_f, _ = precision_recall_fscore_support(
        y_true=y_true, y_pred=y_pred, average="macro"
    )
    micro_p, micro_r, micro_f, _ = precision_recall_fscore_support(
        y_true=y_true, y_pred=y_pred, average="micro"
    )

    aprfs_scores = APRFSScores(a, p, r, f, s, macro_p, macro_r, macro_f, micro_p, micro_r, micro_f)

    return aprfs_scores
