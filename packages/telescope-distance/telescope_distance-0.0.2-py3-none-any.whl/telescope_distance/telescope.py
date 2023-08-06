import numpy as np
import math
from sklearn.preprocessing import StandardScaler


class TelescopeDistance:
    """Employee class is used to hold employee object data.

        Methods:
            __init__(self, emp_id, emp_name)
            print()
    """
    def __init__(self, clf, weights, max_k=None):
        """TelescopeDistance Class Constructor to initialize the object.

            Input Arguments:
                clf : Class constructor
                    a classifier class constructor for the estimation of the inner summand
                weights : list, ndarray, callable
                    a list or a generator function of the sequence of the weights used in the telescope distance
                    formulation.
                max_k : int, optional
                    the maximum depth of the telescope distance infinite summation,
                    default value will be set as logarithm of the shortest time-series
        """

        assert isinstance(weights, (list, np.ndarray)) or callable(
            weights), "weights should be a list/array or a function"

        self.clf = clf
        self.weights = weights
        self.max_k = max_k

    @staticmethod
    def reshape_features(x, sub_length, overlapping=False):
        """ Returns all the subsequences with length k of the timeseries x.
            In case of multidimensional timeseries it returns the flattened version of subsequences.

            Parameters
            ----------
            x : ndarray
                array containing the timeseries sample path.
            sub_length : int
                the length of the subsequences
            overlapping : bool, optional
                a flag used to determine the overlap condition of the subsequences
            Returns
            -------
            ndarray
                a 2D array containing flattened subsequences
            """
        n = x.shape[0]
        subseq = [(x[i: i + sub_length, :]).flatten() for i in range(n - sub_length + 1)] if overlapping \
            else [(x[i * sub_length: (i + 1) * sub_length, :]).flatten() for i in range(0, (n // sub_length))]
        return np.array(subseq)

    def _subseq_distance(self, X, Y):
        """Returns the value of telescope distance's inner summand.

        Parameters
        ----------
        X : ndarray
            a 2D array containing first timeseries subsequences
        Y : ndarray
            a 2D array containing second timeseries subsequences
        Returns
        -------
        float
            a value as a distance between two timeseries marginals
        """
        data = np.concatenate((X, Y))
        n = X.shape[0]
        m = Y.shape[0]
        labels = np.array([0] * X.shape[0] + [1] * Y.shape[0])
        data = StandardScaler().fit_transform(data)
        clf = self.clf()
        clf.fit(data, labels)
        prediction = clf.predict(data)
        Tx = prediction[labels == 0].sum()
        Ty = prediction[labels == 1].sum()
        return math.fabs(Tx / n - Ty / m)

    def distance(self, x, y):
        """ This method calculates the empirical estimate of telescope distance between the probability distribution of
        the generating processes associated with time-series x and y.

        Parameters
        ----------
        x : ndarray
            a 2D array that represents the first time-series
        y : ndarray
            a 2D array that represents the second time-series
        Returns
        -------
        float
            the empirical estimate of telescope distance
        """
        n = min(x.shape[0], y.shape[0])
        max_k = int(math.log(n)) if self.max_k is None else self.max_k

        weights = np.array([self.weights(i) for i in range(1, max_k)]) if callable(self.weights) else self.weights

        dist = np.array(
            [self._subseq_distance(self.reshape_features(x, k), self.reshape_features(y, k))
             for k in range(1, max_k)
             ])
        return dist.dot(weights)




