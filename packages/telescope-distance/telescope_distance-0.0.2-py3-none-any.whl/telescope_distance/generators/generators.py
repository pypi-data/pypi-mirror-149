import numpy as np


def generate_irrational_rotation_series(alpha, series_length, dist1, dist2):
    """
    Irrational rotation time-series generator

    Generates a time-series of size series_length.
    Generated time-series follows the model:
    .. math::
        r[t] = (r[t - 1] + alpha) mod 1
        ts[t] = a_1 * I(r[t] < 0.5) + a_2 * I(r[t] >= 0.5)
    where :math:`a_1` and :math:`a_2` are drawn from dist1 and dist2, respectively.

    Parameters
    ----------
    alpha: float
        Irrational number that characterize the process
    series_length: int
        Length of time series (number of time instants).
    dist1: int, scipy.rv_generic
        Distribution associated to state 1 from which sample path elements with hidden state 1 are drawn. If an integer
        is given, it assigns this value to elements of sample path with state 1
    dist2: int, scipy.rv_generic
        Distribution associated to state 2 from which sample path elements with hidden state 2 are drawn.If an integer
        is given, it assigns this value to elements of sample path with state 1

    Returns
    -------
    numpy.ndarray
        An Irrational rotation time_series
    """

    def _draw_x(r, _dist1, _dist2):
        if r < 0.5:
            return _dist1.rvs() if type(_dist1) is not int else _dist1
        else:
            return _dist2.rvs() if type(_dist2) is not int else _dist2

    r0 = np.random.uniform()
    x = [_draw_x(r0, dist1, dist2)]
    for i in range(series_length - 1):
        r0 = (r0 + alpha) % 1
        x.append(_draw_x(r0, dist1, dist2))
    return np.array(x).reshape((series_length, -1))


class MarkovChain:
    """ Discrete-time Markov chain

    Parameters
    ----------
    n_states : int
        Size of the finite state space.

    order : int (default : 1)
        Order of Markov chain memory

    transition_mat : ndarray or None (default : None)
        Transition matrix associated to the extended state space

    Attributes
    ----------
    state : int
        Current state's number in the extended state space

    Methods
    -------
    get_state:
        Returns the current state of MC in the actual state space

    generate_sample_path:
        Returns a sample path from current state

    generate_hidden_markov_sample_path:
        Returns a sample path from an HMM with

    Class Methods
    -------------
    get_stationary_dist:
        Computes the stationary distribution of a given transition matrix

    generate_arbitrary_markovian_transition:
        Generates an arbitrary stationary transition matrix for a given state size and order

    """
    def __init__(self, n_states, order=1, transition_mat=None):

        self.number_of_states = n_states
        self.order = order

        # Set an arbitrary stationary Markov transition matrix, if None is given.
        if transition_mat is None:
            self.transition_matrix = MarkovChain.generate_arbitrary_markovian_transition(n_states, order)
        else:
            self.transition_matrix = transition_mat

        stationary_dist = MarkovChain.get_stationary_dist(self.transition_matrix)

        self.state = np.random.choice(self.transition_matrix.shape[0], p=stationary_dist)

    def get_state(self):
        return self.state % self.number_of_states

    def take_step(self):
        self.state = np.random.choice(self.transition_matrix.shape[0], p=self.transition_matrix[self.state, :])
        return self.get_state()

    def generate_sample_path(self, series_length):
        """ Generates a sample path

        Parameters
        ----------
        series_length : int
            Size of the sample path.

        """
        state_seq = np.array([self.take_step() for i in range(series_length)]).reshape((series_length, -1))
        return state_seq

    def generate_hidden_markov_sample_path(self, series_length, distributions):
        """ Generates an HMM sample path

        Parameters
        ----------
        series_length : int
            Size of the sample path.

        distributions :  list of rv_generics
            Sampling distribution associated to states

        """

        assert len(distributions) == self.number_of_states, "The operator distributions is invalid because its length " \
                                                            "should be equal to number_of_states "
        for distribution in distributions:
            assert hasattr(distribution, 'rvs'), "All elements of distributions should have callable attribute rvs to " \
                                                 "sample from the distribution "

        markovian_seq = self.generate_sample_path(series_length)
        sample_path = np.array([distributions[state].rvs() for state in markovian_seq])
        return sample_path

    @classmethod
    def get_stationary_dist(cls, transition):
        evals, evecs = np.linalg.eig(transition.T)
        idx = np.argmin(np.abs(evals - 1))
        w = np.real(evecs[:, idx]).T
        w = w / np.sum(w)
        return w

    @classmethod
    def generate_arbitrary_markovian_transition(cls, n_states, order):
        n_extended_state = n_states ** order
        transition_mat = np.zeros((n_extended_state, n_extended_state))
        for i in range(n_extended_state):
            cutting_points = np.random.uniform(size=n_states - 1)
            cutting_points.sort()
            transition_prob = [cutting_points[0]]
            for j in range(n_states - 2):
                transition_prob.append(cutting_points[j + 1] - cutting_points[j])
            transition_prob.append(1 - cutting_points[-1])
            states_common_part = (i % (n_states ** (order - 1))) * n_states
            for j in range(n_states):
                transition_mat[i, states_common_part + j] = transition_prob[j]

        # Checks the stationarity condition of generated transition matrix
        evals, evecs = np.linalg.eig(transition_mat.T)
        if np.min(np.abs(evals - 1)) < 1e-8:
            return transition_mat

        return cls.generate_arbitrary_markovian_transition(n_states, order)


def write_to_file(f_name, data):
    """ Write a multidimensional time-series dataset into a file

    Parameters
    ----------
    f_name : str
        Full path to save the data to.
    data : list or ndarray
        list of ndarray of shape=(sz, d)
        ndarray of shape=(n_ts, sz, d)
    """
    if type(data) is list:
        data = np.array(data)
    np.savetxt(f'{f_name}.csv', data.reshape(data.shape[0], -1))
    with open(f'{f_name}.shape', 'wt') as f:
        f.write(','.join(map(str,data.shape)))


def read_from_file(f_name):
    """Read a multidimensional time-series from a file

    Parameters
    ----------

    f_name : str
        Full path to read the data from.

    """
    shape = None
    with open(f'{f_name}.shape', 'rt') as f:
        shape = [int(i) for i in f.readline().split(',')]
    data = np.loadtxt(f'{f_name}.csv')
    return data.reshape(shape)
