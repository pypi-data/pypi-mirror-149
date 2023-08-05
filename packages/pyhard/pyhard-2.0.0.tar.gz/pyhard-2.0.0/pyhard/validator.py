"""
Module that provides convenient functions for validating an input dataset.
"""

import pandas as pd
from pandas.api.types import is_integer_dtype, is_numeric_dtype, is_object_dtype  # noqa


__all__ = [
    'is_target_dtype_valid',
    'are_classes_balanced',
    'has_no_missing_values',
    'are_features_numeric'
]


def is_target_dtype_valid(problem: str, target: pd.Series):
    """
    Asserts the response variable (target) dtype is correct.

    Args:
        problem (str): type of learning problem. Either 'classification' or 'regression'
        target (pandas.Series): series of target values

    Returns:
        None

    Raises:
        AssertionError: If dtype is not the expected.

    """
    if problem == 'classification':
        assert is_integer_dtype(target) or is_object_dtype(target), \
            "Target column dtype must be either integer or object (string)."
    elif problem == 'regression':
        assert is_numeric_dtype(target), "Target column dtype must be numeric."


def are_classes_balanced(target: pd.Series, ir_tol: float = 1.5):
    """
    Checks whether the classes are balanced, based on the Imbalance Ratio (IR), which is the proportion of the number
    of samples in the majority class over the number of samples in the minority class.

    Args:
        target (pandas.Series): series of target values
        ir_tol (float): IR tolerance. Imbalance occurs when IR > ir_tol

    Returns:
        bool: True if classes are balanced, False otherwise

    """
    class_count = target.groupby(target).count()
    return (class_count.max() / class_count.min()) <= ir_tol


def has_no_missing_values(data: pd.DataFrame):
    """
    Asserts that there are no missing data present.

    Args:
        data (pandas.DataFrame): input data

    Returns:
        None

    Raises:
        AssertionError: If null values are encountered.

    """
    assert not data.isnull().any(None), "Data should not contain NaN values."  # noqa


def are_features_numeric(df_feat: pd.DataFrame):
    """
    Asserts that all features are numeric.

    Args:
        df_feat (pandas.DataFrame): array of features

    Returns:
        None

    Raises:
        AssertionError: If any feature is not numeric.

    """
    assert all(map(lambda col: is_numeric_dtype(df_feat[col]), df_feat)), "All features must be numeric."
