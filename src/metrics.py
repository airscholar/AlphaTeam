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
# --------------------------------------- GETTER -----------------------------------------
# ----------------------------------------------------------------------------------------

def get_metrics(networkGraphs, method, clean=True, directed=False, multi=False):
    """
    :Function: Get the metrics for the given graph
    Method:
        - 'kcore'
        - 'degree'
        - 'triangles'
        - 'pagerank'
        - 'betweenness_centrality'
        - 'closeness_centrality'
        - 'eigenvector_centrality'
        - 'load_centrality'
        - 'degree_centrality'
    :param networkGraphs: Network graphs
    :type networkGraphs: NetworkGraphs
    :param method: Method to compute the metrics
    :type method: str
    :param clean: Clean result DataFrame after computing the metrics
    :type clean: bool
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
    """
    if method not in ['kcore', 'degree', 'triangles', 'pagerank', 'betweenness_centrality', 'closeness_centrality',
                      'eigenvector_centrality', 'load_centrality', 'degree_centrality']:
        raise ValueError("Method not supported, please select one of the following: kcore, degree, triangles, "
                         "pagerank, betweenness_centrality, closeness_centrality, eigenvector_centrality, "
                         "load_centrality, degree_centrality ")

    if method == 'kcore':
        return compute_kcore(networkGraphs, clean=clean, directed=directed, multi=multi)
    elif method == 'degree':
        return compute_nodes_degree(networkGraphs, clean=clean, directed=directed, multi=multi)
    elif method == 'triangles':
        return compute_triangles(networkGraphs, clean=clean, directed=directed, multi=multi)
    elif method == 'pagerank':
        return compute_page_rank(networkGraphs, clean=clean, directed=directed, multi=multi)
    elif method == 'betweenness_centrality':
        return compute_betweeness_centrality(networkGraphs, clean=clean, directed=directed, multi=multi)
    elif method == 'closeness_centrality':
        return compute_closeness_centrality(networkGraphs, clean=clean, directed=directed, multi=multi)
    elif method == 'eigenvector_centrality':
        return compute_eigen_centrality(networkGraphs, clean=clean, directed=directed, multi=multi)
    elif method == 'load_centrality':
        return compute_load_centrality(networkGraphs, clean=clean, directed=directed, multi=multi)
    elif method == 'degree_centrality':
        return compute_degree_centrality(networkGraphs, clean=clean, directed=directed, multi=multi)
    else:
        raise ValueError("Method not supported")


# ----------------------------------------------------------------------------------------
# ------------------------------------ GLOBAL METRICS ------------------------------------
# ----------------------------------------------------------------------------------------
@memoize
def compute_global_metrics(networkGraphs):
    """
    :Function: Compute the global metrics for the NetworkGraphs object (all the graphs)
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :return: Pandas dataframe with the metrics and values (for each graph type)
    :rtype: pd.DataFrame
    """
    directed = compute_metrics(networkGraphs.DiGraph)  # compute for directed
    undirected = compute_metrics(networkGraphs.Graph)  # compute for undirected
    multidi = compute_metrics(networkGraphs.MultiDiGraph)  # compute for multidi
    multi = compute_metrics(networkGraphs.MultiGraph)  # compute for multi

    df = pd.merge(directed, undirected, how='inner', on='Metrics'). \
        merge(multidi, how='inner', on='Metrics'). \
        merge(multi, how='inner', on='Metrics')
    df.columns = ['Metrics', 'Directed', 'Undirected', 'MultiDi', 'Multi']
    return df


# ----------------------------------------------------------------------------------------


@memoize
def compute_metrics(networkx_):
    """
    :Function: Compute the generals metrics for the NetworkX graph
    :param networkx_: NetworkX graph
    :type networkx_: nx.Graph or nx.DiGraph or nx.MultiGraph or nx.MultiDiGraph
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
    """

    df = pd.DataFrame()

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

    try:
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

@memoize
def compute_node_centralities(networkGraphs, directed=True, multi=True, clean=True):
    """
    :Function: Compute all the centrality metrics for the NetworkGraphs
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :param clean: Clean the DataFrame after computing the metrics
    :type clean: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
    """
    degree_centrality = compute_degree_centrality(networkGraphs, directed=directed, multi=multi, clean=clean)
    eigen_centrality = compute_eigen_centrality(networkGraphs, directed=directed, multi=multi, clean=clean)
    closeness_centrality = compute_closeness_centrality(networkGraphs, directed=directed, multi=multi, clean=clean)
    betweenness_centrality = compute_betweeness_centrality(networkGraphs, directed=directed, multi=multi, clean=clean)
    load_centrality = compute_load_centrality(networkGraphs, directed=directed, multi=multi, clean=clean)

    df = pd.merge(degree_centrality, eigen_centrality, how='inner', on='Node')
    df = pd.merge(df, closeness_centrality, how='inner', on='Node')
    df = pd.merge(df, betweenness_centrality, how='inner', on='Node')
    df = pd.merge(df, load_centrality, how='inner', on='Node')

    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_node_metrics(networkGraphs, directed=True, multi=True, clean=True):
    """
    :Function: Compute all the node metrics for the NetworkGraphs object
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :param clean: Clean the DataFrame after computing the metrics
    :type clean: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
    """
    kcore = compute_kcore(networkGraphs, directed=directed, multi=multi, clean=clean)
    triangle = compute_triangles(networkGraphs, directed=directed, multi=multi, clean=clean)
    degree = compute_nodes_degree(networkGraphs, directed=directed, multi=multi, clean=clean)
    pagerank = compute_page_rank(networkGraphs, directed=directed, multi=multi, clean=clean)

    df = pd.merge(kcore, triangle, how='inner', on='Node')
    df = pd.merge(df, degree, how='inner', on='Node')
    df = pd.merge(df, pagerank, how='inner', on='Node')
    return df


# ----------------------------------------------------------------------------------------
# ------------------------------ CENTRALITY METRICS --------------------------------------
# ----------------------------------------------------------------------------------------
@memoize
def compute_degree_centrality(networkGraphs, directed=True, multi=True, clean=True):
    """
    :Function: Compute the degree centrality for the NetworkGraphs object
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :param clean: Clean the DataFrame after computing the metrics
    :type clean: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
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

    if clean:
        df = clean_df(df)
    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_eigen_centrality(networkGraphs, directed=True, multi=True, clean=True):
    """
    :Function: Compute the eigenvector centrality for the NetworkGraphs object
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :param clean: Clean the DataFrame after computing the metrics
    :type clean: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
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

    if clean:
        df = clean_df(df)
    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_closeness_centrality(networkGraphs, directed=True, multi=True, clean=True):
    """
    :Function: Compute the closeness centrality for the NetworkGraphs object
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :param clean: Clean the DataFrame after computing the metrics
    :type clean: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
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

    if clean:
        df = clean_df(df)
    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_betweeness_centrality(networkGraphs, directed=True, multi=True, clean=True):
    """
    :Function: Compute the betweeness centrality for the NetworkGraphs object
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :param clean: Clean the DataFrame after computing the metrics
    :type clean: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
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

    if clean:
        df = clean_df(df)
    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_load_centrality(networkGraphs, directed=True, multi=True, clean=True):
    """
    :Function: Compute the load centrality for the NetworkGraphs object
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :param clean: Clean the DataFrame after computing the metrics
    :type clean: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
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

    if clean:
        df = clean_df(df)
    return df


# ----------------------------------------------------------------------------------------
# ------------------------------ NODES METRICS ------------------------------------------
# ----------------------------------------------------------------------------------------

@memoize
def compute_nodes_degree(networkGraphs, directed=True, multi=True, clean=True):
    """
    :Function: Compute the node degree for the NetworkGraphs object, degree computation allows for Directed and Multi graphs
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :param clean: Clean the DataFrame after computing the metrics
    :type clean: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
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

    if clean:
        df = clean_df(df)
    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_kcore(networkGraphs, directed=True, multi=False, clean=True):
    """
    :Function: Compute the k-core for the NetworkGraphs object, k-core computation allows for Directed but not Multi graphs
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :param clean: Clean the DataFrame after computing the metrics
    :type clean: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
    :raises: ValueError if the graph is multi
    """
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
        print(ValueError("K-Core computation is not allowed for Multi graphs"))

    try:
        kcore = nx.core_number(G)
        df = pd.DataFrame(kcore.items(), columns=['Node', 'K-Core'])
    except:
        df = pd.DataFrame(columns=['Node', 'K-Core'])
        df['Node'] = list(networkGraphs.Graph.nodes())
        df['K-Core'] = np.nan

    if clean:
        df = clean_df(df)
    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_triangles(networkGraphs, clean=True, directed=False, multi=False):
    """
    :Function: Compute the triangle for the NetworkGraphs object not allows for Directed and Multi graphs
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param clean: Clean the DataFrame after computing the metrics
    :type clean: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
    :raises: Exception if the graph is directed or multi
    """
    if multi or directed:
        print(ValueError('Triangles computation is not allowed for directed and multi graphs'))

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

    if clean:
        df = clean_df(df)
    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_page_rank(networkGraphs, directed=True, multi=True, clean=True):
    """
    :Function: Compute the page rank for the NetworkGraphs object allows for Directed and Multi graphs
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :param clean: Clean the DataFrame after computing the metrics
    :type clean: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
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

    if clean:
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
    :type df: pd.DataFrame
    :param column: Column name
    :type column: str
    :return: Pandas dataframe with the CDF
    :rtype: pd.DataFrame
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
    :type df: pd.DataFrame
    :param column: Column name
    :type column: str
    :return: Pandas dataframe with the CCDF
    :rtype: pd.DataFrame
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

def clean_df(df):
    """
    :Function: Clean the dataframe by rounding the values to 6 decimals and shortening the strings to 12 characters
    :param df: Pandas dataframe to clean
    :type df: pd.DataFrame
    :return: Pandas dataframe cleaned
    :rtype: pd.DataFrame
    """

    # if the columns is float round it to 6 decimals
    for column in df.columns:
        # if the columns is a number round it to 6 decimals
        if is_numeric_dtype(df[column]):
            df[column] = df[column].round(6)

        if df[column].dtype == object:
            df[column] = df[column].apply(lambda x: x[:6] + '...' + x[-6:] if len(x) > 15 and x[:2] == '0x' else x[:12])

    return df
