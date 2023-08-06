import numpy as np


def cat_and_zero_pad_arrays_with_different_shape_zero(tensors: list[np.ndarray]) -> np.ndarray:
    """

    Args:
        tensors (list[np.ndarray]):

    Returns:
    """
    max_length = 0

    for tensor in tensors:
        max_length = max(max_length, tensor.shape[0])

    cat = np.zeros((len(tensors), max_length, *tensors[0].shape[1:]))

    for i, tensor in enumerate(tensors):
        cat[i, : tensor.shape[0]] += tensor

    return cat
