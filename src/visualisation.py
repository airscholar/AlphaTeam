"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Visualisation for the NetworkX graphs
"""


# ----------------------------------------------------------------------------------------
import src.machineLearning as ml
import src.metrics as m
from src.visualisation_src.ML_visualisation import *
from src.visualisation_src.metrics_visualisation import *
from src.visualisation_src.basic_network_visualisation import *
from src.visualisation_src.temporal_visualisation import *
from pandas.api.types import is_numeric_dtype
from src.visualisation_src.utils_visualisation import *


# ----------------------------------------------------------------------------------------


def plot_network(networkGraphs, layout='map', dynamic=False):
    """
    :Function: Plot the NetworkX graph on as map
    Layouts:
        - 'map'
        - 'twopi'
        - 'sfdp'
    :param networkGraphs: Network graphs
    :type networkGraphs: NetworkGraphs
    :param layout: Layout of the plot
    :type layout: str
    :param dynamic: Boolean to indicate if the plot is dynamic or not
    :type dynamic: bool
    :return: filename
    :rtype: str
    """
    if not networkGraphs.is_spatial() and layout == 'map':
        print(ValueError("Graph is not spatial with coordinates"))
        return 'no_graph.html'

    filename = f"{'Dynamic' if dynamic else 'Static'}_{layout}.html"
    if dynamic:
        filename = filename.replace(f"_{layout}", "")
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        if dynamic:
            dynamic_visualisation(networkGraphs, filepath)
        else:
            static_visualisation(networkGraphs, filepath, layout_=layout)

    return filename


# ----------------------------------------------------------------------------------------

def plot_cluster(networkGraphs, clusterType, noOfClusters=0, dynamic=False, layout='map'):
    """
    :Function: Plot the cluster for the given graph
    Clusters:
        - 'louvain'
        - 'greedy_modularity'
        - 'label_propagation'
        - 'asyn_lpa'
        - 'girvan_newman',
        - 'k_clique'
        - 'spectral'
        - 'kmeans'
        - 'agglomerative'
        - 'dbscan'
        - 'hierarchical'
    Layouts:
        - 'map'
        - 'twopi'
        - 'sfdp'
    :param networkGraphs: Network graphs
    :type networkGraphs: NetworkGraphs
    :param clusterType: Type of cluster
    :type clusterType: str
    :param noOfClusters: Size of the cluster
    :type noOfClusters: int
    :param dynamic: Boolean to indicate if the plot is dynamic or not
    :type dynamic: bool
    :param layout: Layout of the plot
    :type layout: str
    :return: Cluster and filename of the plot
    :rtype: pd.DataFrame, str
    """
    if clusterType not in ['louvain', 'greedy_modularity', 'label_propagation', 'asyn_lpa', 'girvan_newman',
                           'edge_betweenness', 'k_clique', 'spectral', 'kmeans', 'dbscan', 'hierarchical',
                           'agglomerative']:
        print(ValueError("Cluster type is not valid"))
        df = m.return_nan(networkGraphs, 'Cluster')
        return df, 'no_graph.html'
    if not networkGraphs.is_spatial() and layout == 'map':
        print(ValueError("Graph is not spatial with coordinates"))
        df = m.return_nan(networkGraphs, 'Cluster')
        return df, 'no_graph.html'

    cluster = ml.get_communities(networkGraphs, clusterType, noOfClusters=noOfClusters)
    filename = f"{clusterType}_{'Dynamic' if dynamic else 'Static'}_{layout}.html"
    if dynamic:
        filename = filename.replace(f"_{layout}", "")
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        if dynamic:
            generate_dynamic_cluster(networkGraphs, cluster, filepath)
        else:
            generate_static_cluster(networkGraphs, cluster, filepath, layout_=layout)

    return cluster, filename


# ----------------------------------------------------------------------------------------

def plot_metric(networkGraphs, metrics, directed=True, multi=True, dynamic=False, layout='map'):
    """
    :Function: Plot the metric for the given graph
    Metrics:
        - 'kcore'
        - 'degree'
        - 'triangles'
        - 'pagerank'
        - 'betweenness_centrality'
        - 'closeness_centrality'
        - 'eigenvector_centrality'
        - 'load_centrality'
        - 'degree_centrality'
    Layouts:
        - 'map'
        - 'twopi'
        - 'sfdp'
    :param networkGraphs: Network graphs
    :type networkGraphs: NetworkGraphs
    :param metrics: Metrics to be plotted
    :type metrics: str
    :param dynamic: Boolean to indicate if the plot is dynamic or not
    :type dynamic: bool
    :param layout: Layout of the plot
    :type layout: str
    :param directed: Boolean to indicate if the graph is directed or not
    :type directed: bool
    :param multi: for multi graphs
    :type multi: bool
    :return: Dataframe with the metric and the filename of the plot
    :rtype: pd.DataFrame, str
    """
    df = m.get_metrics(networkGraphs, metrics, directed=directed, multi=multi)

    if df.empty or df.isnull().values.any() or not is_numeric_dtype(df[df.columns.values[1]]) or (
            not networkGraphs.is_spatial() and layout == 'map'):
        print(ValueError(
            'Metric column is empty. Please select a different metric or select different layout because graphs is not spatial with coordinates '))
        return df, "no_graph.html"

    filename = f"{metrics}_{'Directed' if directed else 'Undirected'}_{'Mutli' if multi else ''}_{'Dynamic' if dynamic else 'Static'}_{layout}.html"
    if dynamic:
        filename = filename.replace(f"_{layout}", "")
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        if dynamic:
            generate_dynamic_metric(networkGraphs, df, filepath)
        else:
            generate_static_metric(networkGraphs, df, filepath, layout_=layout)

    return df, filename


# ----------------------------------------------------------------------------------------


def plot_all_metrics(networkGraphs, metrics, directed=True, multi=True, layout='map'):
    """
    :Function: Plot all the metrics for the given graph
    Metrics:
        - 'centralities'
        - 'nodes'
    Layouts:
        - 'map'
        - 'twopi'
        - 'sfdp'
    :param networkGraphs: Network graphs
    :type networkGraphs: NetworkGraphs
    :param metrics: Metrics to be plotted
    :type metrics: str
    :param directed: Boolean to indicate if the graph is directed or not
    :type directed: bool
    :param multi: for multi graphs
    :type multi: bool
    :param layout: Layout of the plot
    :type layout: str
    :return: Dataframe with all the metrics and the filename of the plot
    :rtype: pd.DataFrame, str
    """
    if not networkGraphs.is_spatial() and layout == 'map':
        print(ValueError(
            'Metric column is empty. Please select a different metric or select different layout because graphs is '
            'not spatial with coordinates '))
        df = m.return_nan(networkGraphs, 'Metrics')
        return df, "no_graph.html"

    if metrics == 'centralities':
        df = m.compute_node_centralities(networkGraphs, directed=directed, multi=multi)
    elif metrics == 'nodes':
        df = m.compute_node_metrics(networkGraphs, directed=directed, multi=multi)
    else:
        print(ValueError('Please select a valid metric, either "centralities" or "nodes"'))
        df = m.return_nan(networkGraphs, 'Metrics')
        return df, 'no_graph.html'

    filename = f"All_{metrics}_{'Directed' if directed else 'Undirected'}_{'Multi' if multi else ''}_{layout}.html"
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        generate_static_all_metrics(networkGraphs, df, filepath, layout_=layout)

    return df, filename


# ----------------------------------------------------------------------------------------


def plot_histogram(networkGraphs, metrics, directed=True, multi=True):
    """
    :Function: Plot the histogram distribution for a given metric
    Metrics:
        - 'kcore'
        - 'degree'
        - 'triangles'
        - 'pagerank'
        - 'betweenness_centrality'
        - 'closeness_centrality'
        - 'eigenvector_centrality'
        - 'load_centrality'
        - 'degree_centrality'
        - 'centralities' - All centralities
        - 'nodes' - All node metrics
    :param networkGraphs: Network graphs
    :type networkGraphs: NetworkGraphs
    :param metrics: Metrics to be plotted
    :type metrics: str
    :param directed: Boolean to indicate if the graph is directed or not
    :type directed: bool
    :param multi: for multi graphs
    :type multi: bool
    :return: df and filename
    :rtype: pd.DataFrame, str
    """
    if metrics == 'centralities':
        df = m.compute_node_centralities(networkGraphs, directed=False, multi=multi)
    elif metrics == 'nodes':
        df = m.compute_node_metrics(networkGraphs, directed=False, multi=multi)
    else:
        df = m.get_metrics(networkGraphs, metrics, directed=False, multi=multi)

    filename = f"{metrics}_{'Directed' if directed else 'Undirected'}_{'Mutli' if multi else ''}_Histogram.html"
    filepath = get_file_path(networkGraphs, filename)
    if not os.path.isfile(filepath):
        generate_histogram_metric(df, filepath)

    return df, filename


# ----------------------------------------------------------------------------------------


def plot_hotspot(networkGraphs):
    """
    :Function: Plot the hotspot and coldspot for the given graph
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :return: Dataframe with the hotspot and coldspot and filename
    :rtype: pd.DataFrame, str
    """
    if not networkGraphs.is_spatial():
        print(ValueError('Graph is not spatial. Please select a spatial graph.'))
        df = m.return_nan(networkGraphs, 'Cluster')
        return df, 'no_graph.html'

    df = ml.get_hotspot(networkGraphs)

    filename = f"Density_hotspot.html"
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        generate_hotspot(networkGraphs, df, filepath)

    return df, filename


# ----------------------------------------------------------------------------------------


def plot_boxplot(networkGraphs, metrics, directed=True, multi=True):
    """
    :Function: Plot the boxplot for a given metric
    Metrics:
        - 'kcore'
        - 'degree'
        - 'triangles'
        - 'pagerank'
        - 'betweenness_centrality'
        - 'closeness_centrality'
        - 'eigenvector_centrality'
        - 'load_centrality'
        - 'degree_centrality'
        - 'centralities' - All centralities
        - 'nodes' - All node metrics
    :param networkGraphs: Network graphs
    :type networkGraphs: NetworkGraphs
    :param metrics: Metrics to be plotted
    :type metrics: str
    :param directed: Boolean to indicate if the graph is directed or not
    :type directed: bool
    :param multi: for multi graphs
    :type multi: bool
    :return: df and filename
    :rtype: pd.DataFrame, str
    """
    if metrics == 'centralities':
        df = m.compute_node_centralities(networkGraphs, directed=False, multi=multi)
    elif metrics == 'nodes':
        df = m.compute_node_metrics(networkGraphs, directed=False, multi=multi)
    else:
        df = m.get_metrics(networkGraphs, metrics, directed=False, multi=multi)

    filename = f"{metrics}_{'Directed' if directed else 'Undirected'}_{'Mutli' if multi else ''}_Boxplot.html"
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        generate_boxplot_metric(df, filepath)

    return df, filename


# ----------------------------------------------------------------------------------------


def plot_violin(networkGraphs, metrics, directed=True, multi=True):
    """
    :Function: Plot the violin plot for a metric
    Metrics:
        - 'kcore'
        - 'degree'
        - 'triangles'
        - 'pagerank'
        - 'betweenness_centrality'
        - 'closeness_centrality'
        - 'eigenvector_centrality'
        - 'load_centrality'
        - 'degree_centrality'
        - 'centralities' - All centralities
        - 'nodes' - All node metrics
    :param networkGraphs: Network graphs
    :type networkGraphs: NetworkGraphs
    :param metrics: Metrics to be plotted
    :type metrics: str
    :param directed: Boolean to indicate if the graph is directed or not
    :type directed: bool
    :param multi: for multi graphs
    :type multi: bool
    :return: df and filename
    :rtype: pd.DataFrame, str
    """
    if metrics == 'centralities':
        df = m.compute_node_centralities(networkGraphs, directed=False, multi=multi)
    elif metrics == 'nodes':
        df = m.compute_node_metrics(networkGraphs, directed=False, multi=multi)
    else:
        df = m.get_metrics(networkGraphs, metrics, directed=False, multi=multi)

    filename = f"{metrics}_{'Directed' if directed else 'Undirected'}_{'Mutli' if multi else ''}_Violin.html"
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        generate_violin_metric(df, filepath)

    return df, filename


# ----------------------------------------------------------------------------------------


def plot_heatmap(networkGraphs):
    """
    :Function: Plot the heatmap for the given graph
    :param networkGraphs:
    :type networkGraphs: NetworkGraphs
    :return: filename
    :rtype: str
    """
    filename = f"heatmap.html"
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        generate_heatmap(networkGraphs, filepath)

    return filename


# ----------------------------------------------------------------------------------------

def plot_temporal(neworkGraphs, layout='map'):
    """
    :Function: Plot the temporal graph for the given graph
    :param neworkGraphs: NetworkGraphs object
    :type neworkGraphs: NetworkGraphs
    :return: filename
    :rtype: str
    """
    if not neworkGraphs.is_temporal():
        print(ValueError('Graph is not temporal. Please select a temporal graph.'))
        return 'no_graph.html'

    if not neworkGraphs.is_spatial() and layout == 'map':
        print(ValueError('Graph is not spatial. Please select a spatial graph.'))
        return 'no_graph.html'

    filename = f"temporal_{layout}.html"
    filepath = get_file_path(neworkGraphs, filename)

    if not os.path.isfile(filepath):
        generate_temporal(neworkGraphs, filepath, layout_=layout)

    return filename
