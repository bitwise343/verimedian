# (c) Justin Beaurone
from . import np
from . import type_array
from . import P


def verifiable_median(x: np.ndarray) -> (np.ndarray, np.ndarray, int):
    """Sort an array x into a sorted array y, and find a square
    permutation matrix A such that Ax = y. The median value is the
    center of y. The array x must be of odd size and contain only
    integers.

    inputs:
    x         the unsorted array

    outputs:
    A         the permutation matrix s.t. Ax = y
    m         the median of x
    """
    # x must be a numpy ndarray
    if (tx := type(x)) != np.ndarray:
        raise ValueError(f"type(x): {tx} is invalid. Expected np.ndarray.")
    # x must be 1 dimensional
    elif (shx := x.shape) != (sx := x.size,):
        raise ValueError(f"shape(x): {shx} is invalid. Expected 1 dimensional.")
    # x must be odd-length
    elif sx % 2 != 1:
        raise ValueError(f"len(x): {sx} is invalid. Expected odd length.")
    # all elements in x must be Python integers
    elif not np.all(type_array(x) == int):
        raise ValueError(f"Type of elements `x`: ({td}) is invalid. " \
                         + "Expected all elements to be of type `int`.")
    # all elements in x must be less than P
    elif not np.all(x <= P):
        raise ValueError(f"All elements in `x` must be less than P.")

    # Sort an array of tuples containing (value, index) for each element in x.
    sorter = np.array([(v, i) for v, i in zip(x, np.arange(sx))],
                      dtype=[("value", object), ("original_index", int)])
    sorter.sort(order=["value", "original_index"])

    # Set column `original_index` of each row of A to 1
    A = np.zeros((sx, sx), dtype=int)
    for i in range(sx):
        A[i][sorter["original_index"][i]] = 1

    return A, sorter["value"][int(sx/2)]