from typing import List, Union

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from ncafs import NCAFSR
from scipy.special import softmax
from sklearn.feature_selection import VarianceThreshold
from sklearn.utils import check_array

from . import get_seed
from .thirdparty import rank_aggregation as ra
from .thirdparty import skfeature
from .thirdparty.skfeature import ITFS
from .thirdparty.entropy_estimators import set_random_generator
from .utils import call_module_func


def variance_filter(X: np.ndarray, threshold: float = 1e-3, indices: bool = False):
    """
    Filter that removes all low-variance features.

    Args:
        X (array-like): feature matrix
        threshold (float): low variance threshold. Features with variance below that will be marked to be removed
        indices (bool): if True, the return value will be an array of integers, rather than a boolean mask
            (default False)

    Returns:
        array-like: If `indices` is True, returns the indices of the selected features. If False, then returns a boolean
        mask array, whose shape is `# input_features`.
    """
    var_thres = VarianceThreshold(threshold=threshold)
    var_thres.fit(X)
    return var_thres.get_support(indices=indices)


def correlation_filter(X: np.ndarray, threshold=0.95, indices: bool = False) -> np.ndarray:
    """
    Filter that removes highly-correlated features. Groups of features are formed from correlated pairs (transitive
    relation), and only the first element is selected.

    Args:
        X (array-like): feature matrix
        threshold (float): correlation coefficient threshold
        indices (bool): if True, the return value will be an array of integers, rather than a boolean mask
            (default False)

    Returns:
        array-like: If `indices` is True, returns the indices of the selected features. If False, then returns a boolean
        mask array, whose shape is `# input_features`.
    """
    n_feat = X.shape[1]
    selected = set(range(n_feat))
    corr = np.corrcoef(X.T, rowvar=True)
    np.fill_diagonal(corr, 0)
    corr_bin = corr > threshold
    corr_pairs = np.transpose(np.where(np.triu(corr_bin)))

    for p in corr_pairs:
        if p[0] in selected:
            selected.remove(p[1])
    selected = np.array(list(selected))
    selected.sort()

    if indices:
        return selected
    else:
        mask = np.zeros(n_feat, dtype=bool)
        mask[selected] = True
        return mask


def filtfeat(X: np.ndarray, Y: np.ndarray, method: str = 'NCA', max_n_features: int = 10,
             names: List[str] = None, n_jobs: int = 1, **kwargs) -> List[Union[int, str]]:
    """
    Filter feature selection. If Y has more than one column, than applies a rank aggregation method to the multi
    selections.

    Args:
        X (2D array-like): input features array
        Y (2D array-like): output performance array
        method (str): either Neighborhood Component Analysis (NCA, default) or Information Theoretic based (IT)
        max_n_features (int): max number if features to be selected (default 10)
        names (list): list with features names (default None). If provided, returns a list of selected features by name;
            otherwise, returns a list of indices (int)
        n_jobs (int): number of jobs to run in parallel. `-1` means using all processors. Defaults to 1
        **kwargs: optional paramters passed to the feature selection method

    Returns:
        list: Selected features
    """
    check_array(X, ensure_2d=True)
    check_array(Y, ensure_2d=True)

    n_instances, n_features = X.shape
    n_output = Y.shape[1]
    assert n_instances == Y.shape[0], "X and Y must have the same number of instances."

    FS = {'NCA': NCAFSR, 'IT': ITFS}[method]

    def run_fs(X_, y_, params):
        fs = FS(**params).fit(X_, y_)
        w_sort_idx = np.argsort(fs.weights_)[::-1]
        support = fs.support_[w_sort_idx]
        return list(map(str, w_sort_idx[support]))

    ranks = Parallel(n_jobs=n_jobs)(delayed(run_fs)(X, Y[:, i], kwargs) for i in range(n_output))

    agg = ra.RankAggregator()
    selected_list = agg.instant_runoff(ranks)[:max_n_features]
    selected_indices = list(map(int, selected_list))

    if names is None:
        return selected_indices
    else:
        return [names[i] for i in selected_indices]


@DeprecationWarning
def featfilt(df_metadata: pd.DataFrame, max_n_features=10, method='icap', var_filter=True, var_threshold=0, **kwargs):
    """
    Supervised feature filtering function. It involves three steps:

    1. Removes features whose variance is below ``var_threshold``, if ``var_filter`` is set true
    2. For each algo, it applies an information theoretic based method and select the most relevant features whose
       cumulative sum of score values is greater than or equal ``eta``
    3. Aggregation of the ranks obtained in (2), and selection of the top ``max_n_features``

    Input dataframe (``df_metadata``) should use Matilda standard: *feature_* prefix for measure columns, and *algo_*
    prefix for algorithm performances.

    According to `Matilda documentation <https://github.com/andremun/InstanceSpace>`_, it is recommended *using no
    more than 10 features as input to PILOT's optimal projection algorithm* (default ``max_n_features=10``).

    :param df_metadata: metadata dataframe.
    :type df_metadata: pandas.DataFrame
    :param max_n_features: maximum number of selected features at the end.
    :type max_n_features: int
    :param method: score method (see :py:mod:`pyhard.thirdparty.skfeature` module)
    :type method: str
    :param var_filter: enables variance filter
    :type var_filter: bool
    :param var_threshold: variance filter threshold
    :type var_threshold: float
    :param kwargs: specific for the used method
    :return: list of selected features, ``df_metadata`` with not selected features dropped
    """

    set_random_generator(get_seed())
    df_features = df_metadata.filter(regex='^feature_')
    df_algo = df_metadata.filter(regex='^algo_')
    orig_feat = df_features.columns.to_list()

    kwargs = {**kwargs, **{'n_selected_features': max_n_features}}

    if var_filter:
        mask = variance_filter(df_features.values, var_threshold)
        df_features = df_features.iloc[:, mask]

    agg = ra.RankAggregator()
    rank = []
    feat_list = df_features.columns.to_list()

    for algo in df_algo:
        args = [df_features.values, df_algo[[algo]].values]
        F, J, _ = call_module_func(skfeature, method, *args, **kwargs)
        idx = np.argsort(J)[::-1]
        assert (np.diff(J[idx]) <= 0).all()
        # rank.append(_select(F[idx], J[idx], eta=eta))
        rank.append(F)

    rank = [[feat_list[i] for i in l] for l in rank]
    selected_list = agg.instant_runoff(rank)[:max_n_features]
    blacklist = list(set(orig_feat).difference(set(selected_list)))

    return selected_list, df_metadata.drop(columns=blacklist)


@DeprecationWarning
def _select(F, J, how='cumsum', **kwargs):
    sorted_idx = np.argsort(J)[::-1]
    F_sorted = F[sorted_idx]

    if how == 'cumsum':
        if 'eta' in kwargs:
            eta = kwargs['eta']
        else:
            eta = 0.8
        s_value = softmax(J[sorted_idx])
        p = 0
        selected = []
        for i in range(len(s_value)):
            p += s_value[i]
            selected.append(F_sorted[i])
            if p >= eta:
                break
        return selected

    elif how == 'top':
        if 'N' in kwargs:
            N = kwargs['N']
        else:
            N = len(F) // 2
        return F_sorted[:N]
