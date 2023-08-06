"""
Base class for partially temporal networks
"""

import numpy as np
import pandas as pd
from phasik.classes.TemporalNetwork import (TemporalNetwork,
                                            _process_input_tedges)

__all__ = ["PartiallyTemporalNetwork"]


class PartiallyTemporalNetwork(TemporalNetwork):
    """Base class for partially temporal networks

    Partially temporal networks are temporal networks for which we do not have
    temporal information about all edges.

    Attributes
    ----------
    nodes : list of (str or int)
        Sorted list of node names. Node names can be either strings or integers,
        but they all need to be of the same type.
    times : list of (int or float)
        Sorted list of times for which we have temporal information
    tedges : pandas.DataFrame
        Dataframe containing tedges (potentially weighted).
        Columns are ['i', 'j', 't', ('weight')] and each row represents a tedge.
    snapshots : numpy array
        Array of shape (T, N, N) storing the instantaneous values of
        the adjacency matrix A_{ij}(t).
    temporal_nodes : list of (str or int)
        List of nodes that are part of a temporal edge
    temporal_edges : list of tuples
        List of edges for which we have temporal information

    """

    def __init__(self):
        super().__init__()

        self._temporal_nodes = []
        self._temporal_edges = []

    @property
    def nodes(self):
        return super().nodes

    @property
    def tedges(self):
        return super().tedges

    @property
    def snapshots(self):
        return super().snapshots

    @property
    def temporal_nodes(self):
        return self._temporal_nodes

    @temporal_nodes.setter
    def temporal_nodes(self, nodes):
        self._temporal_nodes = nodes

    @property
    def temporal_edges(self):
        return self._temporal_edges

    @temporal_edges.setter
    def temporal_edges(self, edges):
        self._temporal_edges = edges

    def temporal_neighbors(self):
        """Returns a dict of neighbors in the aggregated network that are temporal nodes"""
        neighbors = super().neighbors()
        return {
            node: [u for u in value if u in self.temporal_nodes]
            for node, value in neighbors.items()
        }

    def number_of_temporal_edges(self):
        """Returns the number of temporal edges in the temporal network"""
        return len(self._temporal_edges)

    def number_of_temporal_nodes(self):
        """Returns the number of temporal nodes in the temporal network"""
        return len(self._temporal_nodes)

    def fraction_of_temporal_nodes(self):
        """Returns the fraction of temporal edges in the temporal network"""
        return self.number_of_temporal_nodes() / self.N()

    def fraction_of_temporal_edges(self):
        """Returns the fraction of temporal edges in the temporal network"""
        return self.number_of_temporal_edges() / self.number_of_edges()

    @classmethod
    def from_tedges(
        cls, tedges, temporal_nodes=None, temporal_edges=None, normalise="max"
    ):
        """Creates a PartiallyTemporalNetwork from a dataframe of tedges

        Parameters
        ----------
        tedges : pandas.DataFrame or list of tuples
            List of tedges with 'i', 'j', 't', and optionally 'weight'
            If DataFrame, these are the name of the columns, and each row contains a tedge
        temporal_nodes : list of (str or int)
            List of temporal nodes
        temporal_edges : list of tuples
            List of temporal edges
        normalise : {'max', 'minmax'}
            Choice of normalsation of the edge timeseries

        Returns
        -------
        TN : PartiallyTemporalNetwork

        """

        TN = super().from_tedges(tedges, normalise=normalise)
        if temporal_nodes is None:
            TN._temporal_nodes = TN.nodes
        else:
            TN._temporal_nodes = temporal_nodes
        if temporal_edges is None:
            TN._temporal_edges = TN.edges_aggregated()
        else:
            TN._temporal_edges = temporal_edges

        return TN

    @classmethod
    def from_edge_timeseries(
        cls, edge_timeseries, temporal_nodes=None, temporal_edges=None, normalise="max"
    ):
        """Creates a PartiallyTemporalNetwork from a DataFrame of edge timeseries

        All edges in the network are those of the timeseries, and nodes are extracted from edge names

        Parameters
        ----------
        edge_timeseries : pandas.DataFrame
            Dataframe where each row is a timeseries, with index as edge names and columns as times
        temporal_nodes : list of (str or int)
            List of temporal nodes
        temporal_edges : list of tuples
            List of temporal edges
        normalise : {'max', 'minmax'}
            Choice of normalsation of the edge timeseries

        Returns
        -------
        PartiallyTemporalNetwork

        """

        TN = super().from_edge_timeseries(edge_timeseries, normalise=normalise)
        if temporal_nodes is None:
            TN._temporal_nodes = TN.nodes
        else:
            TN._temporal_nodes = temporal_nodes
        if temporal_edges is None:
            TN._temporal_edges = TN.edges_aggregated()
        else:
            TN._temporal_edges = temporal_edges
        return TN

    @classmethod
    def from_node_timeseries(cls, node_timeseries, normalise="max"):
        """Creates a partially temporal network by combining node timeseries into edge timeseries.

        By construction, the underlying static network created is always fully connected.

        Parameters
        ----------
        node_timeseries : pandas.DataFrame
            Timeseries of nodes, indexed by node name and times as columns
        normalise : {'max', 'minmax'}
            Choice of normalsation of the edge timeseries

        Returns
        -------
        PartiallyTemporalNetwork
        """
        TN = super().from_node_timeseries(node_timeseries, normalise=normalise)
        TN._temporal_nodes = TN.nodes
        TN._temporal_edges = TN.edges_aggregated()
        return TN

    @classmethod
    def from_static_network_and_tedges(
        cls, static_network, tedges, static_edge_default_weight=None, normalise="max"
    ):
        """Creates a partially temporal network by combining a static network with tedges

        Parameters
        ----------
        static_network : networkx.Graph
            Static network into which to integrate the temporal information
        tedges : pandas.DataFrame or list of tuples
            Tedges must be of the form (i, j, t, weight)
        static_edge_default_weight : float, optional
            Weight to use for edges that have no temporal information
        normalise : {'max', 'minmax'}
            Choice of normalsation of the edge timeseries

        Returns
        -------
        PartiallyTemporalNetwork

        """

        tedges = _process_input_tedges(tedges)
        # CHECK not necessary?
        # if 'weight' not in tedges.columns :
        #    tedges['weight'] = 1 # add column with weight 1

        # convert static network's edges to DataFrame
        static_network_edges = pd.DataFrame(static_network.edges)
        static_network_edges.columns = ["static_i", "static_j"]

        # sort nodes in each row, for undirected edges
        static_network_edges[["static_i", "static_j"]] = np.sort(
            static_network_edges[["static_i", "static_j"]], axis=1
        )
        tedges[["i", "j"]] = np.sort(tedges[["i", "j"]], axis=1)

        # check that all static network edges have temporal info
        edges_aggregated = set(tedges[["i", "j"]].itertuples(index=False, name=None))
        missing_edges = list(
            set(static_network.edges).difference(edges_aggregated)
        )  # edges with no temporal information
        if not missing_edges:
            print("INFO: all edges have temporal information. This could be a TempNet.")

        # perform merge TODO check this /!\
        # Keep all edges present in the static network, and only those
        # Add all time edges corresponding to those
        # For edges that have no temporal information (no corresponding tedge), sets t and weight as Nan
        tedges_merged = pd.merge(
            static_network_edges,
            tedges,
            how="left",
            left_on=["static_i", "static_j"],
            right_on=["i", "j"],
        )

        if (
            static_edge_default_weight is None
        ):  # remove all edges without temporal information
            tedges_final = tedges_merged.dropna()
            temporal_edges = [
                edge for edge in edges_aggregated if edge not in missing_edges
            ]
            tedges_final = tedges_final[["i", "j", "t", "weight"]]
        else:  # add default weight across all timepoints for edges without temporal information
            if missing_edges:
                times = (
                    tedges["t"]
                    .drop_duplicates()
                    .to_frame()
                    .assign(weight=static_edge_default_weight)
                )
                tedges_missing = tedges_merged[tedges_merged["t"].isnull()]
                tedges_static = tedges_missing[["static_i", "static_j"]].assign(
                    weight=static_edge_default_weight
                )
                tedges_static = tedges_static.merge(times, on="weight")[
                    ["static_i", "static_j", "t", "weight"]
                ]
                tedges_static.columns = ["i", "j", "t", "weight"]

                tedges_temporal = tedges_merged.dropna()[
                    ["static_i", "static_j", "t", "weight"]
                ]
                tedges_temporal.columns = ["i", "j", "t", "weight"]

                tedges_final = pd.concat([tedges_temporal, tedges_static])
                temporal_edges = sorted(
                    set(tedges_temporal[["i", "j"]].itertuples(index=False, name=None))
                )
            else:  # all edges have temporal information
                tedges_final = tedges
                temporal_edges = edges_aggregated

        temporal_nodes = list(set([node for edge in temporal_edges for node in edge]))

        TN = cls.from_tedges(
            tedges_final, temporal_nodes, temporal_edges, normalise=normalise
        )
        return TN
