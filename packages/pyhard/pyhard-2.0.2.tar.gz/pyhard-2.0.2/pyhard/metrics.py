"""
Module that provides convenient functions for evaluating metrics per instance.
"""

from statistics import harmonic_mean

import numpy as np


def logloss(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-15) -> np.ndarray:
    """
    Calculates the log-loss metric value for each instance.

    Args:
        y_true (array-like): true class (one-hot-encoding)
        y_pred (array-like): predicted class probability
        eps (float): numeric lower tolerance

    Returns:
        array-like: log-loss values
    """
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.sum(y_true * np.log(y_pred), axis=1)


def brier(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Calculates the brier metric value for each instance.

    Args:
        y_true (array-like): true class (one-hot-encoding)
        y_pred (array-like): predicted class (one-hot-encoding)

    Returns:
        array-like: brier values
    """
    return np.sum((y_pred - y_true) ** 2, axis=1)


def absolute_error(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Calculates the absolute error value for each instance.

    Args:
        y_true (array-like): true value
        y_pred (array-like): predicted value

    Returns:
        array-like: absolute error values
    """
    return np.absolute(y_pred - y_true)


def squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
        Calculates the squared error value for each instance.

        Args:
            y_true (array-like): true value
            y_pred (array-like): predicted value

        Returns:
            array-like: squared error values
        """
    return (y_pred - y_true) ** 2


def loss_threshold(n_classes: int, metric: str = 'logloss', eps: float = 1e-3):
    """
    Calculates the maximum threshold below which the metric indicates a correct classification of the instance. It is
    equivalent to set the threshold to the metric value when all classes have almost the same predicted probability (the
    right class has a probability slightly higher - :math:`\epsilon`).

    Args:
        n_classes (int): number of classes
        metric (str): loss metric, either `log-loss` (default) or `brier`
        eps (float): slight increase in probability of the correct class

    Returns:
        float: metric threshold

    """
    assert n_classes >= 2

    p = np.ones((1, n_classes)) / n_classes
    p -= eps / n_classes
    p[0, 0] += eps
    np.testing.assert_almost_equal(p.sum(), 1)
    c = np.zeros((1, n_classes))
    c[0, 0] = 1

    if metric == 'logloss':
        lower_bound = logloss(np.array([[1, 0]]), np.array([[0.5, 0.5]]))[0]
        m = harmonic_mean([logloss(y_true=c, y_pred=p)[0], lower_bound])
    elif metric == 'brier':
        lower_bound = brier(np.array([[1, 0]]), np.array([[0.5, 0.5]]))[0]
        m = harmonic_mean([brier(y_true=c, y_pred=p)[0], lower_bound])
    else:
        raise ValueError(f"Unsupported metric '{metric}'.")

    return round(m, 4)
