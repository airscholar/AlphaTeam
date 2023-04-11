"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Compute the metrics for the NetworkX graphs
"""

# -------------------------------------- IMPORTS -------------------------------------------

# Internal imports
from src.utils import *

# External imports
import networkx as nx
import pandas as pd


# ----------------------------------------------------------------------------------------
# --------------------------------------- GETTER -----------------------------------------
# ----------------------------------------------------------------------------------------

def get_metrics(networkGraphs, method, directed=False, multi=False):
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
        return compute_kcore(networkGraphs, directed=directed, multi=multi)
    elif method == 'degree':
        return compute_nodes_degree(networkGraphs, directed=directed, multi=multi)
    elif method == 'triangles':
        return compute_triangles(networkGraphs, directed=directed, multi=multi)
    elif method == 'pagerank':
        return compute_page_rank(networkGraphs, directed=directed, multi=multi)
    elif method == 'betweenness_centrality':
        return compute_betweeness_centrality(networkGraphs, directed=directed, multi=multi)
    elif method == 'closeness_centrality':
        return compute_closeness_centrality(networkGraphs, directed=directed, multi=multi)
    elif method == 'eigenvector_centrality':
        return compute_eigen_centrality(networkGraphs, directed=directed, multi=multi)
    elif method == 'load_centrality':
        return compute_load_centrality(networkGraphs, directed=directed, multi=multi)
    elif method == 'degree_centrality':
        return compute_degree_centrality(networkGraphs, directed=directed, multi=multi)
    else:
        raise ValueError("Method not supported")


# ----------------------------------------------------------------------------------------
# ------------------------------------ GLOBAL METRICS ------------------------------------
# ----------------------------------------------------------------------------------------
@memoize
def compute_global_metrics(networkGraphs, directed=False, multi=False):
    """
    :Function: Compute the global metrics for the NetworkGraphs object (all the graphs)
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :return: Pandas dataframe with the metrics and values (for each graph type)
    :rtype: pd.DataFrame
    """
    if multi:
        G = networkGraphs.MultiDiGraph if directed else networkGraphs.MultiGraph
    else:
        G = networkGraphs.DiGraph if directed else networkGraphs.Graph

    return compute_metrics(G)


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

    try:
        efficiency_global = nx.global_efficiency(networkx_)
    except:
        efficiency_global = None

    try:
        efficiency_local = nx.local_efficiency(networkx_)
    except:
        efficiency_local = None

    try:
        nbr_of_isolates = nx.number_of_isolates(networkx_)
    except:
        nbr_of_isolates = None

    records = [
        {"Metrics": "Clustering Coefficient", "Values": clustering_coefficient},
        {"Metrics": "Avg. Shortest Path Length", "Values": avg_shortest_path_length},
        {"Metrics": "Diameter", "Values": diameter},
        {"Metrics": "Radius", "Values": radius},
        {"Metrics": "Number of Nodes", "Values": networkx_.number_of_nodes()},
        {"Metrics": "Number of Edges", "Values": networkx_.number_of_edges()},
        {"Metrics": "Global Efficiency", "Values": efficiency_global},
        {"Metrics": "Local Efficiency", "Values": efficiency_local},
        {"Metrics": "Number of Isolates", "Values": nbr_of_isolates},
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
def compute_node_centralities(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute all the centrality metrics for the NetworkGraphs
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
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

@memoize
def compute_node_metrics(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute all the node metrics for the NetworkGraphs object
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
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
    :Function: Compute the degree centrality for the NetworkGraphs object
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
    """
    metric = 'Degree Centrality'
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
    try:
        degree_centrality = nx.degree_centrality(G)
        df = pd.DataFrame(degree_centrality.items(), columns=['Node', metric])
    except:
        df = return_nan(networkGraphs, metric)

    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_eigen_centrality(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the eigenvector centrality for the NetworkGraphs object
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
    """
    metric = 'Eigenvector Centrality'
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
    try:
        eigen_centrality = nx.eigenvector_centrality(G)
        df = pd.DataFrame(eigen_centrality.items(), columns=['Node', metric])
    except:
        df = return_nan(networkGraphs, metric)

    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_closeness_centrality(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the closeness centrality for the NetworkGraphs object
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
    """
    metric = 'Closeness Centrality'
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
    try:
        closeness_centrality = nx.closeness_centrality(G)
        df = pd.DataFrame(closeness_centrality.items(), columns=['Node', metric])
    except:
        df = return_nan(networkGraphs, metric)

    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_betweeness_centrality(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the betweeness centrality for the NetworkGraphs object
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
    """
    metric = 'Betweeness Centrality'
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
    try:
        betweeness_centrality = nx.betweenness_centrality(G)
        df = pd.DataFrame(betweeness_centrality.items(), columns=['Node', metric])
    except:
        df = return_nan(networkGraphs, metric)

    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_load_centrality(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the load centrality for the NetworkGraphs object
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
    """
    metric = 'Load Centrality'
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
    try:
        load_centrality = nx.load_centrality(G)
        df = pd.DataFrame(load_centrality.items(), columns=['Node', metric])
    except:
        df = return_nan(networkGraphs, metric)

    return df


# ----------------------------------------------------------------------------------------
# ------------------------------ NODES METRICS ------------------------------------------
# ----------------------------------------------------------------------------------------

@memoize
def compute_nodes_degree(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the node degree for the NetworkGraphs object, degree computation allows for Directed and Multi graphs
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
    """
    metric = 'Degree'
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph

    try:
        degree = nx.degree(G)
        df = pd.DataFrame(degree, columns=['Node', metric])
    except:
        df = return_nan(networkGraphs, metric)

    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_kcore(networkGraphs, directed=True, multi=False):
    """
    :Function: Compute the k-core for the NetworkGraphs object, k-core computation allows for Directed but not Multi graphs
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
    :raises: ValueError if the graph is multi
    """
    metric = 'K-Core'
    if multi:
        print(ValueError("K-Core computation is not allowed for Multi graphs"))
        df = return_nan(networkGraphs, metric)
    else:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
        try:
            kcore = nx.core_number(G)
            df = pd.DataFrame(kcore.items(), columns=['Node', metric])
        except:
            df = return_nan(networkGraphs, metric)

    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_triangles(networkGraphs, directed=False, multi=False):
    """
    :Function: Compute the triangle for the NetworkGraphs object not allows for Directed or Multi graphs
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
    :raises: Exception if the graph is directed or multi
    """
    metric = 'Triangle'
    if multi or directed:
        print(ValueError('Triangles computation is not allowed for directed or multi graphs'))
        df = return_nan(networkGraphs, metric)

    else:
        G = networkGraphs.Graph
        try:
            triangle = nx.triangles(G)
            df = pd.DataFrame(triangle.items(), columns=['Node', metric])
        except:
            df = return_nan(networkGraphs, metric)

    return df


# ----------------------------------------------------------------------------------------

@memoize
def compute_page_rank(networkGraphs, directed=True, multi=True):
    """
    :Function: Compute the page rank for the NetworkGraphs object allows for Directed and Multi graphs
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param directed: Compute the metrics for the directed graph
    :type directed: bool
    :param multi: Compute the metrics for the multi graph
    :type multi: bool
    :return: Pandas dataframe with the metrics and values
    :rtype: pd.DataFrame
    """
    metric = 'Page Rank'
    if not multi:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph
    else:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph

    try:
        page_rank = nx.pagerank(G)
        df = pd.DataFrame(page_rank.items(), columns=['Node', metric])
    except:
        df = return_nan(networkGraphs, metric)

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
