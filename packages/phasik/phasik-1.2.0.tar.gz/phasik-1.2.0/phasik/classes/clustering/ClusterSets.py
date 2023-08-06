"""
Base class for cluster sets, i.e. clustering for a range of number of clusters
"""

from collections import Sequence

import numpy as np
from phasik.classes.clustering import ClusterSet
from phasik.drawing.drawing import plot_events, plot_phases
from phasik.drawing.drawing_clusters import (plot_cluster_sets,
                                             relabel_clustersets)
from phasik.drawing.utils import adjust_margin, display_name

__all__ = ["ClusterSets"]


class ClusterSets(Sequence):
    """Base class for sets of clusters (partition) of timepoints

    Attributes
    -----------

    cluster_sets : iterable of phasik.ClusterSet
        List of ClusterSets
    clusters : numpy array of int
        Summary array of the cluster labels, with dim (len(ns_max), len(times))
    n_clusters : list of int
        Number of clusters in the cluster set (partition)
    times : list of (int or float)
        Sorted list of time associated to each clustered snapshot
    distance_metric : str
        Distance metric used to compute the distance between snapshots, e.g. 'euclidean',
        with sklearn.metrics.pairwise.paired_distances.
        It must be one of the options allowed by scipy.spatial.distance.pdist
        for its metric parameter (e.g. 'chebyshev', 'cityblock', 'correlation',
        'cosine', 'euclidean', 'hamming', 'jaccard', etc.), or a metric listed
        in pairwise.PAIRWISE_DISTANCE_FUNCTIONS.
    n_max_type : float
        Method that was used to determine when to stop clustering when creating this cluster
        set. e.g. A cluster set can be created by clustering until a particular number of clusters has been
        reached ('maxclust'), or until every cluster is at least a certain distance away from each other
        ('distance').
    ns_max : list of int
        List of values corresponding to the n_max_type described above, in other words,
        list of numbers clusters to be computed. The number of elements in this list
        is the number of ClusterSet computed.
    silhouettes_average : numpy array
        Value of average silouette for each clustering
    """

    def __init__(self, cluster_sets, n_max_type, ns_max):

        """
        Parameters
        ----------
        cluster_sets : iterable of ClusterSet

        n_max_type : str
            Method that was used to determine when to stop clustering when creating these cluster
            sets. e.g. A cluster set can be created by clustering until a particular number of clusters has been
            reached ('maxclust'), or until every cluster is at least a certain distance away from each other
            ('distance')
        ns_max : list of int
            List of values corresponding to the n_max_type described above, in other words,
            list of numbers clusters to be computed. The number of elements in this list
            is the number of ClusterSet computed.

        """

        self._cluster_sets = cluster_sets
        self.clusters = np.array(
            [cluster_set.clusters for cluster_set in cluster_sets]
        )  # array of cluster labels
        self.n_clusters = np.array(
            [cluster_set.n_clusters for cluster_set in cluster_sets]
        )
        self.times = cluster_sets[0].times  # times must be the same in all sets
        self.distance_metric = cluster_sets[
            0
        ].distance_metric  # must be the same in all sets
        self.n_max_type = n_max_type
        self.ns_max = ns_max
        self.silhouettes_average = np.array(
            [cluster_set.silhouette_average for cluster_set in cluster_sets]
        )

    def __len__(self):
        return len(self._cluster_sets)

    def __getitem__(self, key):
        return self._cluster_sets[key]

    @property
    def clusters_sets(self):
        """Returns the list of ClusterSet"""
        return self._cluster_sets

    @classmethod
    def from_distance_matrix(
        cls, distance_matrix, n_max_type, ns_clusters_max, cluster_method
    ):
        """Generates ClusterSets from a distance matrix

        Parameters
        ----------
        distance_matrix : phasik.DistanceMatrix
            Distance matrix from which to cluster
        cluster_method : str
            Clustering method used to cluster the temporal network snapshots. Examples :
            'k_means',  'centroid', 'average', 'complete', 'weighted', 'median', 'single', 'ward'
        n_max_type : str
            The method that determines when to stop clustering. For example, cluster set
            can be created by clustering until a particular number of clusters has been
            reached ('maxclust'), or until every cluster is at least a certain distance
            away from each other ('distance').
        ns_clusters_max : list of int
            List of values corresponding to the n_max_type described above, in other words,
            list of numbers clusters to be computed. The number of elements in this list
            is the number of ClusterSet computed.

        Returns
        -------
        ClusterSets

        """
        cluster_sets = [
            ClusterSet.from_distance_matrix(
                distance_matrix, n_max_type, n_max, cluster_method
            )
            for n_max in ns_clusters_max
        ]

        return cls(cluster_sets, n_max_type, ns_clusters_max)

    def plot(
        self,
        axs=None,
        coloring="consistent",
        translation=None,
        with_silhouettes=False,
        with_n_clusters=False,
    ):
        """Plots these cluster sets as a scatter graph

        Parameters
        ----------
        ax : matplotlib.Axes, optional
            Axes on which to plot
        coloring : {'ascending', 'consistent', None}
        translation : dict, optional
        If None (default), has no effect. Elsee, dictionary that determines which label 
        should be replaced by which other label
        For example {1: 2, 2: 3, 3: 1}
        It is applied after the order relabling from `method`.
        with_silhouettes : bool
            If True, also plot the average silhouettes on a 2nd axis. Defaults to False.
        with_n_clusters : bool
            If True, also plot the actual number of clusters on a 3rd axis. Defaults to False.

        Returns
        -------
        None
        """
        return plot_cluster_sets(self, axs, coloring, translation, with_silhouettes, with_n_clusters)

    def plot_and_format_with_average_silhouettes(
        self, axs, events, phases, time_ticks=None, coloring="consistent"
    ):
        """Plot and format these cluster sets as a scatter graph, along with the average silhouettes and cluster set
        sizes

        Our pattern generally has been to leave all formatting in the jupyter notebooks, but this method is used
        by several different notebooks, so it makes sense to put it somewhere common.

        Parameters
        ----------
        axs : list of matplotlib.Axes
            Axes on which to plot; should be an indexable object with at least three items
        events :
            Any events that should be plotted on the scatter graph
        phases :
            Any phases that should be plotted on the scatter graph
        time_ticks : list or array
            The ticks that should be displayed along the x-axis (time axis)

        Returns
        -------
        None
        """

        (ax1, ax2, ax3) = (axs[0], axs[1], axs[2])

        # Plot
        ax3.tick_params(labelleft=True, labelbottom=True)
        self.plot(
            axs=(ax1, ax2, ax3),
            coloring=coloring,
            with_silhouettes=True,
            with_n_clusters=True,
        )
        adjust_margin(ax1, bottom=(0.15 if phases else 0))
        plot_events(events, ax=ax1)
        plot_phases(phases, ax=ax1, y_pos=0.04, ymax=0.1)

        # Format
        ax1.set_xlabel("Time")
        ax1.set_ylabel(display_name(self.n_max_type))
        ax1.tick_params(labelbottom=True)
        if time_ticks:
            ax1.set_xticks(time_ticks)

        ax2.set_xlabel("Average silhouette")
        ax2.set_xlim((0, 1))
        ax2.tick_params(labelleft=True, labelbottom=True)

        ax3.set_xlabel("Actual # clusters")

    def plot_silhouette_samples(self, axs, coloring="consistent"):
        """Plot the average silhouettes across this range of cluster sets

        Parameters
        ----------
        axs : list of matplotlib.Axes
            Axes on which to plot; should be an iterable object with at least as many items as there
            are cluster sets in this class.

        Returns
        -------
        None
        """

        if coloring == "consistent":
            self = relabel_clustersets(self)

        for cluster_set, ax in zip(self._cluster_sets, axs.flatten()):
            cluster_set.plot_silhouette_samples(ax=ax)
