from scipy.cluster import hierarchy
from multiprocessing import Pool
import numpy as np


def agglomerative_clustering(series_list, distance_fn, method='single', pool_size=1):
    """ Hierarchical clustering for time-series.

    Parameters
    ----------
    series_list: list, ndarray
        list of ndarray of shape=(sz, d)
        ndarray of shape=(n_ts, sz, d)
        Time series dataset.

    distance_fn: callable
        distance function to compute the pairwise distance between timeseries.

    method: str
        Which linkage criterion to use for agglomerative clustering.

    pool_size: int
        The size of multiprocessing pool to run distance matrix computations in parallel.

    Returns
    -------
    labels : array of shape (n_ts,)
        Index of the cluster each sample belongs to.
    """
    n = len(series_list)
    distance_mat = np.zeros(n * (n - 1) // 2)
    args = []
    idx_mapping = {}
    idx_counter = 0
    for i in range(n):
        for j in range(i + 1, n):
            args.append((series_list[i], series_list[j],))
            idx_mapping[idx_counter] = n * i + j - ((i + 2) * (i + 1)) // 2
            idx_counter += 1
    pool = Pool(pool_size)
    distance_arr = pool.starmap(distance_fn, args)
    for i, val in enumerate(distance_arr):
        distance_mat[idx_mapping[i]] = val

    linkage_matrix = hierarchy.linkage(distance_mat, method)
    clustering_labels = hierarchy.fcluster(linkage_matrix, 2, criterion='maxclust')

    return clustering_labels


