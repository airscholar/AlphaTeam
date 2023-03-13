"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Compute the metrics for the NetworkX graphs
"""

# ----------------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from src.utils import memoize


# ----------------------------------------------------------------------------------------
# ------------------------------------ GLOBAL METRICS ------------------------------------
# ----------------------------------------------------------------------------------------
@memoize
def compute_global_metrics(networkGraphs):
    """
    :Function: Compute the global metrics for the NetworkX graph (directed and undirected)
    :param networkGraphs: Network Graphs
    :return: Pandas dataframe with the metrics and values (directed and undirected)
    """
    directed = compute_metrics(networkGraphs.DiGraph)  # compute for directed
    undirected = compute_metrics(networkGraphs.Graph)  # compute for undirected

    return pd.merge(directed, undirected, how='inner',
                    on='Metrics').rename(columns={'Values_x': 'Directed', 'Values_y': 'Undirected'})


# ----------------------------------------------------------------------------------------


@memoize
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
        clustering_coefficient = None

    try:
        avg_shortest_path_length = nx.average_shortest_path_length(networkx_)
    except:
        avg_shortest_path_length = None

    try:
        diameter = nx.diameter(networkx_)
    except:
        diameter = None

    try:
        radius = nx.radius(networkx_)
    except:
        radius = None

    try:
        avg_eigenvector_centrality = np.mean(list(nx.eigenvector_centrality(networkx_).values()))
    except:
        avg_eigenvector_centrality = None

    try:
        avg_closeness_centrality = np.mean(list(nx.closeness_centrality(networkx_).values()))
    except:
        avg_closeness_centrality = None

    try:
        avg_betweenness_centrality = np.mean(list(nx.betweenness_centrality(networkx_).values()))
    except:
        avg_betweenness_centrality = None

    try:
        avg_degree_centrality = np.mean(list(nx.degree_centrality(networkx_).values()))
    except:
        avg_degree_centrality = None

    try:
        avg_load_centrality = np.mean(list(nx.load_centrality(networkx_).values()))
    except:
        avg_load_centrality = None

    try:
        avg_pagerank = np.mean(list(nx.pagerank(networkx_).values()))
    except:
        avg_pagerank = None

    try:
        avg_clustering = np.mean(list(nx.clustering(networkx_).values()))
    except:
        avg_clustering = None

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
        {"Metrics": "Avg. Clustering", "Values": avg_clustering},
        {"Metrics": "Avg. Eigenvector Centrality",
         "Values": avg_eigenvector_centrality},
        {"Metrics": "Avg. Betweenness Centrality",
         "Values": avg_betweenness_centrality},
        {"Metrics": "Avg. Closeness Centrality", "Values": avg_closeness_centrality},
        {"Metrics": "Avg. Degree Centrality", "Values": avg_degree_centrality},
        {"Metrics": "Avg. Page Rank", "Values": avg_pagerank},
        {"Metrics": "Avg. Load Centrality", "Values": avg_load_centrality},
    ]

    for record in records:
        df = pd.concat([df, pd.DataFrame(record, index=[0])], ignore_index=True)

    return df


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
        load_centrality = compute_load_centrality(networkGraphs, directed=False)
    else:
        degree_centrality = compute_degree_centrality(networkGraphs, directed=True)
        eigen_centrality = compute_eigen_centrality(networkGraphs, directed=True)
        closeness_centrality = compute_closeness_centrality(networkGraphs, directed=True)
        betweenness_centrality = compute_betweeness_centrality(networkGraphs, directed=True)
        load_centrality = compute_load_centrality(networkGraphs, directed=True)

    # merge all into a single dataframe
    df = pd.merge(degree_centrality, eigen_centrality, how='inner', on='Node')
    df = pd.merge(df, closeness_centrality, how='inner', on='Node')
    df = pd.merge(df, betweenness_centrality, how='inner', on='Node')
    df = pd.merge(df, load_centrality, how='inner', on='Node')

    return df


# ----------------------------------------------------------------------------------------
# ------------------------------ CENTRALITY METRICS --------------------------------------
# ----------------------------------------------------------------------------------------
@memoize
def compute_degree_centrality(networkGraphs, directed=True):
    """
    :Function: Compute the degree centrality for the NetworkX graph
    :param networkGraphs: Network Graphs
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

@memoize
def compute_eigen_centrality(networkGraphs, directed=True):
    """
    :Function: Compute the eigenvector centrality for the NetworkX graph
    :param networkGraphs: Network Graphs
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

@memoize
def compute_closeness_centrality(networkGraphs, directed=True):
    """
    :Function: Compute the closeness centrality for the NetworkX graph
    :param networkGraphs: Network Graphs
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

@memoize
def compute_betweeness_centrality(networkGraphs, directed=True):
    """
    :Function: Compute the betweeness centrality for the NetworkX graph
    :param networkGraphs: Network Graphs
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
@memoize
def compute_load_centrality(networkGraphs, directed=True):
    """
    :Function: Compute the load centrality for the NetworkX graph
    :param networkGraphs: Network Graphs
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    if not directed:
        load_centrality = nx.load_centrality(networkGraphs.Graph)
    else:
        load_centrality = nx.load_centrality(networkGraphs.DiGraph)

    df = pd.DataFrame(load_centrality.items(), columns=['Node', 'Load Centrality'])
    return df


# ----------------------------------------------------------------------------------------
# ------------------------------ NODES METRICS ------------------------------------------
# ----------------------------------------------------------------------------------------

@memoize
def compute_nodes_degree(networkGraphs, directed=True):
    """
    :Function: Compute the node degree for the NetworkX graph
    :param networkGraphs: NetworkGraphs
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    if not directed:
        degree = nx.degree(networkGraphs.Graph)
    else:
        degree = nx.degree(networkGraphs.DiGraph)

    df = pd.DataFrame(degree, columns=['Node', 'Degree'])
    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_kcore(networkGraphs, directed=True):
    """
    :Function: Compute the k-core
    :param networkGraphs: NetworkGraphs
    :param directed: Boolean
    :return: Pandas dataframe with the k-core
    """
    if not directed:
        kcore = nx.core_number(networkGraphs.Graph)
    else:
        kcore = nx.core_number(networkGraphs.DiGraph)

    df = pd.DataFrame(kcore.items(), columns=['Node', 'K-Core'])
    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_triangles(networkGraphs, directed=True):
    """
    :Function: Compute the triangle
    :param networkGraphs: NetworkGraphs
    :param directed: Boolean
    :return: Pandas dataframe with the triangle
    """
    if not directed:
        triangle = nx.triangles(networkGraphs.Graph)
    else:
        triangle = nx.triangles(networkGraphs.DiGraph)

    df = pd.DataFrame(triangle.items(), columns=['Node', 'Triangle'])
    return df


# ----------------------------------------------------------------------------------------
# --------------------------- CONVERT TO HISTOGRAM ---------------------------------------
# ----------------------------------------------------------------------------------------
@memoize
def compute_CDF(df, column):
    """
    :Function: Compute the Cumulative Distribution Function for a given column
    :param df: Pandas dataframe
    :param column: Column name
    :return: Pandas dataframe with the CDF
    """
    df = df.sort_values(by=column, ascending=True)
    df['CDF'] = np.cumsum(df[column]) / np.sum(df[column])
    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_CCDF(df, column):
    """
    :Function: Compute the Complementary Cumulative Distribution Function for a given column
    :param df: Pandas dataframe
    :param column: Column name
    :return: Pandas dataframe with the CCDF
    """
    df = compute_CDF(df, column)
    df['CCDF'] = 1 - df['CDF']
    return df


# ----------------------------------------------------------------------------------------
# ----------------------------------- OTHERS ---------------------------------------------
# ----------------------------------------------------------------------------------------

@memoize
def get_shortest_path(networkGraphs, source, target, weight=None, directed=False):
    if not directed:
        return nx.shortest_path(networkGraphs.Graph, source, target, weight=weight)
    else:
        return nx.shortest_path(networkGraphs.DiGraph, source, target, weight=weight)


# ----------------------------------------------------------------------------------------

def export_to_csv(df, filename):
    """
    :Function: Export the dataframe to a csv file
    :param df: Pandas dataframe
    :param filename: Filename
    :return: 1 if the file is exported
    """
    df.to_csv(filename, index=False)
    return 1


# ----------------------------------------------------------------------------------------

# TEST FUNCTIONS VISUALIZATION SHOULD BE IN ANOTHER FILE
def histogram(df, column, bins=100, log=False, title=None):
    """
    :Function: Plot the histogram for a given column
    :param df: Pandas dataframe
    :param column: Column name
    :param bins: Number of bins
    :param log: Boolean
    :return: Histogram
    """
    if log:
        plt.hist(df[column], bins=bins, log=True)
    else:
        plt.hist(df[column], bins=bins)

    if title:
        plt.title(title)
    plt.show()
