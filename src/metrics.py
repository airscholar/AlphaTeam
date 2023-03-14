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
from pandas.api.types import is_numeric_dtype
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

    try:
        transitivity = nx.transitivity(networkx_)
    except:
        transitivity = None

    try :
        avg_degree = np.mean(list(dict(networkx_.degree()).values()))
    except:
        avg_degree = None

    try:
        density = nx.density(networkx_)
    except:
        density = None

    records = [
        {"Metrics": "Clustering Coefficient", "Values": clustering_coefficient},
        {"Metrics": "Avg. Shortest Path Length", "Values": avg_shortest_path_length},
        {"Metrics": "Diameter", "Values": diameter},
        {"Metrics": "Radius", "Values": radius},
        {"Metrics": "Number of Nodes", "Values": networkx_.number_of_nodes()},
        {"Metrics": "Number of Edges", "Values": networkx_.number_of_edges()},
        {"Metrics": "Density", "Values": density},
        {"Metrics": "Transitivity", "Values": transitivity},
        {"Metrics": "Avg. Degree", "Values": avg_degree},
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
# ------------------------------- ALL METRICS FUNCTION -----------------------------------
# ----------------------------------------------------------------------------------------

def compute_node_centralities(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the node metrics for the NetworkX graph
    :param networkGraphs: Network Graphs
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    degree_centrality = compute_degree_centrality(networkGraphs, directed=directed, multi=multi)
    eigen_centrality = compute_eigen_centrality(networkGraphs, directed=directed, multi=multi)
    closeness_centrality = compute_closeness_centrality(networkGraphs, directed=directed, multi=multi)
    betweenness_centrality = compute_betweeness_centrality(networkGraphs, directed=directed, multi=multi)
    load_centrality = compute_load_centrality(networkGraphs, directed=directed, multi=multi)

    df = pd.merge(degree_centrality, eigen_centrality, how='inner', on='Node')
    df = pd.merge(df, closeness_centrality, how='inner', on='Node')
    df = pd.merge(df, betweenness_centrality, how='inner', on='Node')
    df = pd.merge(df, load_centrality, how='inner', on='Node')
    return df

# ----------------------------------------------------------------------------------------


def compute_node_metrics(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the node metrics for the NetworkX graph
    :param networkGraphs: Network Graphs
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    kcore = compute_kcore(networkGraphs, directed=directed, multi=multi)
    triangle = compute_triangles(networkGraphs, directed=directed, multi=multi)
    degree = compute_nodes_degree(networkGraphs, directed=directed, multi=multi)
    pagerank = compute_page_rank(networkGraphs, directed=directed, multi=multi)

    df = pd.merge(kcore, triangle, how='inner', on='Node')
    df = pd.merge(df, degree, how='inner', on='Node')
    df = pd.merge(df, pagerank, how='inner', on='Node')
    return df

# ----------------------------------------------------------------------------------------
# ------------------------------ CENTRALITY METRICS --------------------------------------
# ----------------------------------------------------------------------------------------
@memoize
def compute_degree_centrality(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the degree centrality for the NetworkX graph
    :param networkGraphs: Network Graphs
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
    try:
        degree_centrality = nx.degree_centrality(G)
        df = pd.DataFrame(degree_centrality.items(), columns=['Node', 'Degree Centrality'])
    except:
        df = pd.DataFrame(columns=['Node', 'Degree Centrality'])
        df['Node'] = list(networkGraphs.Graph.nodes())
        df['Degree Centrality'] = np.nan

    df = clean_df(df)
    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_eigen_centrality(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the eigenvector centrality for the NetworkX graph
    :param networkGraphs: Network Graphs
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
    try:
        eigen_centrality = nx.eigenvector_centrality(G)
        df = pd.DataFrame(eigen_centrality.items(), columns=['Node', 'Eigenvector Centrality'])
    except:
        df = pd.DataFrame(columns=['Node', 'Eigenvector Centrality'])
        df['Node'] = list(networkGraphs.Graph.nodes())
        df['Eigenvector Centrality'] = np.nan

    df = clean_df(df)
    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_closeness_centrality(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the closeness centrality for the NetworkX graph
    :param networkGraphs: Network Graphs
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
    try:
        closeness_centrality = nx.closeness_centrality(G)
        df = pd.DataFrame(closeness_centrality.items(), columns=['Node', 'Closeness Centrality'])
    except:
        df = pd.DataFrame(columns=['Node', 'Closeness Centrality'])
        df['Node'] = list(networkGraphs.Graph.nodes())
        df['Closeness Centrality'] = np.nan

    df = clean_df(df)
    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_betweeness_centrality(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the betweeness centrality for the NetworkX graph
    :param networkGraphs: Network Graphs
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
    try:
        betweeness_centrality = nx.betweenness_centrality(G)
        df = pd.DataFrame(betweeness_centrality.items(), columns=['Node', 'Betweeness Centrality'])
    except:
        df = pd.DataFrame(columns=['Node', 'Betweeness Centrality'])
        df['Node'] = list(networkGraphs.Graph.nodes())
        df['Betweeness Centrality'] = np.nan

    df = clean_df(df)
    return df


# ----------------------------------------------------------------------------------------

def compute_load_centrality(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the load centrality for the NetworkX graph
    :param networkGraphs: Network Graphs
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
    try:
        load_centrality = nx.load_centrality(G)
        df = pd.DataFrame(load_centrality.items(), columns=['Node', 'Load Centrality'])
    except:
        df = pd.DataFrame(columns=['Node', 'Load Centrality'])
        df['Node'] = list(networkGraphs.Graph.nodes())
        df['Load Centrality'] = np.nan

    df = clean_df(df)
    return df


# ----------------------------------------------------------------------------------------
# ------------------------------ NODES METRICS ------------------------------------------
# ----------------------------------------------------------------------------------------

@memoize
def compute_nodes_degree(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the node degree for the NetworkX graph
    :param networkGraphs: NetworkGraphs
    :param directed: Boolean
    :return: Pandas dataframe with the metrics and values
    """
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
    try:
        degree = nx.degree(G)
        df = pd.DataFrame(degree, columns=['Node', 'Degree'])
    except:
        df = pd.DataFrame(columns=['Node', 'Degree'])
        df['Node'] = list(networkGraphs.Graph.nodes())
        df['Degree'] = np.nan

    df = clean_df(df)
    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_kcore(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the k-core
    :param networkGraphs: NetworkGraphs
    :param directed: Boolean
    :return: Pandas dataframe with the k-core
    """
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
    try:
        kcore = nx.core_number(G)
        df = pd.DataFrame(kcore.items(), columns=['Node', 'K-Core'])
    except:
        df = pd.DataFrame(columns=['Node', 'K-Core'])
        df['Node'] = list(networkGraphs.Graph.nodes())
        df['K-Core'] = np.nan

    df = clean_df(df)
    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_triangles(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the triangle
    :param networkGraphs: NetworkGraphs
    :param directed: Boolean
    :return: Pandas dataframe with the triangle
    """
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
    try:
        triangle = nx.triangles(G)
        df = pd.DataFrame(triangle.items(), columns=['Node', 'Triangle'])
    except:
        df = pd.DataFrame(columns=['Node', 'Triangle'])
        df['Node'] = list(networkGraphs.Graph.nodes())
        df['Triangle'] = np.nan

    df = clean_df(df)
    return df

# ----------------------------------------------------------------------------------------

@memoize
def compute_page_rank(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the page rank
    :param networkGraphs: NetworkGraphs
    :param directed: Boolean
    :return: Pandas dataframe with the page rank
    """
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
    try:
        page_rank = nx.pagerank(G)
        df = pd.DataFrame(page_rank.items(), columns=['Node', 'Page Rank'])
    except:
        df = pd.DataFrame(columns=['Node', 'Page Rank'])
        df['Node'] = list(networkGraphs.Graph.nodes())
        df['Page Rank'] = np.nan

    df = clean_df(df)
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

# ----------------------------------------------------------------------------------------

def clean_df(df):
    """
    :Function: Clean the dataframe
    :param df: Pandas dataframe
    :param column: Column name
    :return: Pandas dataframe
    """

    # if the columns is float round it to 6 decimals
    for column in df.columns:
        # if the columns is a number round it to 6 decimals
        if is_numeric_dtype(df[column]):
            df[column] = df[column].round(6)

        if df[column].dtype == object:
            df[column] = df[column].apply(lambda x: x[:6] + '...' + x[-6:] if len(x) > 15 and x[:2] == '0x' else x[:12])

    return df


