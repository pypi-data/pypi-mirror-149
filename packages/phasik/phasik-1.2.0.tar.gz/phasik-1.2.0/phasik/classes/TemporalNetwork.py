"""
Base class for temporal networks
"""

from copy import deepcopy
from itertools import combinations

import networkx as nx
import numpy as np
import pandas as pd

import phasik as pk

__all__ = ["TemporalNetwork", "_process_input_tedges"]


class TemporalNetwork:
    """Base class for temporal networks

    Temporal networks are networks with time-varying edges. They consist of nodes
    and edges, and latter can have time-varying weights.

    Attributes
    ----------
    nodes : list of (str or int)
        Sorted list of node names. Node names can be either strings or integers,
        but they all need to be of the same type.
    times : list of (int or float)
        Sorted list of times for which we have temporal information
    tedges : pandas.DataFrame
        Dataframe containing tedges, also called timestamped data (potentially weighted).
        Columns are ['i', 'j', 't', ('weight')] and each row represents a tedge.
    snapshots : numpy array
        Array of shape (T, N, N) storing the instantaneous values of
        the adjacency matrix A_{ij}(t).

    """

    def __init__(self):
        self._nodes = []
        self._times = []
        self._tedges = pd.DataFrame()
        self._snapshots = np.zeros((1,))

    @property
    def nodes(self):
        """Returns a list of nodes in the TemporalNetwork"""
        return self._nodes

    @property
    def times(self):
        """Returns a list of times in the TemporalNetwork"""
        return self._times

    @property
    def tedges(self):
        """Returns a DataFrame of tedges the TemporalNetwork"""
        return self._tedges

    @property
    def snapshots(self):
        """Returns a numpy array of snapshots in the TemporalNetwork"""
        return self._snapshots

    def __len__(self):
        """Returns the number of nodes in the TemporalNetwork"""
        return len(self._nodes)

    def __str__(self):
        """Returns summary information about the TemporalNetwork"""
        return f"{type(self)} with {self.N()} nodes and {self.T()} times"

    def __iter__(self):
        """Returns an iterable over nodes"""
        return iter(self._nodes)

    def __contains__(self, node):
        """Returns True if node is a node, False otherwise. Use as 'node in TN'."""
        try:
            return node in self._nodes
        except TypeError:
            return False

    def N(self):
        """Returns the number of nodes"""
        return len(self._nodes)

    def T(self):
        """Returns the number of times"""
        return len(self._times)

    def shape(self):
        """Returns the shape (N,T) of the TemporalNetwork"""
        return self.N(), self.T()

    def number_of_edges(self):
        """Returns the number of edges in the aggregated network"""
        return len(self.edges_aggregated())

    def is_weighted(self):
        """Returns True if tedges are weighted"""
        return "weight" in self._tedges.columns

    def has_node(self, node):
        """Returns True if node is in the TemporalNetwork"""
        return node in self._nodes

    def has_time(self, time):
        """Returns True if time is in the TemporalNetwork"""
        return time in self._times

    def has_tedge(self, tedge):
        """Returns True if tedge is in the TemporalNetwork, regardless of its weight"""
        if len(tedge) == 3:
            u, v, t = tedge
        elif len(tedge) == 4:
            u, v, t, _ = tedge
        else:
            raise Exception("Tedge must be of length 3 or 4")
        # /!\ tedge must be sorted, only checking one orientation
        return (
            (self._tedges["i"] == u)
            & (self._tedges["j"] == v)
            & (self._tedges["t"] == t)
        )

    def _add_nodes(self, nodes_to_add):
        """Add multiple nodes to the TemporalNetwork, without updating it further

        Parameters
        ----------
        nodes_to_add : list of str or int
            List of nodes to add

        Returns
        -------
        None

        """
        self._nodes += nodes_to_add
        self._nodes = sorted(set(self._nodes))

    def _add_times(self, times_to_add):
        """Add multiple times to the TemporalNetwork, without updating it further

        Parameters
        ----------
        nodes_to_add : list of str or int
            List of nodes to add

        Returns
        -------

        """
        self._times += times_to_add
        self._times = sorted(set(self._times))

    def add_tedges(self, tedges_to_add):
        """Adds multiple tedges (optionally weighted)

        Parameters
        ----------
        tedges_to_add : DataFrame or list of tuples

        Returns
        -------
        None

        """
        tedges_to_add = _process_input_tedges(tedges_to_add)
        self._tedges = self._tedges.append(tedges_to_add)
        self._tedges = self._tedges.drop_duplicates(subset=["i", "j", "t"], keep="last")
        # sort?

        # update nodes and times first to update their indices
        times_to_add = tedges_to_add["t"].to_list()
        nodes_to_add = tedges_to_add[["i", "j"]].to_numpy().flatten().tolist()

        self._add_nodes(nodes_to_add)
        self._add_times(times_to_add)

        # update snapshots
        self._compute_snapshots()  # computes them from scratch

    def _compute_snapshots(self):
        """Computes the snapshots from scratch from the tedges"""

        snapshots = np.zeros((self.T(), self.N(), self.N()))
        for row in self._tedges.itertuples(index=False):
            tedge = (row.i, row.j, row.t)
            if "weight" in self._tedges.columns:
                weight = row.weight
            else:
                weight = 1

            i, j, i_t = self._tedge_to_indices(tedge)
            snapshots[i_t, i, j] = weight
            snapshots[i_t, j, i] = weight  # undirected edges

        self._snapshots = snapshots

    def _node_index(self, node):
        """Returns the index of node 'node'."""
        return self._nodes.index(node)

    def _time_index(self, time):
        """Returns the index of time 'time'."""
        return self._times.index(time)

    def _tedge_to_indices(self, tedge):
        """Returns the indices of the nodes and time in 'tedge'."""
        u, v, t = tedge[:3]  # discard potential weight
        i = self._node_index(u)
        j = self._node_index(v)
        i_t = self._time_index(t)
        return i, j, i_t

    def _edge_to_indices(self, edge):
        """Returns the indices of the nodes in 'edge'."""
        u, v = edge
        i = self._node_index(u)
        j = self._node_index(v)
        return i, j

    def neighbors(self):
        """Returns a dict of neighbors (in aggregate network)"""
        G_agg = self.aggregated_network()
        # get rid of weight dicts
        return {
            node: list(values.keys())
            for node, values in dict(G_agg.adjacency()).items()
        }

    # TODO filter out non-temporal edges
    def edge_timeseries(self, edges=None):
        """Returns dict of edge time series. Keys are edge names and values are timeseries

        Parameters
        ----------
        edges : list of tuples
            List of edges wanted, e.g. [('A, B')]. If None (default), all edges in the temporal network are used.

        Returns
        -------
        all_series : dict
            Dictionary with edge names as keys (as 'A-B'), and timeseries as values.

        """
        # all_series = {'-'.join(sorted([str(self._nodes[i]), str(self._nodes[j])])) : self._snapshots[:, i, j]
        #             for i in range(self.N()) for j in range(i)}

        if edges is None:
            if isinstance(self, pk.PartiallyTemporalNetwork):
                edges = self.temporal_edges
            else:
                edges = self.edges_aggregated()

        all_series = {}
        for edge in edges:
            u, v = edge
            i, j = self._edge_to_indices(edge)
            edge_name = "-".join(edge)
            all_series[edge_name] = self._snapshots[:, i, j]

        # if isinstance(self, pk.PartiallyTemporalNetwork) : # only keep time series that contain temporal information
        #     return {edge : series for edge, series in all_series.items() if tuple(edge.split('-')) in self.temporal_edges}
        # else :
        #     return all_series

        return all_series

    def tedges_of_edge(self, edge, return_mask=True, reverse=False):
        """Returns a filtered DataFrame containing only the tedges of edge 'edge'.

        Optionally, return the boolean mask to filter the original DataFrame.

        Parameters
        ----------
        edge : tuple
            Edge used to filter tedges
        return_mask : bool, optional
            If True (default), return boolean mask to filter the original DataFrame
        reverse : bool, optional
            If True, return the Dataframe obtained by filtered with logically opposite mask,
            i.e. all tedges except those of edge 'edge'.

        Returns
        -------
        None

        """
        edge = tuple(sorted(edge))
        u, v = edge

        if edge not in self.edges_aggregated():
            raise ValueError(f"Edge {edge} not an edge of the temporal network")

        mask = (self._tedges["i"] == u) & (self._tedges["j"] == v)
        if reverse:
            mask = np.logical_not(mask)

        if return_mask:
            return self._tedges[mask], mask
        else:
            return self._tedges[mask]

    def tedges_of_node(self, node, return_mask=True, reverse=False):
        """Returns a filtered DataFrame containing only the tedges of node 'node'.

        Optionally, return the boolean mask to filter the original DataFrame.

        Parameters
        ----------
        node : str or int
            Node used to filter tedges
        return_mask : bool, optional
            If True (default), return boolean mask to filter the original DataFrame
        reverse : bool, optional
            If True, return the Dataframe obtained by filtered with logically opposite mask,
            i.e. all tedges except those of node 'node'.

        Returns
        -------

        """
        if not self.has_node(node):
            raise ValueError(f"Node {node} not a node of the temporal network")

        mask = (self._tedges["i"] == node) | (self._tedges["j"] == node)
        if reverse:
            mask = np.logical_not(mask)

        if return_mask:
            return self._tedges[mask], mask
        else:
            return self._tedges[mask]

    def aggregated_network(self, time_indices=None, output="weighted"):
        """Returns a time-aggregated network as a networkx.Graph

        Parameters
        ----------
        time_indices : list of int, optional
            Indices of times over which to aggregate the network (default: all times).
        output : {'weighted', 'averaged', 'binary', 'normalised'}, optional
            Determines the type of output edge weights

        Returns
        -------
        G_agg : networkx Graph
            Aggregated network

        """
        if time_indices is None:
            time_indices = range(self.T())

        adj_aggregated = self._snapshots[time_indices].sum(axis=0)
        n_t = len(time_indices)

        if output == "weighted":
            pass
        elif output == "averaged":
            adj_aggregated /= n_t
        elif output == "binary":
            tol = 1e-3
            adj_aggregated[adj_aggregated > tol] = 1
        elif output == "normalised":
            adj_aggregated /= np.max(adj_aggregated)

        G_agg = nx.Graph(adj_aggregated)
        G_agg = nx.relabel_nodes(G_agg, {i: node for i, node in enumerate(self._nodes)})

        return G_agg

    def network_at_time(self, time_index, output="weighted"):
        """Returns the temporal network at time 'time' as a networkx.Graph

        Parameters
        ----------
        time_index : int
            Time index at which we want the temporal network
        output : {'weighted', 'averaged', 'binary', 'normalised'}, optional
            Determines the type of output edge weights

        Returns
        -------
        networkx Graph
            Network at time 'time'
        """

        return self.aggregated_network(time_indices=[time_index], output=output)

    def edges_aggregated(self):
        """Returns a list of edges in the aggregated network

        Parameters
        ----------
        None

        Returns
        -------
        list of tuples
        """
        # note : some class methods build complete networks, in which case all edges will be included
        G_agg = self.aggregated_network()
        return list(G_agg.edges)

    # TODO there is a bug in here not sure what
    def to_partially_temporal(self):
        """Returns a copy of the temporal network as a PartiallyTemporalNetwork"""

        tedges = deepcopy(self._tedges)
        return pk.PartiallyTemporalNetwork.from_tedges(tedges)

    def discard_temporal_info_from_edge(self, edge, default_weight=1, reverse=False):
        """Discards temporal information from 'edge' by setting its weight to a constant

        Returns a copy of the temporal network with the new edge weights

        Parameters
        ----------
        edge : tuple of int or str
           Edge from which to discard temporal information
        default_weight : float, optional
           Value used for the edges with no temporal information
        reverse : bool, optional
           If True, discard temporal info from all edges except 'edge'.

        Returns
        -------
        TN_modified : TemporalNetwork

        """
        # after discarding temporal information, we need to have a PartiallyTemporalNetwork
        if isinstance(self, pk.PartiallyTemporalNetwork):
            TN_modified = deepcopy(self)
        else:
            TN_modified = self.to_partially_temporal()

        if edge not in TN_modified.edges_aggregated():
            raise ValueError(f"Edge {edge} not an edge in the temporal network.")
        elif edge not in TN_modified.temporal_edges:
            raise ValueError(f"Edge {edge} not a temporal edge.")

        # udpate tedges
        _, mask = TN_modified.tedges_of_edge(edge, reverse=reverse)
        TN_modified._tedges.loc[mask, "weight"] = default_weight

        # update snapshots
        if not reverse:
            i, j = TN_modified._edge_to_indices(edge)  # one edge to modify
            TN_modified.snapshots[:, i, j] = default_weight
            TN_modified.snapshots[:, j, i] = default_weight
        else:
            for edge_to_modify in self.temporal_edges:
                if edge_to_modify != edge:
                    i, j = TN_modified._edge_to_indices(
                        edge_to_modify
                    )  # one edge to modify
                    TN_modified.snapshots[:, i, j] = default_weight
                    TN_modified.snapshots[:, j, i] = default_weight

        # update temporal nodes and edges
        if reverse:
            TN_modified.temporal_nodes = sorted(edge)
            TN_modified.temporal_edges = [edge]
        else:
            TN_modified.temporal_edges.remove(edge)
            temporal_nodes = np.unique(TN_modified.temporal_edges)
            TN_modified.temporal_nodes = list(temporal_nodes)
            # the following does not work because nodes might appear in other tedges
            # TN_modified.temporal_nodes.remove(edge[0])
            # TN_modified.temporal_nodes.remove(edge[1])

        return TN_modified

    def discard_temporal_info_from_node(self, node, default_weight=1, reverse=False):
        """Discards temporal information from 'node' by setting the weight of its edges to a constant

        Returns a copy of the temporal network with the new edge weights

        Parameters
        ----------
        node : int or str
            Node from which to discard temporal information
        default_weight : float, optional
            Value used for the edges with no temporal information
        reverse : bool, optional
            If True, discard temporal info from all nodes except 'node'.

        Returns
        -------
        TN_modified : TemporalNetwork

        """
        # after discarding temporal information, we need to have a PartiallyTemporalNetwork
        if isinstance(self, pk.PartiallyTemporalNetwork):
            TN_modified = deepcopy(self)
        else:
            TN_modified = self.to_partially_temporal()

        if not TN_modified.has_node(node):
            raise ValueError(f"Node {node} not an node in the temporal network.")
        elif node not in TN_modified.temporal_nodes:
            raise ValueError(f"Node {node} not a temporal node.")

        # update tedges
        _, mask = TN_modified.tedges_of_node(node, reverse=reverse)
        TN_modified._tedges.loc[mask, "weight"] = default_weight

        #        temporal_edges_selected = [tuple(sorted([node, u])) for u in TN_modified.temporal_neighbors()[node]]
        temporal_edges_selected = [edge for edge in self.temporal_edges if node in edge]

        # update snapshots
        if not reverse:
            for edge_to_modify in temporal_edges_selected:
                i, j = TN_modified._edge_to_indices(
                    edge_to_modify
                )  # one edge to modify
                TN_modified.snapshots[:, i, j] = default_weight
                TN_modified.snapshots[:, j, i] = default_weight
        else:
            TN_modified._compute_snapshots()
        #            for node_to_modify in self.temporal_nodes :
        #                if node_to_modify != node :
        #                    i = TN_modified._node_index(node_to_modify) # one edge to modify
        #                    TN_modified.snapshots[:, i, :] = default_weight
        #                    TN_modified.snapshots[:, :, i] = default_weight

        # update temporal nodes and edges

        if reverse:
            TN_modified.temporal_nodes = [node]
            TN_modified.temporal_edges = temporal_edges_selected
        else:
            TN_modified.temporal_nodes.remove(node)
            TN_modified.temporal_edges = [
                edge
                for edge in TN_modified.temporal_edges
                if edge not in temporal_edges_selected
            ]

        return TN_modified

    @classmethod
    def from_tedges(cls, tedges, normalise=None):
        """Creates a TemporalNetwork from a dataframe of tedges

        Parameters
        ----------
        tedges : pandas.DataFrame or list of tuples
            List of tedges with 'i', 'j', 't', and optionally 'weight'
            If DataFrame, these are the name of the columns, and each row contains a tedge
        normalise : {'max', 'minmax'}
            Choice of normalsation of the edge timeseries

        Returns
        -------
        TN : TemporalNetwork

        """

        tedges = _process_input_tedges(tedges)
        if normalise:
            if "weight" not in tedges.columns:
                raise ValueError(
                    "Cannot normalise weights because edges are unweighted"
                )

        if normalise == None:
            pass
        elif normalise == "max":
            grouped = tedges.groupby(["i", "j"])["weight"]
            maxes = grouped.transform("max")
            tedges["weight"] = tedges["weight"] / maxes
            tedges["weight"] = tedges["weight"].fillna(1)
        elif normalise == "minmax":
            grouped = tedges.groupby(["i", "j"])["weight"]
            maxes = grouped.transform("max")
            mins = grouped.transform("min")
            tedges["weight"] = (tedges["weight"] - mins) / (maxes - mins)
            # In cases where max = min we'll have a division by zero error.
            tedges["weight"] = tedges["weight"].fillna(0.5)
        else:
            raise ValueError("Unknown value for 'normalise'")

        TN = cls()
        TN.add_tedges(tedges)
        return TN

    @classmethod
    def from_edge_timeseries(cls, edge_timeseries, normalise="max"):
        """Creates a TemporalNetwork from a DataFrame of edge timeseries

        All edges in the network are those of the timeseries, and nodes are extracted from edge names

        Parameters
        ----------
        edge_timeseries : pandas.DataFrame
            Dataframe where each row is a timeseries, with index as edge names and columns as times
        normalise : {'max', 'minmax', None}
            Choice of normalsation of the edge timeseries

        Returns
        -------
        TemporalNetwork

        """

        tedges = convert_edge_timeseries_to_tedges(edge_timeseries)
        return cls.from_tedges(tedges, normalise)

    @classmethod
    def from_node_timeseries(cls, node_timeseries, normalise="max"):
        """Creates a temporal network by combining node timeseries into edge timeseries.

        By construction, the underlying static network created is always fully connected.

        Parameters
        ----------
        node_timeseries : pandas.DataFrame
            Timeseries of nodes, indexed by node name and times as columns
        normalise : {'max', 'minmax', None}
            Choice of normalsation of the edge timeseries

        Returns
        -------
        TemporalNetwork
        """

        edge_series = convert_node_to_edge_timeseries(node_timeseries)

        return cls.from_edge_timeseries(edge_series, normalise=normalise)

    @classmethod
    def from_static_network_and_tedges(
        cls,
        static_network,
        tedges,
        static_edge_default_weight=None,
        normalise="max",
        quiet=True,
    ):
        """Creates a temporal network by combining a static network with tedges

        If all edges of the static network are represented in the tedges, create a temporal network
        by setting time-varying edge weights from the tedges.
        Raises an Exception if not all edges have temporal information.

        Parameters
        ----------
        static_network : networkx.Graph
            Static network into which to integrate the temporal information
        tedges : pandas.DataFrame or list of tuples
            Tedges must be of the form (i, j, t, weight)
        static_edge_default_weight : float
            Weight to use for edges without temporal information
        normalise : {'max', 'minmax', None}
            Choice of normalsation of the edge timeseries
        quiet : bool
            If True (default), print minimum informative messages
        Returns
        -------

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
        static_network_edges_set = set(
            static_network_edges[["static_i", "static_j"]].itertuples(
                index=False, name=None
            )
        )
        # missing_edges = set(static_network.edges).difference(edges_aggregated)
        missing_edges = static_network_edges_set.difference(edges_aggregated)
        if missing_edges == set():
            # perform merge TODO check this /!\
            tedges_merged = pd.merge(
                static_network_edges,
                tedges,
                how="left",
                left_on=["static_i", "static_j"],
                right_on=["i", "j"],
            )
            tedges_merged = tedges_merged.drop(columns=["static_i", "static_j"])
            return cls.from_tedges(tedges_merged, normalise=normalise)
        else:  # create a PartiallyTemporalNetwork

            print(
                f"WARNING: {len(missing_edges)}/{len(static_network_edges)} edges "
                f"in the static network have no temporal information. \n"
                f"A PartiallyTemporalNetwork is created instead."
            )

            if not quiet:
                print(f"Edges with no temporal information:")
                print(missing_edges)

            return pk.PartiallyTemporalNetwork.from_static_network_and_tedges(
                static_network, tedges, static_edge_default_weight, normalise=normalise
            )

            # Exception(f"{len(missing_edges)} edges in the static network have no temporal information. "
            #               f"Create a PartiallyTemporalNetwork instead.")

    @classmethod
    def from_static_network_and_edge_timeseries(
        cls,
        static_network,
        edge_timeseries,
        static_edge_default_weight=None,
        normalise=None,
        quiet=False,
    ):
        """Creates a temporal network by combining a static network with edge timeseries

        If all edges of the static network are represented in the timeseries, create a temporal network
        by setting time-varying edge weights from the tedges.
        If not all edges  of the static network, creates a partially temporal network.

        Parameters
        ----------
        static_network : nx.Graph
            Static network into which to integrate the temporal information
        edge_timeseries : Dataframe
            Dataframe with indexed (rows) by edge names (formatted as 'A-B') and
            with columns as times. Entries of the Dataframe represent the weight of
            that edge at that time.
        static_edge_default_weight : float
            Weight to use for edges without temporal information
        normalise : {'max', 'minmax', None}
            Choice of normalsation of the edge timeseries
        quiet : bool
            If True (default), print minimum informative messages

        Returns
        -------
        TemporalNetwork

        """

        tedges = convert_edge_timeseries_to_tedges(edge_timeseries)

        return cls.from_static_network_and_tedges(
            static_network, tedges, static_edge_default_weight, normalise, quiet
        )

    @classmethod
    def from_static_network_and_node_timeseries(
        cls,
        static_network,
        node_timeseries,
        combine_node_weights=lambda x, y: x * y,
        static_edge_default_weight=None,
        normalise=None,
        quiet=False,
    ):
        """Creates a temporal network by combining a static network with node timeseries

        Edge time series are generated for the subset of edges in the 'static_network'
        that have both nodes in the 'node_timeseries', by combining their time series.
        These edge times series are used to set the time-varying weights of the corresponding
        edges in the temporal network.
        If not all edges have temporal information, creates a partially temporal network.

        Parameters
        ----------
        static_network : nx.Graph
            Static network into which to integrate the temporal information
        node_timeseries : Dataframe
            Dataframe with indexed (rows) by node names and
            with columns as times. Entries of the Dataframe represent the value of
            that node at that time.
        combine_node_weights : function
            Function that determines how two node timeseries are combined to generate
            and edge timeseries. By default, the two node timeseries are multiplied.
        static_edge_default_weight : float
            Weight to use for edges without temporal information
        normalise : {'max', 'minmax'}
            Choice of normalsation of the edge timeseries
        quiet : bool
            If True (default), print minimum informative messages

        Returns
        -------
        TemporalNetwork

        """

        # only keep node timeseries from nodes that are in the static network
        nodes_static = list(static_network.nodes)
        nodes_temporal_all = list(node_timeseries.index)
        nodes_temporal = [node for node in nodes_temporal_all if node in nodes_static]

        node_series_in_network = node_timeseries[
            node_timeseries.index.isin(nodes_temporal)
        ]

        # combine node timeseries to obtain edge timeseries, only edges that a present in the static network
        edge_series = convert_node_to_edge_timeseries(
            node_series_in_network,
            combine_node_weights,
            static_edges=list(static_network.edges),
        )

        return cls.from_static_network_and_edge_timeseries(
            static_network, edge_series, static_edge_default_weight, normalise, quiet
        )


def _process_input_tedges(tedges):
    """Check that input is valid and convert to DataFrame id needed

    Parameters
    ----------
    tedges : (list of tuples) or Dataframe
        A list of (optionally weighted) tedges (i, j, t, weight) as tuples or in a Dataframe

    Returns
    -------
    tedges : pandas DataFrame

    """

    if isinstance(tedges, list):  # convert to DataFrame
        if all([isinstance(tedge, tuple) for tedge in tedges]):
            if all([len(tedge) == 3 for tedge in tedges]):
                columns = ["i", "j", "t"]
                tedges = pd.DataFrame(data=tedges, columns=columns)
            elif all([len(tedge) == 4 for tedge in tedges]):
                columns = ["i", "j", "t", "weight"]
                tedges = pd.DataFrame(data=tedges, columns=columns)
            else:
                raise ValueError(
                    "Tedges in list must have length 3 (i, j, t) or 4 (i, j, t, weight)"
                )
        else:
            raise TypeError("All tedges in list should be tuples")
    elif isinstance(tedges, pd.DataFrame):  # check columns
        if (list(tedges.columns) == ["i", "j", "t"]) or (
            list(tedges.columns) == ["i", "j", "t", "weight"]
        ):
            pass
        else:
            print(tedges)
            raise ValueError(
                "Tedge dataframe must have columns (i, j, t) or  (i, j, t, weight)"
            )
    else:
        raise TypeError(
            "Invalid type of input tedges: should be a list of tuples or a DataFrame"
        )

    # remove self-edges
    tedges = tedges[tedges["i"] != tedges["j"]]

    tedges = tedges.sort_values(by=["i", "j", "t"])

    return tedges


def convert_edge_timeseries_to_tedges(edge_timeseries):
    """Converts edge timeseries to DataFrame of tedges

    Note: since all timeseries have the same number of timepoints, many rows in the tedges might have a zero weight

    Parameters
    ----------
    edge_timeseries : pandas.DataFrame
        Time series indexed by edge name and where columns are timepoints

    Returns
    -------
    tedges : pandas.DataFrame

    """
    # series_df = pd.DataFrame.from_dict(edge_timeseries, orient="index", columns=times)
    series_stack = edge_timeseries.stack()  # times are second index now
    series_stack = series_stack.to_frame("weight")
    tedges = series_stack.reset_index()  # set multindex (edge, time) as columns
    tedges[["i", "j"]] = tedges["level_0"].str.split(
        "-", expand=True
    )  # split edge as columns 'i' and 'j'
    del tedges["level_0"]
    tedges.columns = ["t", "weight", "i", "j"]  # rename
    tedges = tedges[["i", "j", "t", "weight"]]  # reorder

    return tedges


def convert_node_to_edge_timeseries(
    node_series, combine=lambda x, y: x * y, static_edges=None
):
    """Convert node timeseries to edge timeseries

    Parameters
    ----------
    node_series : pandas.DataFrame
        Node timeseries, indexed by node names and where columns are times
    combine : function
        Function to use to combine two node time series into one edge time series
    static_edges : list of tuples
        List of edges in static network. If None (default), considers fully connected network between nodes

    Returns
    -------
    edge_series : pd.DataFrame
        Dataframe containing edge timeseries, indexed by edge name 'A-B', columns are times, and entries are weights
    """

    edge_series_dict = {}

    #     node_series = node_series.sort_index() # to ensure that intersection later contains all edges

    if static_edges is None:
        static_edges = combinations(node_series.index, 2)

    all_potential_edges = combinations(node_series.index, 2)

    #     edges = set(static_edges).intersection(all_potential_edges)

    # ordering of nodes inside each edge is not guaranteed to be the same in those lists
    # so to ensure the right intersection, we need to sort or use frozensets
    set1 = {frozenset(edge) for edge in static_edges}
    set2 = {frozenset(edge) for edge in all_potential_edges}
    set3 = set1.intersection(set2)

    edges = [
        tuple(edge) for edge in set3
    ]  # list of edges in static network with temporal information

    for edge in edges:
        edge_name = "-".join(edge)
        u, v = edge
        series = combine(node_series.loc[u], node_series.loc[v])
        edge_series_dict[edge_name] = series

    edge_series = pd.DataFrame.from_dict(edge_series_dict, orient="index")

    return edge_series
