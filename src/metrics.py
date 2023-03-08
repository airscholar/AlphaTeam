"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Compute the metrics for the NetworkX graphs
"""

# ----------------------------------------------------------------------------------------

# Imports
import pandas as pd
import networkx as nx
import numpy as np


# ----------------------------------------------------------------------------------------


def compute_global_metrics(networkx_):
    """
    :Function: Compute the global metrics for the NetworkX graph (directed and undirected)
    :param networkx_: NetworkX Digraph
    :return: Pandas dataframe with the metrics and values (directed and undirected)
    """
    directed = compute_metrics(networkx_)  # compute for directed
    undirected = compute_metrics(networkx_.to_undirected())  # compute for undirected

    return pd.merge(directed, undirected, how='inner',
                    on='Metrics').rename(columns={'Values_x': 'Directed', 'Values_y': 'Undirected'})


# ----------------------------------------------------------------------------------------


def compute_metrics(networkx_):
    """
    :Function: Compute the generals metrics for the NetworkX graph
    :param networkx_: NetworkX Digraph
    :return: Pandas dataframe with the metrics and values
    """

    df = pd.DataFrame()  # return pandas dataframe

    try:
        clustering_coefficient = nx.average_clustering(networkx_)
    except:
        clustering_coefficient = 0

    try:
        avg_shortest_path_length = nx.average_shortest_path_length(networkx_)
    except:
        avg_shortest_path_length = 0

    try:
        diameter = nx.diameter(networkx_)
    except:
        diameter = 0

    try:
        radius = nx.radius(networkx_)
    except:
        radius = 0

    records = [
        {"Metrics": "Clustering Coefficient", "Values": clustering_coefficient},
        {"Metrics": "Avg. Shortest Path Length", "Values": avg_shortest_path_length},
        {"Metrics": "Diameter", "Values": diameter},
        {"Metrics": "Radius", "Values": radius},
        {"Metrics": "Number of Nodes", "Values": networkx_.number_of_nodes()},
        {"Metrics": "Number of Edges", "Values": networkx_.number_of_edges()},
        {"Metrics": "Density", "Values": nx.density(networkx_)},
        {"Metrics": "Transitivity", "Values": nx.transitivity(networkx_)},
        {"Metrics": "Avg. Degree", "Values": np.mean(list(dict(networkx_.degree()).values()))},
        {"Metrics": "Avg. Clustering", "Values": np.mean(list(nx.clustering(networkx_).values()))},
        {"Metrics": "Avg. Eigenvector Centrality",
         "Values": np.mean(list(nx.eigenvector_centrality(networkx_).values()))},
        {"Metrics": "Avg. Betweenness Centrality",
         "Values": np.mean(list(nx.betweenness_centrality(networkx_).values()))},
        {"Metrics": "Avg. Closeness Centrality", "Values": np.mean(list(nx.closeness_centrality(networkx_).values()))},
        {"Metrics": "Avg. Degree Centrality", "Values": np.mean(list(nx.degree_centrality(networkx_).values()))},
        {"Metrics": "Avg. Page Rank", "Values": np.mean(list(nx.pagerank(networkx_).values()))},
        {"Metrics": "Avg. Load Centrality", "Values": np.mean(list(nx.load_centrality(networkx_).values()))}
    ]

    for record in records:
        df = pd.concat([df, pd.DataFrame(record, index=[0])], ignore_index=True)

    return df

# ----------------------------------------------------------------------------------------


def compute_connectivity(networkx_):
    return 0

# ----------------------------------------------------------------------------------------

# def compute_node_metrics(networkx, directed=True):
#     """
#     :Function: Compute the node metrics for the NetworkX graph
#     :param networkx: NetworkX Digraph
#     :param directed: Boolean
#     :return: Pandas dataframe with the metrics and values
#     """
#     if not directed:
#         return compute_node_metrics(networkx.to_undirected(), directed=True)
#
#     degree_centrality = compute_degree_centrality(networkx)
#     closeness_centrality = compute_closeness_centrality(networkx)
#     betweeness_centrality = compute_betweeness_centrality(networkx)
#     eigen_centrality = compute_eigen_centrality(networkx)
#
#     df = pd.DataFrame([degree_centrality, closeness_centrality, betweeness_centrality, eigen_centrality]).T
#     df.columns = ['Degree Centrality', 'Closeness Centrality', 'Betweeness Centrality', 'Eigenvector Centrality']
#
#     return df

# ----------------------------------------------------------------------------------------


def compute_degree_centrality(networkx_, directed=True):
    """
    :Function: Compute the degree centrality for the NetworkX graph
    :param networkx_: NetworkX Digraph
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    if not directed:
        return compute_degree_centrality(networkx_.to_undirected(), directed=True)

    df = pd.DataFrame(nx.degree_centrality(networkx_).items(), columns=['Node', 'Degree Centrality'])
    return df


# ----------------------------------------------------------------------------------------


def compute_eigen_centrality(networkx_, directed=True):
    """
    :Function: Compute the eigenvector centrality for the NetworkX graph
    :param networkx_: NetworkX Digraph
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    if not directed:
        return compute_eigen_centrality(networkx_.to_undirected(), directed=True)

    df = pd.DataFrame(nx.eigenvector_centrality(networkx_).items(), columns=['Node', 'Eigenvector Centrality'])
    return df

# ----------------------------------------------------------------------------------------


def compute_closeness_centrality(networkx_, directed=True):
    """
    :Function: Compute the closeness centrality for the NetworkX graph
    :param networkx_: NetworkX Digraph
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    if not directed:
        return compute_closeness_centrality(networkx_.to_undirected(), directed=True)

    df = pd.DataFrame(nx.closeness_centrality(networkx_).items(), columns=['Node', 'Closeness Centrality'])
    return df

# ----------------------------------------------------------------------------------------


def compute_betweeness_centrality(networkx_, directed=True):
    """
    :Function: Compute the betweeness centrality for the NetworkX graph
    :param networkx_: NetworkX Digraph
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    if not directed:
        return compute_betweeness_centrality(networkx_.to_undirected(), directed=True)

    df = pd.DataFrame(nx.betweenness_centrality(networkx_).items(), columns=['Node', 'Betweeness Centrality'])
    return df

# ----------------------------------------------------------------------------------------


def get_shortest_path(networkx_, source, target, weight=None):
    return nx.shortest_path(networkx_, source=source, target=target, weight=weight)
