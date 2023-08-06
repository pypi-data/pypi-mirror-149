"""
Useful functions to draw clusters
"""

from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np
import scipy.cluster.hierarchy as sch
import seaborn as sb
from matplotlib import cm
from matplotlib.colors import ListedColormap
from phasik.drawing.utils import palette_20_ordered
from phasik.utils.clusters import rand_index_over_methods_and_sizes
from sklearn.metrics import adjusted_rand_score

__all__ = [
    "plot_randindex_bars_over_methods_and_sizes",
    "plot_cluster_set",
    "plot_cluster_sets",
    "plot_average_silhouettes",
    "plot_ns_clusters",
    "relabel_next_clusterset_sorted",
    "relabel_clusters_sorted",
    "relabel_clustersets",
    "relabel_clustersets_from_dict"
]


def plot_randindex_bars_over_methods_and_sizes(
    valid_cluster_sets, reference_method="ward", ax=None, plot_ref=False
):

    "Plot Rand Index as bars, to compare any method to a reference method, for all combinations of methods and number of clusters" ""

    if ax is None:
        ax = plt.gca()

    valid_methods = [sets[1] for sets in valid_cluster_sets]

    i_ref = valid_methods.index(reference_method)
    clusters_ref = valid_cluster_sets[i_ref][0]

    rand_index = rand_index_over_methods_and_sizes(valid_cluster_sets, reference_method)
    n_sizes, n_methods = rand_index.shape

    if not plot_ref:
        n_methods -= 1

    width = 1  # bar width
    width_size = n_methods * width  # width of all bars for a given # of clusters
    width_inter_size = 4 * width  # width space between two # of clusters

    xlabels = clusters_ref.n_clusters
    xticks = np.arange(n_sizes) * (width_size + width_inter_size)  # the label locations

    for i, method in enumerate(valid_methods):

        heights = rand_index[:, i]

        if not plot_ref and i == i_ref:
            pass
        else:  # don't plot i_ref if plot_ref is False
            ax.bar(xticks + i * width - width_size / 2, heights, width, label=method)

    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)


def plot_cluster_set(
    cluster_set,
    ax=None,
    y_height=0,
    cmap=cm.get_cmap("tab10"),
    number_of_colors=10,
    colors=None,
):
    """Plots this cluster set as a scatter graph

    Parameters
    ----------
    cluster_set :

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

    if ax is None:
        ax = plt.gca()

    y = np.ones(len(cluster_set.times)) * y_height

    if isinstance(colors, list):
        clusters_plot = relabel_clusters_sorted(
            cluster_set.clusters, final_labels=colors
        )
    else:
        clusters_plot = cluster_set.clusters

    # check that the clustering has not changed
    assert adjusted_rand_score(clusters_plot, cluster_set.clusters) == 1

    ax.scatter(
        cluster_set.times, y, c=clusters_plot, cmap=cmap, vmin=1, vmax=number_of_colors
    )


def plot_cluster_sets(
    cluster_sets,
    axs=None,
    coloring="consistent",
    translation=None,
    with_silhouettes=False,
    with_n_clusters=False,
):
    """Plot these cluster sets as a scatter graph

    Parameters
    ----------
    cluster_sets : tempnetx ClusterSets

    axs : matplotlib.Axes, optional
        Matplotlib axes on which to plot
    coloring : {'ascending', 'consistent', None}, optional

    translation : dict, optional
        If None (default), has no effect. Elsee, dictionary that determines which label 
        should be replaced by which other label
        For example {1: 2, 2: 3, 3: 1}
        It is applied after the order relabling from `method`.
    with_silhouettes : bool, optional

    with_n_clusters : bool, optional

    Returns
    -------
    None
    """

    if axs is None:
        assert not with_silhouettes
        assert not with_n_clusters
        ax1 = plt.gca()

    if with_silhouettes:
        if with_n_clusters:
            ax1, ax2, ax3 = axs
        else:
            ax1, ax2 = axs
    else:
        if isinstance(axs, tuple):
            ax1 = axs[0]
        else:
            ax1 = axs

    if coloring is not None:
        cluster_sets = relabel_clustersets(cluster_sets, method=coloring, translation=translation)

    for cluster_set in cluster_sets:
        #            (cmap, number_of_colors) = ('tab20', 20) if cluster_set.size > 10 else ('tab10', 10)
        # replace by single colour palette with 20 colours such that first 10 colours are same as tab10
        cmap = palette_20_ordered(as_map=True)
        number_of_colors = 20
        plot_cluster_set(
            cluster_set,
            ax=ax1,
            y_height=cluster_set.n_max,
            cmap=cmap,
            number_of_colors=number_of_colors,
        )

    if with_silhouettes:
        plot_average_silhouettes(cluster_sets, ax=ax2)

    if with_n_clusters:
        plot_ns_clusters(cluster_sets, ax=ax3)


def plot_dendrogram(
    cluster_set, ax=None, distance_threshold=None, leaf_rotation=90, leaf_font_size=6
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

    if ax is None:
        ax = plt.gca()

    if cluster_set.linkage is None:
        raise ValueError(
            "Cannot compute the threshold of a non-hierarchical clustering"
        )

    # Calculate the distance threshold at which clusters stop, so that below this threshold we plot the
    # dendrogram in colour, while above it we plot in black.
    if distance_threshold is None:
        distance_threshold = cluster_set.distance_threshold()

    sch.dendrogram(
        cluster_set.linkage,
        leaf_rotation=leaf_rotation,
        leaf_font_size=leaf_font_size,
        color_threshold=distance_threshold,
        above_threshold_color="black",
        ax=ax,
    )
    ax.axhline(y=distance_threshold, c="grey", ls="--", zorder=1)


def plot_average_silhouettes(cluster_sets, ax=None):
    """Plot the average silhouettes across this range of cluster sets

    Parameters
    ----------
    cluster_sets : ClusterSets

    ax : matplotlib.Axes, optional
        Axes on which to plot
    Returns
    -------
    None
    """

    if ax is None:
        ax = plt.gca()
    ax.plot(cluster_sets.silhouettes_average, cluster_sets.ns_max, "ko-")
    ax.set_xlabel("Average silhouette")


def plot_ns_clusters(cluster_sets, ax=None):
    """Plot the average cluster set sizes across this range of cluster sets

    Parameters
    ----------
    cluster_sets : ClusterSets
    ax : matplotlib.Axes, optional
        Axes on which to plot

    Returns
    -------
    None
    """

    if ax is None:
        ax = plt.gca()
    ax.plot(cluster_sets.n_clusters, cluster_sets.ns_max, "ko-")


def relabel_clusters_sorted(clusters, final_labels=None):
    """Returns array of cluster labels sorted in order of appearance, with clusters unchanged

    Parameters
    ----------
    clusters : array of int
        Cluster labels
    final_labels : array of int
        Cluster labels in expected order (has size of the number of clusters)

    Example
    --------
    >>> clusters = np.array([2, 2, 2, 3, 3, 1, 1, 1])
    >>> relabel_clusters_sorted(clusters)
    [ 1 1 1 2 2 3 3 3 ]
    """
    arr = -clusters
    i = 1
    for j, el in enumerate(arr):
        if el >= 0:
            pass
        else:
            arr[arr == el] = i
            i += 1

    if final_labels is not None:
        if not set(clusters) == set(final_labels):
            raise ValueError("The length of final_labels must the number of clusters")

    if isinstance(final_labels, list):
        arr = list(map(lambda k: final_labels[k - 1], arr))

    # check that the clustering has not changed
    assert adjusted_rand_score(clusters, arr) == 1

    return arr


def relabel_clustersets(cluster_sets, method="consistent", translation=None):
    """Relabels clusters in each cluster set, so that clusters are labeled consistently at different numbers
    of clusters.

    This is especially useful when plotting cluster sets, to have consistent colouring.

    Parameters
    ----------
    cluster_sets : ClusterSets
    method : {'consistent', 'ascending'}, optional
    translation : dict, optional
        If None (default), has no effect. Elsee, dictionary that determines which label 
        should be replaced by which other label
        For example {1: 2, 2: 3, 3: 1}
        It is applied after the order relabling from `method`.

    Returns
    -------
    cluster_sets_sorted: ClusterSets

    """

    if method not in ["consistent", "ascending"]:
        raise ValueError("Method should be one of ['consistent', 'ascending'].")

    n = len(cluster_sets.n_clusters)

    cluster_sets_sorted = deepcopy(cluster_sets)
    new_clusters = []

    if method == "ascending" or method == "consistent":
        cluster_sets_sorted.clusters[0] = relabel_clusters_sorted(
            cluster_sets_sorted.clusters[0]
        )
        cluster_sets_sorted[0].clusters = relabel_clusters_sorted(
            cluster_sets_sorted.clusters[0]
        )

    # compute without modifying original
    for i in range(n - 1):
        #        print("dealing now with")
        #        print(i+1, "th no. of clusters", cluster_sets.sizes[i+1], "clusters")
        if method == "consistent":
            cluster_sets_sorted = relabel_next_clusterset_sorted(
                cluster_sets, cluster_sets_sorted, i
            )
        elif method == "ascending":
            cluster_sets_sorted.clusters[i + 1] = relabel_clusters_sorted(
                cluster_sets_sorted.clusters[i + 1]
            )
            cluster_sets_sorted[i + 1].clusters = relabel_clusters_sorted(
                cluster_sets_sorted.clusters[i + 1]
            )
        else:
            raise KeyError("Unknown sorting method")

    if translation is not None:
        cluster_sets_sorted = relabel_clustersets_from_dict(cluster_sets_sorted, translation)

    return cluster_sets_sorted


def relabel_clustersets_from_dict(cluster_sets, translation):
    """Relabels clusters in each cluster set, so that clusters are labeled according to the
    translation dictionary

    This is especially useful when plotting cluster sets, to have consistent colouring. between
    different figures with cluster sets.

    Parameters
    ----------
    cluster_sets : ClusterSets
    translation : dict
        Dictionary that determines which label should be replaced by which other label
        For example {1: 2, 2: 3, 3: 1}

    Returns
    -------
    cluster_sets_sorted: ClusterSets
    """

    if set(translation.keys()) != set(translation.values()):
        raise ValueError(
            "`translation` is not a valid dict: it does not preserve the original cluster structure."
        )

    cluster_sets_relabled = deepcopy(cluster_sets)

    # swap label values in summary array
    for k, v in translation.items():
        cluster_sets_relabled.clusters[cluster_sets.clusters == k] = v

    # swap label values in each clusterset
    for i, clusters in enumerate(cluster_sets_relabled.clusters):
        cluster_sets_relabled.clusters_sets[i].clusters = clusters

    return cluster_sets_relabled


def relabel_next_clusterset_sorted(cluster_sets, cluster_sets_sorted, i):
    """Relabels the clusters in i+1th cluster set so that it is consistent with ith cluster set

    This is especially useful when plotting cluster sets, to have consistent colouring.

    Parameters
    ----------
    cluster_sets : ClusterSets
        Original cluster sets
    cluster_sets_sorted : ClusterSets
        Cluster sets being sorted, already sorted up to i-1
    i : int

    Returns
    -------
    cluster_sets_sorted : ClusterSets
    """

    # first we need the original clusters
    # to determine which cluster was split going from i to i+1 clusters
    clusters_ref = cluster_sets.clusters[i]  # i clusters
    clusters_up = cluster_sets.clusters[i + 1]  # i+1 clusters

    n_ref = cluster_sets.n_clusters[i]
    n_up = cluster_sets.n_clusters[i + 1]

    # those labels that changed between ref and up
    diff = clusters_ref[clusters_ref != clusters_up]

    if diff.size == 0:  # empty array, no difference between i and i+1
        #        print("pass, empty array")
        pass

    else:  # otherwise, sort
        # label of reference cluster that was split in up
        label_split = min(diff)

        # size of cluster before splitting (in ref)
        len_ref = len(clusters_ref[clusters_ref == label_split])
        # size of cluster after splitting (in up)
        len_up = len(clusters_up[clusters_up == label_split])

        # the cluster is split into two clusters: they have labels label_split and label_split+1.
        # we keep the same colour for the bigger of the two, i.e. we assign it label label_split
        # the smaller one is assigned the new colour, i.e. label n_up
        # we need to shift the other labels accordingly
        clusters_ref_sorted = cluster_sets_sorted.clusters[i]
        clusters_up_sorted = cluster_sets_sorted.clusters[i + 1]

        n_diff = n_up - n_ref  # number of additional clusters between i and i+1

        if n_diff == 1:
            if (
                len_up >= len_ref / 2
            ):  # split cluster with old label is bigger than new label: old label stays unchanged
                clusters_up_sorted[
                    clusters_up == label_split + 1
                ] = -1  # flag new cluster
                unchanged = clusters_up_sorted != -1
                clusters_up_sorted[unchanged] = clusters_ref_sorted[unchanged]
                clusters_up_sorted[
                    clusters_up_sorted == -1
                ] = n_up  # assign new colour to new cluster
            else:
                clusters_up_sorted[clusters_up == label_split] = -1  # flag old cluster
                unchanged = clusters_up_sorted != -1
                clusters_up_sorted[unchanged] = clusters_ref_sorted[unchanged]
                clusters_up_sorted[
                    clusters_up_sorted == -1
                ] = n_up  # assign new colour to old cluster
        else:  # more than 1, then cluster is split into labels label_split, label_split+1, label_split+2, ...
            lens_new = [
                len(clusters_up[clusters_up == label_split + j])
                for j in range(n_diff + 1)
            ]
            j_max = np.argmax(lens_new) - 1
            if (
                j_max == -1
            ):  # split cluster with old label is bigger than new label: old label stays unchanged
                for j in range(n_diff):
                    clusters_up_sorted[clusters_up == label_split + 1 + j] = (
                        -1 - j
                    )  # flag new cluster
                unchanged = clusters_up_sorted > 0
                clusters_up_sorted[unchanged] = clusters_ref_sorted[unchanged]
                for j in range(n_diff):
                    clusters_up_sorted[clusters_up_sorted == -1 - j] = (
                        n_up - n_diff + 1 + j
                    )  # assign new colour to new cluster
            else:  # swap old cluster label_split with j_max
                clusters_up_sorted[
                    clusters_up == label_split
                ] = -label_split  # flag old cluster
                for j in range(n_diff):
                    clusters_up_sorted[clusters_up == label_split + 1 + j] = (
                        -label_split - 1 - j
                    )  # flag new clusters
                unchanged = clusters_up_sorted > 0
                clusters_up_sorted[unchanged] = clusters_ref_sorted[unchanged]
                clusters_up_sorted[
                    clusters_up_sorted == -label_split - 1 - j_max
                ] = label_split
                for j in range(n_diff):
                    if j != j_max:
                        clusters_up_sorted[
                            clusters_up_sorted == -label_split - 1 - j
                        ] = (
                            n_up - n_diff + 1 + j
                        )  # assign new colour to new cluster
                clusters_up_sorted[clusters_up_sorted == -label_split] = (
                    n_up - n_diff + 1 + j_max
                )  # assign new colour to old cluster

        # update clusters also in cluster_set instance
        cluster_sets_sorted[i + 1].clusters = clusters_up_sorted

        # check that the clustering has not changed
        assert adjusted_rand_score(clusters_up_sorted, clusters_up) == 1

    return cluster_sets_sorted
