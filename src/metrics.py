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


def compute_global_metrics(networkGraphs):
    """
    :Function: Compute the global metrics for the NetworkX graph (directed and undirected)
    :param network_graphs: Network Graphs
    :return: Pandas dataframe with the metrics and values (directed and undirected)
    """
    directed = compute_metrics(networkGraphs.DiGraph)  # compute for directed
    undirected = compute_metrics(networkGraphs.Graph)  # compute for undirected

    return pd.merge(directed, undirected, how='inner',
                    on='Metrics').rename(columns={'Values_x': 'Directed', 'Values_y': 'Undirected'})


# ----------------------------------------------------------------------------------------


def compute_metrics(networkx_):
    """
    :Function: Compute the generals metrics for the NetworkX graph
    :param networkx_: NetworkX graph
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

def compute_node_metrics(networkGraphs, directed=True):
    """
    :Function: Compute the node metrics for the NetworkX graph
    :param networkGraphs: Network Graphs
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    if not directed:
        degree_centrality = compute_degree_centrality(networkGraphs, directed=False)
        eigen_centrality = compute_eigen_centrality(networkGraphs, directed=False)
        closeness_centrality = compute_closeness_centrality(networkGraphs, directed=False)
        betweenness_centrality = compute_betweeness_centrality(networkGraphs, directed=False)
    else:
        degree_centrality = compute_degree_centrality(networkGraphs, directed=True)
        eigen_centrality = compute_eigen_centrality(networkGraphs, directed=True)
        closeness_centrality = compute_closeness_centrality(networkGraphs, directed=True)
        betweenness_centrality = compute_betweeness_centrality(networkGraphs, directed=True)

    # merge all into a single dataframe
    df = pd.merge(degree_centrality, eigen_centrality, how='inner', on='Node')
    df = pd.merge(df, closeness_centrality, how='inner', on='Node')
    df = pd.merge(df, betweenness_centrality, how='inner', on='Node')

    return df



# ----------------------------------------------------------------------------------------


def compute_degree_centrality(networkGraphs, directed=True):
    """
    :Function: Compute the degree centrality for the NetworkX graph
    :param network_graphs: Network Graphs
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """

    if not directed:
        degree_centrality = nx.degree_centrality(networkGraphs.Graph)
    else:
        degree_centrality = nx.degree_centrality(networkGraphs.DiGraph)

    df = pd.DataFrame(degree_centrality.items(), columns=['Node', 'Degree Centrality'])

    return df


# ----------------------------------------------------------------------------------------


def compute_eigen_centrality(networkGraphs, directed=True):
    """
    :Function: Compute the eigenvector centrality for the NetworkX graph
    :param network_graphs: Network Graphs
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """

    if not directed:
        eigen_centrality = nx.eigenvector_centrality(networkGraphs.Graph)
    else:
        eigen_centrality = nx.eigenvector_centrality(networkGraphs.DiGraph)

    df = pd.DataFrame(eigen_centrality.items(), columns=['Node', 'Eigenvector Centrality'])

    return df


# ----------------------------------------------------------------------------------------


def compute_closeness_centrality(networkGraphs, directed=True):
    """
    :Function: Compute the closeness centrality for the NetworkX graph
    :param network_graphs: Network Graphs
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """

    if not directed:
        closeness_centrality = nx.closeness_centrality(networkGraphs.Graph)
    else:
        closeness_centrality = nx.closeness_centrality(networkGraphs.DiGraph)

    df = pd.DataFrame(closeness_centrality.items(), columns=['Node', 'Closeness Centrality'])
    return df


# ----------------------------------------------------------------------------------------


def compute_betweeness_centrality(networkGraphs, directed=True):
    """
    :Function: Compute the betweeness centrality for the NetworkX graph
    :param network_graphs: Network Graphs
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    if not directed:
        betweeness_centrality = nx.betweenness_centrality(networkGraphs.Graph)
    else:
        betweeness_centrality = nx.betweenness_centrality(networkGraphs.DiGraph)

    df = pd.DataFrame(betweeness_centrality.items(),
                      columns=['Node', 'Betweeness Centrality'])
    return df


# ----------------------------------------------------------------------------------------


def get_shortest_path(networkGraphs, source, target, weight=None, directed=False):
    if not directed:
        return nx.shortest_path(networkGraphs.Graph, source, target, weight=weight)
    else:
        return nx.shortest_path(networkGraphs.DiGraph, source, target, weight=weight)
