"""
Base class for a cluster set of temporal network snapshots
"""

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import scipy.cluster.hierarchy as sch
import seaborn as sb
from phasik.classes import DistanceMatrix
from phasik.drawing.drawing_clusters import plot_cluster_set, plot_dendrogram
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

__all__ = ["ClusterSet"]


class ClusterSet:
    """Base class for a set of clusters (partition) of timepoints

    Attributes
    -----------

    clusters : list of int
        Clusters as a list of cluster labels
    times : list of (int or float)
        Sorted list of time associated to each clustered snapshot
    n_clusters : int
        Number of clusters in the cluster set (partition)
    cluster_method : float
        Method used to cluster the snapshots . Examples :
        'k_means',  'centroid', 'average', 'complete', 'weighted', 'median', 'single', 'ward'
    n_max_type : float
        Method that was used to determine when to stop clustering when creating this cluster
        set. e.g. A cluster set can be created by clustering until a particular number of clusters has been
        reached ('maxclust'), or until every cluster is at least a certain distance away from each other
        ('distance').
    n_max : int
        Value corresponding to the n_max_type described above.
    distance_metric : str
        Distance metric used to compute the distance between snapshots, e.g. 'euclidean',
        with sklearn.metrics.pairwise.paired_distances.
        It must be one of the options allowed by scipy.spatial.distance.pdist
        for its metric parameter (e.g. 'chebyshev', 'cityblock', 'correlation',
        'cosine', 'euclidean', 'hamming', 'jaccard', etc.), or a metric listed
        in pairwise.PAIRWISE_DISTANCE_FUNCTIONS.
    """

    def __init__(
        self,
        clusters,
        times,
        linkage,
        distance_matrix,
        distance_metric,
        cluster_method,
        n_clusters_max,
        n_max_type,
    ):
        """

        Parameters
        ----------
        clusters : list of int
            Clusters as a list of cluster labels
        times : list of (int or float)
            Sorted list of time associated to each clustered snapshot
        linkage :
            Linkage of the clustering
        distance_matrix : phasik.DistanceMatrix
            Distance matrix from which the clusters were computed
        cluster_method : float
            Method used to cluster the snapshots . Examples :
            k_means',  'centroid', 'average', 'complete', 'weighted', 'median', 'single', 'ward'
        n_max_type : float
            Method that was used to determine when to stop clustering when creating this cluster
            set. e.g. A cluster set can be created by clustering until a particular number of clusters has been
            reached ('maxclust'), or until every cluster is at least a certain distance away from each other
            ('distance').
        n_clusters_max : int
            Value corresponding to the n_max_type described above.
        distance_metric : str
            Distance metric used to compute the distance between snapshots, e.g. 'euclidean',
            with sklearn.metrics.pairwise.paired_distances.
            It must be one of the options allowed by scipy.spatial.distance.pdist
            for its metric parameter (e.g. 'chebyshev', 'cityblock', 'correlation',
            'cosine', 'euclidean', 'hamming', 'jaccard', etc.), or a metric listed
            in pairwise.PAIRWISE_DISTANCE_FUNCTIONS.

        """

        self._clusters = clusters
        self._times = times
        self.n_clusters = len(set(clusters))
        self._cluster_method = cluster_method
        self._n_max = n_clusters_max
        self._n_max_type = n_max_type
        self._distance_metric = distance_metric
        try:
            self.silhouette_average = silhouette_score(
                distance_matrix.distance_matrix, clusters, metric="precomputed"
            )
            self.silhouette_samples = silhouette_samples(
                distance_matrix.distance_matrix, clusters, metric="precomputed"
            )
        except ValueError as error:
            # Often the number of clusters is 1, which sklearn does not like.
            print(
                f"WARNING: unable to compute silhouette for cluster set. Error is: {error}"
            )
            self.silhouette_average = 0
            self.silhouette_samples = np.array([])
        self.linkage = linkage

    @property
    def clusters(self):
        """Returns the clusters, i.e. a list of cluster labels (int)"""
        return self._clusters

    @clusters.setter
    def clusters(self, arr):
        self._clusters = arr

    @property
    def times(self):
        """Returns the list of times corresponding to datapoints clustered"""
        return self._times

    @property
    def cluster_method(self):
        """Returns the clustering method used to cluster the temporal data"""
        return self._cluster_method

    @property
    def n_max_type(self):
        """Returns the method (str) that determines when to stop clustering"""
        return self._n_max_type

    @property
    def n_max(self):
        """Returns the value corresponding to the n_max_type described above."""
        return self._n_max

    @property
    def distance_metric(self):
        """Returns the distance metric used to compute the distance between snapshots, e.g. 'euclidean'"""
        return self._distance_metric

    @classmethod
    def from_distance_matrix(
        cls, distance_matrix, n_max_type, n_clusters_max, cluster_method
    ):
        """Generates a ClusterSet from a distance matrix

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
        n_clusters_max : int
            Value corresponding to the n_max_type described above.

        Returns
        -------
        ClusterSet

        """

        times = distance_matrix.times
        distance_metric = distance_matrix.distance_metric

        if cluster_method == "k_means":
            # k-means clustering is only applicable for n_max_type of 'maxclust'
            if n_max_type != "maxclust":
                raise ValueError(
                    f"With {cluster_method}, the n_max_type must be 'maxclust'."
                )

            k_means = KMeans(n_clusters=n_clusters_max, random_state=None)
            clusters = k_means.fit_predict(distance_matrix.snapshots_flat) + 1
            linkage = None

        else:  # hierarchical clustering TODO specify allowed methods
            # From scipy's documentation:
            # "Methods ‘centroid’, ‘median’, and ‘ward’ are correctly defined
            # only if Euclidean pairwise metric is used. If 'y' is passed as precomputed pairwise distances,
            # then it is the user’s responsibility to assure that these distances are in fact Euclidean,
            # otherwise the produced result will be incorrect."
            if cluster_method in ["ward", "centroid", "median"]:
                if distance_metric != "euclidean":
                    raise ValueError(
                        f"With {cluster_method}-linkage, the distance metric must be 'euclidean'."
                    )

            # if len(distance_matrix.distance_matrix_flat) > 0 : # TODO check what it checks
            linkage = sch.linkage(
                distance_matrix.distance_matrix_flat, method=cluster_method
            )
            clusters = sch.fcluster(linkage, n_clusters_max, criterion=n_max_type)

        return cls(
            clusters,
            times,
            linkage,
            distance_matrix,
            distance_metric,
            cluster_method,
            n_clusters_max,
            n_max_type,
        )

    @classmethod
    def from_temporal_network(
        cls,
        temporal_network,
        distance_metric,
        clustering_method,
        n_max_type,
        n_clusters_max,
    ):
        """Generates a ClusterSet from a temporal network

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
        clustering_method : str
            Clustering method used to cluster the temporal network snapshots. Examples :
            'k_means',  'centroid', 'average', 'complete', 'weighted', 'median', 'single', 'ward'
        n_max_type : str
            The method that determines when to stop clustering. For example, cluster set
            can be created by clustering until a particular number of clusters has been
            reached ('maxclust'), or until every cluster is at least a certain distance
            away from each other ('distance').
        n_clusters_max : int
            Value corresponding to the n_max_type described above.

        Returns
        -------
        ClusterSet

        """

        distance_matrix = SnapshotsDistanceMatrix.from_temporal_network(
            temporal_network, distance_metric
        )

        return cls.from_distance_matrix(
            distance_matrix, n_max_type, n_clusters_max, cluster_method
        )

    def distance_threshold(self):
        """Calculate the distance at which clustering stops

        Parameters
        ----------
        None

        Returns
        -------
        int
            Smallest number d such that the distance between any two clusters is < d.
        """

        if self.linkage is None:
            raise ValueError(
                "Cannot compute the threshold of a non-hierarchical clustering"
            )

        number_of_observations = self.linkage.shape[0] + 1
        if self.n_clusters >= number_of_observations:
            return 0
        elif self.n_clusters <= 1:
            return self.linkage[-1, 2] * 1.001
        else:
            return self.linkage[-self.n_clusters, 2] * 1.001

    def plot_dendrogram(
        self, ax=None, distance_threshold=None, leaf_rotation=90, leaf_font_size=6
    ):
        """Plot this cluster set as a dendrogram

        Parameters
        ----------
        ax : matplotlib.Axes, optional
            Axes on which to plot
        leaf_rotation : int or float, optional
            Rotation to apply to the x-axis (leaf) labels (default 90)
        leaf_font_size : int or str, optional
            Desired size of the x-axis (leaf) labels (default 6)

        Returns
        -------
        None
        """

        return plot_dendrogram(
            self, ax, distance_threshold, leaf_rotation, leaf_font_size
        )

    def plot(
        self,
        ax=None,
        y_height=0,
        cmap=cm.get_cmap("tab10"),
        number_of_colors=10,
        colors=None,
    ):
        """Plots this cluster set as a scatter graph

        Parameters
        ----------
        ax : matplotlib.Axes, optional
            Axes on which to plot
        y_height : int or float, optional
            Height at which to plot (default 0)
        cmap : matplotlib.cm, optional
            Desired colour map (default 'tab10')
        number_of_colors : int, optional
            Desired number of colours to use for the colormap (default 10)
        colors: list of int, optional
            If None (default), cluster label 0 is assigned its automatic color "C0"
            and so on. If `colors` is a list (e.g. [3,1,2]), it relabels the clusters in that order
            and assigns them the new corresponding colors. 

        Returns
        -------
        None
        """

        return plot_cluster_set(self, ax, y_height, cmap, number_of_colors, colors)

    def plot_silhouette_samples(self, ax=None):
        """Plot the silhouette samples from this cluster set

        Parameters
        ----------
        ax : matplotlib.Axes, optional
            Axes on which to plot

        Returns
        -------
        None
        """

        if ax is None:
            ax = plt.gca()

        # If there are more than 10 clusters in this cluster set, we'll need to use more colours in our plot.
        #        sb.set_palette("tab20" if self.size > 10 else "tab10")
        # replace by single colour palette with 20 colours such that first 10 colours are same as tab10
        pal = sb.color_palette("tab20", n_colors=20)
        pal2_arr = np.append(pal[::2], pal[1::2], axis=0)
        pal2 = sb.color_palette(pal2_arr)
        sb.set_palette(pal2)

        if self.silhouette_samples.size > 0:
            y_lower = 0
            for i, cluster in enumerate(np.unique(self.clusters)):
                # Aggregate the silhouette scores for samples belonging to each cluster, and sort them
                silhouette_values = self.silhouette_samples[self.clusters == cluster]
                silhouette_values.sort()
                silhouette_size = silhouette_values.shape[0]

                # Calculate height of this cluster
                y_upper = y_lower + silhouette_size
                y = np.arange(y_lower, y_upper)
                ax.fill_betweenx(
                    y,
                    0,
                    silhouette_values,
                    facecolor=f"C{i}",
                    edgecolor=f"C{i}",
                    alpha=1,
                )

                # Compute the new y_lower for next cluster
                vertical_padding = 0
                y_lower = y_upper + vertical_padding

        ax.axvline(x=self.silhouette_average, c="k", ls="--")
