"""
Utility functions for static graphs
"""

import networkx as nx
import pandas as pd

__all__ = ["create_graph_from_interactions", "graph_size_info", "weighted_edges_as_df"]


def create_graph_from_interactions(filename, sheet, source, target):
    """Create a networkx.Graph from an excel sheet describing edges

    Parameters
    ----------
    filename : str
        Path to the excel file
    sheet : str
        Name of the sheet within the excel file
    source : str
        Name of the column containing the source nodes
    target : str
        Name of the column containing the target nodes

    Returns
    -------
    graph : networkx.Graph
    """

    interactions = pd.read_excel(filename, sheet_name=sheet)
    graph = nx.from_pandas_edgelist(interactions, source, target)
    return graph


def graph_size_info(graph):
    """Return basic size info on about graph"""
    return f"{len(graph)} nodes and {len(graph.edges)} edges"


def weighted_edges_as_df(network):
    """Returns a pandas.Dataframe of weighted edges sorted by weight,
    from a networkx.Graph.

    Columns are ['i', 'j', 'weight'] and each row represents a different edge

    Parameters
    ----------
    network : networkx.Graph
        A network from which to get weighted edges

    Returns
    -------
    pandas.DataFrame

    """
    edges_weighted = [(i, j, network[i][j]["weight"]) for (i, j) in network.edges]
    edges_weighted = sorted(edges_weighted, key=lambda row: row[2])[
        ::-1
    ]  # sort by weight
    edges_weighted_df = pd.DataFrame(edges_weighted, columns=["i", "j", "weight"])
    return edges_weighted_df
