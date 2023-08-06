"""
Functions to manipulate and sort clusters
"""

from copy import deepcopy

import numpy as np
from sklearn.metrics import adjusted_rand_score

__all__ = [
    "aggregate_network_by_cluster",
    "convert_cluster_labels_to_dict",
    "rand_index_over_methods_and_sizes",
    "cluster_sort",
    "sort_for_colouring",
    "sort_next_clusters_for_colouring",
]


def aggregate_network_by_cluster(
    temporal_network, clusters, sort_clusters=None, output="averaged"
):
    """Aggregates the temporal network over eacher cluster in a cluster set


    Parameters
    ----------
    temporal_network : phasik.TemporalNetwork
        Temporal network to aggregate
    clusters : array of int
        Cluster labels
    sort_clusters : bool
        If True, sort cluster labels basde on ascending times
    output : {'weighted', 'averaged', 'binary', 'normalised'}, optional
            Determines the type of output edge weights

    Returns
    -------
    aggregates : dict
        Dict each key is a cluster label and each value is a tuple
        of the form (networkx.Graph, list of time indices of cluster).
    """

    aggregates = {}

    if sort_clusters == True:  # sort by ascending times
        clusters = cluster_sort(clusters)
    elif (sort_clusters == False) or (sort_clusters is None):
        pass
    elif isinstance(sort_clusters, list):  # sort by specified order
        clusters = cluster_sort(clusters, final_labels=sort_clusters)
    else:
        raise ValueError(
            "Invalid value for 'sort_clusters': must be True or a list of cluster labels"
        )

    cluster_time_indices = convert_cluster_labels_to_dict(clusters)

    for cluster_label, time_indices in cluster_time_indices.items():

        aggregates[cluster_label] = (
            temporal_network.aggregated_network(
                time_indices=time_indices, output=output
            ),
            time_indices,
        )

    return aggregates


def convert_cluster_labels_to_dict(clusters):
    """Returns dictionary where each key is a cluster label and each
    value is list of the time indices composing the cluster

    Parameters
    ----------
    clusters : list of int
        List of cluster labels

    Return
    ------

    """
    n_max = max(clusters)

    cluster_times = {n: list(np.where(clusters == n)[0]) for n in range(1, n_max + 1)}

    return cluster_times


def rand_index_over_methods_and_sizes(valid_cluster_sets, reference_method="ward"):

    """
    Compute Rand Index to compare any method to a reference method, for all combinations of methods and number of clusters


    Parameters
    ----------
    valid_cluster_sets : list

    reference_method : str

    Returns
    -------

    rand_scores : ndarray
        Array of dimension (n_sizes, n_methods) with rand index scores

    """

    valid_methods = [sets[1] for sets in valid_cluster_sets]

    i_ref = valid_methods.index(reference_method)
    clusters_ref = valid_cluster_sets[i_ref][0]

    # compute Rand index to compare each method with reference method, for each number of clusters
    n_sizes = len(clusters_ref.n_clusters)
    n_methods = len(valid_cluster_sets)

    rand_scores = np.zeros((n_sizes, n_methods))

    for i_size, size in enumerate(clusters_ref.n_clusters):
        for i_method, method in enumerate(valid_methods):

            clusters2 = valid_cluster_sets[i_method][0]

            rand_index = adjusted_rand_score(
                clusters_ref.clusters[i_size], clusters2.clusters[i_size]
            )
            rand_scores[i_size, i_method] = rand_index

    return rand_scores


def cluster_sort(clusters, final_labels=None):
    """
    Return array of cluster labels sorted in order of appearance, with clusters unchanged

    Example
    --------
    >>> clusters = np.array([2, 2, 2, 3, 3, 1, 1, 1])
    >>> cluster_sort(clusters)
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

    if isinstance(final_labels, list):
        arr = list(map(lambda i: final_labels[i - 1], arr))

    # check that the clustering has not changed
    assert adjusted_rand_score(clusters, arr) == 1

    return arr


def sort_for_colouring(cluster_sets, method="consistent"):

    n = len(cluster_sets.sizes)

    cluster_sets_sorted = deepcopy(cluster_sets)
    new_clusters = []

    if method == "ascending":
        cluster_sets_sorted.clusters[0] = cluster_sort(cluster_sets_sorted.clusters[0])
        cluster_sets_sorted[0].clusters = cluster_sort(cluster_sets_sorted.clusters[0])

    # compute without modifying original
    for i in range(n - 1):
        #        print("dealing now with")
        #        print(i+1, "th no. of clusters", cluster_sets.sizes[i+1], "clusters")
        if method == "consistent":
            cluster_sets_sorted = sort_next_clusters_for_colouring(
                cluster_sets, cluster_sets_sorted, i
            )
        elif method == "ascending":
            cluster_sets_sorted.clusters[i + 1] = cluster_sort(
                cluster_sets_sorted.clusters[i + 1]
            )
            cluster_sets_sorted[i + 1].clusters = cluster_sort(
                cluster_sets_sorted.clusters[i + 1]
            )
        else:
            print("Unknown method")
    return cluster_sets_sorted


def sort_next_clusters_for_colouring(cluster_sets, cluster_sets_sorted, i):

    # first we need the original clusters
    # to determine which cluster was split going from i to i+1 clusters
    clusters_ref = cluster_sets.clusters[i]  # i clusters
    clusters_up = cluster_sets.clusters[i + 1]  # i+1 clusters

    n_ref = cluster_sets.sizes[i]
    n_up = cluster_sets.sizes[i + 1]

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
