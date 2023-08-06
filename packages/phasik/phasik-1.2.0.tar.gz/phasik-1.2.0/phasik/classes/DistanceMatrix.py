"""
Base class for the distance matrix of snapshots
"""

import numpy as np
from sklearn.metrics import pairwise_distances

__all__ = ["DistanceMatrix"]


class DistanceMatrix:
    """Base class for matrix of pairwise distance/similarity between snapshots of a temporal network.

    Attributes
    ----------
    times : list of (int or float)
        Times corresponding to each of the T snapshots
    snapshots : numpy array
        Array of dim (T, N, N) representing instantaneous adjacency matrices. Snapshots
        can also be inputed as vectors of dim (T, N).
    snapshots_flat : numpy array
        Snapshots (flattened into vectors if originals are matrices)
        from which the distance matrix is computed
    distance_metric : str
        Distance metric used to compute the distance between snapshots, e.g. 'euclidean'
        with sklearn.metrics.pairwise.paired_distances.
        It must be one of the options allowed by scipy.spatial.distance.pdist
        for its metric parameter (e.g. 'chebyshev', 'cityblock', 'correlation',
        'cosine', 'euclidean', 'hamming', 'jaccard', etc.), or a metric listed
        in pairwise.PAIRWISE_DISTANCE_FUNCTIONS.
    distance_matrix : numpy array
        Array of dim (T, T)
    distance_matrix_flat : numpy array
        Flattened distance matrix of dim (T,)



    """

    def __init__(self, snapshots, times, distance_metric):
        """
        Base class for a distance matrix, i.e. a matrix where each entry
        is the distance/similarity between two snapshots in 'snapshots'.

        Parameters
        ----------
        snapshots : numpy array
            Array of dim (T, N, N) representing instantaneous adjacency matrices. Snapshots
            can also be inputed as vectors of dim (T, N).
        times : list of (float or int)
            Times corresponding to each snapshot
        distance_metric : str
            Distance metric used to compute the distance between snapshots, e.g. 'euclidean',
            with sklearn.metrics.pairwise.paired_distances.
            It must be one of the options allowed by scipy.spatial.distance.pdist
            for its metric parameter (e.g. 'chebyshev', 'cityblock', 'correlation',
            'cosine', 'euclidean', 'hamming', 'jaccard', etc.), or a metric listed
            in pairwise.PAIRWISE_DISTANCE_FUNCTIONS.
        """

        if snapshots.ndim == 2:  # snapshots already in vector form
            T, N = snapshots.shape
            snapshots_flat = snapshots
        elif snapshots.ndim == 3:
            T, N, _ = snapshots.shape
            snapshots_flat = snapshots.reshape(
                T, -1
            )  # flatten each each snapshot (i.e. adjacency matrix) into a vector
        else:
            raise ValueError(
                "Snapshots has wrong number of dimensions: must be 2 or 3."
            )

        self._times = times
        self._snapshots = snapshots
        self._snapshots_flat = snapshots_flat
        self._distance_metric = distance_metric
        self._distance_matrix = pairwise_distances(
            self._snapshots_flat, metric=distance_metric
        )

        # the distance matrix is symmetric. Create a condensed version
        # by flattening the upper triangular half of the matrix into a vector
        upper_triangular_indices = np.triu_indices(n=T, k=1)
        distance_matrix_condensed = self._distance_matrix[upper_triangular_indices]
        self._distance_matrix_flat = distance_matrix_condensed

    @property
    def snapshots(self):
        """Returns the snapshots (matrix or vectors) from which
        the distance matrix is computed"""
        return self._snapshots

    @property
    def snapshots_flat(self):
        """Returns the snapshots (flattened into vectors if original are matrices)
        from which the distance matrix is computed"""
        return self._snapshots_flat

    @property
    def distance_metric(self):
        """Returns the distance metric used to compute the distance matrix"""
        return self._distance_metric

    @property
    def distance_matrix(self):
        """Returns the distance matrix as a numpy array"""
        return self._distance_matrix

    @property
    def times(self):
        """Returns the sorted list of times corresponding to the snapshots"""
        return self._times

    @property
    def distance_matrix_flat(self):
        """Returns the distance matrix flattened for easier use in clustering"""
        return self._distance_matrix_flat

    @classmethod
    def from_temporal_network(cls, temporal_network, distance_metric):
        """Generates a distance matrix from a temporal network

        Each entry of the matrix is the distance between
        two snapshots of the temporal network.

        Parameters
        ----------
        temporal_network : TemporalNetwork
            Temporal network from which to compute the distance matrix
        distance_metric : str
            Distance metric used to compute the distance between snapshots, e.g. 'euclidean',
            with sklearn.metrics.pairwise.paired_distances.
            It must be one of the options allowed by scipy.spatial.distance.pdist
            for its metric parameter (e.g. 'chebyshev', 'cityblock', 'correlation',
            'cosine', 'euclidean', 'hamming', 'jaccard', etc.), or a metric listed
            in pairwise.PAIRWISE_DISTANCE_FUNCTIONS.

        Returns
        -------
        DistanceMatrix

        """

        return cls(temporal_network.snapshots, temporal_network.times, distance_metric)

    @classmethod
    def from_timeseries(cls, timeseries, distance_metric):
        """Generates a distance matrix from time series

        Each entry of the matrix is the distance between
        two 'snapshots' of the timeseries, i.e. the vector with instantaneous values
        of the N timeseries at time t.

        Parameters
        ----------
        timeseries : pandas.Dataframe
            Timeseries relative to nodes, edges, or both. Each row is a timeseries,
            with index as series name and columns as times.
        distance_metric : str
            Distance metric used to compute the distance between snapshots, e.g. 'euclidean',
            with sklearn.metrics.pairwise.paired_distances.
            It must be one of the options allowed by scipy.spatial.distance.pdist
            for its metric parameter (e.g. 'chebyshev', 'cityblock', 'correlation',
            'cosine', 'euclidean', 'hamming', 'jaccard', etc.), or a metric listed
            in pairwise.PAIRWISE_DISTANCE_FUNCTIONS.

        Returns
        -------
        DistanceMatrix

        """

        times = timeseries.columns
        flat_snapshots = timeseries.to_numpy().T

        return cls(flat_snapshots, times, distance_metric)
