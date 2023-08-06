import numpy as np


def standard_error(data: np.ndarray) -> float:
    """
    :param data: numpy array to be evaluated
    :type data: np.ndarray
    :return: error of the mean of data

    Calculate standard error of the mean of a numpy array
    """
    assert isinstance(data, np.ndarray), 'Wrong data type'
    assert len(data.shape) == 1, 'Data must be 1 dimensional'

    error = np.std(data, ddof=1) / np.sqrt(np.size(data))
    return error
