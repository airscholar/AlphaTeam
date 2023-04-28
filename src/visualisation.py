"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Visualisation for the NetworkX graphs
"""

# ----------------------------------------------------------------------------------------

import pandas as pd
# External Imports
from pandas.api.types import is_numeric_dtype

import src.deepLearning as dl
# Internal Imports
import src.machineLearning as ml
import src.metrics as m
from src import utils
from src.deepLearning import *
from src.visualisation_src.DL_visualisation import *
from src.visualisation_src.ML_visualisation import *
from src.visualisation_src.basic_network_visualisation import *
from src.visualisation_src.metrics_visualisation import *
from src.visualisation_src.temporal_visualisation import *
from src.visualisation_src.utils_visualisation import *


# ----------------------------------------------------------------------------------------


def plot_network(networkGraphs, layout='map', dynamic=False, fullPath=False):
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
    :param fullPath: Boolean to indicate if the full path is required
    :type fullPath: bool
    :return: filename
    :rtype: str
    """
    if not networkGraphs.is_spatial() and layout == 'map':
        print(ValueError("Graph is not spatial with coordinates"))
        return '../application/static/no_graph.html'

    filename = f"{'Dynamic' if dynamic else 'Static'}_{layout}.html"
    if dynamic:
        filename = filename.replace(f"_{layout}", "")
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        if dynamic:
            dynamic_visualisation(networkGraphs, filepath)
        else:
            static_visualisation(networkGraphs, filepath, layout_=layout)

    return filepath if fullPath else filename


# ----------------------------------------------------------------------------------------

def plot_cluster(networkGraphs, clusterType, noOfClusters=0, dynamic=False, layout='map', fullPath=False):
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
    :param fullPath: Boolean to indicate if the full path is required
    :type fullPath: bool
    :return: Cluster and filename of the plot
    :rtype: pd.DataFrame, str
    """
    if clusterType not in ['louvain', 'greedy_modularity', 'label_propagation', 'asyn_lpa', 'girvan_newman',
                           'edge_betweenness', 'k_clique', 'spectral', 'kmeans', 'dbscan', 'hierarchical',
                           'agglomerative']:
        print(ValueError("Cluster type is not valid"))
        df = utils.return_nan(networkGraphs, 'Cluster')
        return df, 'no_graph.html'
    if not networkGraphs.is_spatial() and layout == 'map' or noOfClusters >= len(networkGraphs.Graph.nodes) // 2:
        print(ValueError("Graph is not spatial with coordinates, or max number of clusters is reached"))
        df = utils.return_nan(networkGraphs, 'Cluster')
        return df, 'no_graph.html'

    cluster = ml.get_communities(networkGraphs, clusterType, noOfClusters=noOfClusters)
    if len(cluster) == 0 or cluster.isnull().values.any() or len(cluster) != len(networkGraphs.Graph.nodes):
        print(ValueError("Issue with cluster or cluster not possible for this method or graph"))
        return utils.return_nan(networkGraphs, 'Cluster'), 'no_graph.html'

    filename = f"{clusterType}_{'Dynamic' if dynamic else 'Static'}_{layout}.html"
    if dynamic:
        filename = filename.replace(f"_{layout}", "")
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath) or noOfClusters > 0:
        if dynamic:
            generate_dynamic_cluster(networkGraphs, cluster, filepath)
        else:
            generate_static_cluster(networkGraphs, cluster, filepath, clusterType, layout_=layout, nbr=noOfClusters)

    return cluster, filename if not fullPath else filepath


# ----------------------------------------------------------------------------------------

def plot_metric(networkGraphs, metrics, directed=True, multi=True, dynamic=False, layout='map', fullPath=False):
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
    :param fullPath: Boolean to indicate if the full path is required
    :type fullPath: bool
    :return: Dataframe with the metric and the filename of the plot
    :rtype: pd.DataFrame, str
    """
    df = m.get_metrics(networkGraphs, metrics, directed=directed, multi=multi)

    if df.empty or df.isnull().values.any() or not is_numeric_dtype(df[df.columns.values[1]]) or (
            not networkGraphs.is_spatial() and layout == 'map'):
        print(ValueError(
            'Metric column is empty. Please select a different metric or select different layout because graphs is not spatial with coordinates '))
        return df, '../application/static/no_graph.html'

    filename = f"{metrics}_{'Directed' if directed else 'Undirected'}_{'Mutli' if multi else ''}_{'Dynamic' if dynamic else 'Static'}_{layout}.html"
    if dynamic:
        filename = filename.replace(f"_{layout}", "")
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        if dynamic:
            generate_dynamic_metric(networkGraphs, df, filepath)
        else:
            generate_static_metric(networkGraphs, df, filepath, layout_=layout)

    return df, filename if not fullPath else filepath


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
        df = utils.return_nan(networkGraphs, 'Metrics')
        return df, '../application/static/no_graph.html'

    if metrics == 'centralities':
        df = m.compute_node_centralities(networkGraphs, directed=directed, multi=multi)
    elif metrics == 'nodes':
        df = m.compute_node_metrics(networkGraphs, directed=directed, multi=multi)
    else:
        print(ValueError('Please select a valid metric, either "centralities" or "nodes"'))
        df = utils.return_nan(networkGraphs, 'Metrics')
        return df, 'no_graph.html'

    filename = f"All_{metrics}_{'Directed' if directed else 'Undirected'}_{'Multi' if multi else ''}_{layout}.html"
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        generate_static_all_metrics(networkGraphs, df, filepath, layout_=layout)

    return df, filename


# ----------------------------------------------------------------------------------------


def plot_histogram(networkGraphs, metrics, directed=True, multi=True, fullPath=False):
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
    :param fullPath: Boolean to indicate if the full path is required
    :type fullPath: bool
    :return: df and filename
    :rtype: pd.DataFrame, str
    """
    if metrics == 'centralities':
        df = m.compute_node_centralities(networkGraphs, directed=directed, multi=multi)
    elif metrics == 'nodes':
        df = m.compute_node_metrics(networkGraphs, directed=directed, multi=multi)
    else:
        df = m.get_metrics(networkGraphs, metrics, directed=directed, multi=multi)

    filename = f"{metrics}_{'Directed' if directed else 'Undirected'}_{'Mutli' if multi else ''}_Histogram.html"
    filepath = get_file_path(networkGraphs, filename)
    if not os.path.isfile(filepath):
        generate_histogram_metric(df, filepath)

    return df, filename if not fullPath else filepath


# ----------------------------------------------------------------------------------------


def plot_hotspot(networkGraphs, fullPath=False):
    """
    :Function: Plot the hotspot and coldspot for the given graph
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param fullPath: Boolean to indicate if the full path is required
    :type fullPath: bool
    :return: Dataframe with the hotspot and coldspot and filename
    :rtype: pd.DataFrame, str
    """
    if not networkGraphs.is_spatial():
        print(ValueError('Graph is not spatial. Please select a spatial graph.'))
        df = utils.return_nan(networkGraphs, 'Cluster')
        return df, 'no_graph.html'

    df = ml.get_hotspot(networkGraphs)

    filename = f"Density_hotspot.html"
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        generate_hotspot(networkGraphs, df, filepath)

    return df.iloc[:, :2], filename if not fullPath else filepath


# ----------------------------------------------------------------------------------------


def plot_boxplot(networkGraphs, metrics, directed=True, multi=True, fullPath=False):
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
    :param fullPath: Boolean to indicate if the full path is required
    :type fullPath: bool
    :return: df and filename
    :rtype: pd.DataFrame, str
    """
    if metrics == 'centralities':
        df = m.compute_node_centralities(networkGraphs, directed=directed, multi=multi)
    elif metrics == 'nodes':
        df = m.compute_node_metrics(networkGraphs, directed=directed, multi=multi)
    else:
        df = m.get_metrics(networkGraphs, metrics, directed=directed, multi=multi)

    filename = f"{metrics}_{'Directed' if directed else 'Undirected'}_{'Mutli' if multi else ''}_Boxplot.html"
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        generate_boxplot_metric(df, filepath)

    return df.iloc[:, :2], filename if not fullPath else filepath


# ----------------------------------------------------------------------------------------


def plot_violin(networkGraphs, metrics, directed=True, multi=True, fullPath=False):
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
    :param fullPath: Boolean to indicate if the full path is required
    :type fullPath: bool
    :return: df and filename
    :rtype: pd.DataFrame, str
    """
    if metrics == 'centralities':
        df = m.compute_node_centralities(networkGraphs, directed=directed, multi=multi)
    elif metrics == 'nodes':
        df = m.compute_node_metrics(networkGraphs, directed=directed, multi=multi)
    else:
        df = m.get_metrics(networkGraphs, metrics, directed=directed, multi=multi)

    filename = f"{metrics}_{'Directed' if directed else 'Undirected'}_{'Mutli' if multi else ''}_Violin.html"
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        generate_violin_metric(df, filepath)

    return df.iloc[:, :2], filename if not fullPath else filepath


# ----------------------------------------------------------------------------------------


def plot_heatmap(networkGraphs, fullPath=False):
    """
    :Function: Plot the heatmap for the given graph
    :param networkGraphs:
    :type networkGraphs: NetworkGraphs
    :param fullPath: Boolean to indicate if the full path is required
    :type fullPath: bool
    :return: filename
    :rtype: str
    """
    filename = f"heatmap.html"
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        generate_heatmap(networkGraphs, filepath)

    return filename if not fullPath else filepath


# ----------------------------------------------------------------------------------------

def plot_temporal(networkGraphs, layout='map'):
    """
    :Function: Plot the temporal graph for the given graph
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param layout: Layout of the graph
    :type layout: str
    :return: filename
    :rtype: str
    """
    if not networkGraphs.is_temporal():
        print(ValueError('Graph is not temporal. Please select a temporal graph.'))
        return '../application/static/no_graph.html'

    if not networkGraphs.is_spatial() and layout == 'map':
        print(ValueError('Graph is not spatial. Please select a spatial graph.'))
        return '../application/static/no_graph.html'

    filename = f"temporal_{layout}.html"
    filepath = get_file_path(networkGraphs, filename)

    if not os.path.isfile(filepath):
        generate_temporal(networkGraphs, filepath, layout_=layout)

    return filename


# ----------------------------------------------------------------------------------------

def plot_node2vec(networkGraphs, p=1, q=1, layout='TSNE', fullPath=False):
    """
    :Function: Plot the node2vec for the given graph
    layout:
        - 'TSNE'
        - 'UMAP'
        - 'PCA'
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param p: p parameter for node2vec
    :type p: float
    :param q: q parameter for node2vec
    :type q: float
    :param layout: Visualisation method
    :type layout: str
    :param fullPath: Boolean to indicate if the full path is required
    :type fullPath: bool
    :return: df and filename
    :rtype: pd.DataFrame, str
    """
    if layout not in ['TSNE', 'UMAP', 'PCA']:
        print(ValueError('Please select a valid visualisation method.'))
        return '../application/static/no_graph.html'

    _, emb = dl.node2vec_embedding(networkGraphs, p=p, q=q)

    filename = f"node2vec_{layout}.html"
    filepath = get_file_path(networkGraphs, filename)

    if layout == 'TSNE':
        TSNE_visualisation(networkGraphs, emb, filepath)
    elif layout == 'UMAP':
        umap_visualisation(networkGraphs, emb, filepath)
    elif layout == 'PCA':
        PCA_visualisation(networkGraphs, emb, filepath)

    df = pd.DataFrame(emb)

    return df, filename if not fullPath else filepath


# ----------------------------------------------------------------------------------------

def plot_node2vec_cluster(networkGraphs, method, noOfCluster=8, p=1, q=1, layout='TSNE', fullPath=False):
    """
    :Function: Plot the embedding cluster for the given graph
    method:
        - 'kmeans'
        - 'spectral'
        - 'agglomerative'
        - 'dbscan'
    layout:
        - 'TSNE'
        - 'UMAP'
        - 'PCA'
        - 'sfdp'
        - 'twopi'
        - 'map'
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param method: Clustering method
    :type method: str
    :param noOfCluster: Number of clusters
    :type noOfCluster: int
    :param p: p parameter for node2vec
    :type p: float
    :param q: q parameter for node2vec
    :type q: float
    :param layout: Visualisation method
    :type layout: str
    :param fullPath: Boolean to indicate if the full path is required
    :type fullPath: bool
    :return: DataFrame, filename
    :rtype: pd.DataFrame, str
    """
    if layout not in ['TSNE', 'UMAP', 'PCA', 'sfdp', 'twopi', 'map']:
        print(ValueError('Please select a valid visualisation method.'))
        return '../application/static/no_graph.html'

    if layout == 'map' and not networkGraphs.is_spatial():
        print(ValueError('Please select a valid visualisation method.'))
        return '../application/static/no_graph.html'

    if method not in ['kmeans', 'spectral', 'agglomerative', 'dbscan']:
        print(ValueError('Please select a valid clustering method.'))
        return '../application/static/no_graph.html'

    _, emb = dl.node2vec_embedding(networkGraphs, p=p, q=q)
    clusters = ml.get_communities(networkGraphs, method=method, noOfClusters=noOfCluster, embedding=emb)

    filename = f"node2vec_{method}_{layout}.html"
    filepath = get_file_path(networkGraphs, filename)

    if layout == 'TSNE':
        TSNE_visualisation(networkGraphs, emb, filepath, clusters=clusters)
    elif layout == 'UMAP':
        umap_visualisation(networkGraphs, emb, filepath, clusters=clusters)
    elif layout == 'PCA':
        PCA_visualisation(networkGraphs, emb, filepath, clusters=clusters)
    elif layout in ['sfdp', 'twopi', 'map']:
        generate_static_cluster(networkGraphs, clusters, filepath, method, layout_=layout, nbr=noOfCluster)

    df = pd.DataFrame(emb)

    return df, filename if not fullPath else filepath


# ----------------------------------------------------------------------------------------


def plot_DL_embedding(networkGraphs, features=['proximity'], dimension=128, model='SAGE', layout='TSNE',
                      fullPath=False):
    """
    :Function: Plot the embedding for the given graph
    features:
        Format: ['feature1', 'feature2', ...]
        If choose proximity just put ['proximity'] without any other features
        - 'proximity'
        - 'kcore'
        - 'triangles'
        - 'degree'
        - 'pagerank'
    layout:
        - 'TSNE'
        - 'UMAP'
        - 'PCA'
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param features: Feature list
    :type features: list
    :param dimension: Dimension of the embedding
    :type dimension: int
    :param model: GNN model
    :type model: str
    :param layout: Visualisation method
    :type layout: str
    :param fullPath: Boolean to indicate if the full path is required
    :type fullPath: bool
    :return: DataFrame, filename
    :rtype: pd.DataFrame, str
    """
    if layout not in ['TSNE', 'UMAP', 'PCA']:
        print(ValueError('Please select a valid visualisation method.'))
        return '../application/static/no_graph.html'

    if model not in ['SAGE', 'GAT', 'GCN']:
        print(ValueError('Please select a valid GNN.'))
        return '../application/static/no_graph.html'

    emb = get_DL_embedding(networkGraphs, model=model, features=features, dimension=dimension)

    filename = f"DLEmbedding_{layout}.html"
    filepath = get_file_path(networkGraphs, filename)

    if layout == 'TSNE':
        TSNE_visualisation(networkGraphs, emb, filepath)
    elif layout == 'UMAP':
        umap_visualisation(networkGraphs, emb, filepath)
    elif layout == 'PCA':
        PCA_visualisation(networkGraphs, emb, filepath)

    df = pd.DataFrame(emb)

    return df, filename if not fullPath else filepath


# ----------------------------------------------------------------------------------------


def plot_DL_embedding_cluster(networkGraphs, method, noOfCluster=8, features=['proximity'], dimension=128, model='SAGE',
                              layout='TSNE', fullPath=False):
    """
    :Function: Plot the embedding cluster
    method:
        - 'kmeans'
        - 'spectral'
        - 'agglomerative'
        - 'dbscan'
    features:
        Format: ['feature1', 'feature2', ...]
        If choose proximity just put ['proximity'] without any other features
        - 'proximity'
        - 'kcore'
        - 'triangles'
        - 'degree'
        - 'pagerank'
    layout:
        - 'TSNE'
        - 'UMAP'
        - 'PCA'
        - 'sfdp'
        - 'twopi'
        - 'map'
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param method: Clustering method
    :type method: str
    :param noOfCluster: Number of clusters
    :type noOfCluster: int
    :param features: Feature list
    :type features: list
    :param dimension: Dimension of the embedding
    :type dimension: int
    :param model: GNN model
    :type model: str
    :param layout: Visualisation method
    :type layout: str
    :param fullPath: Boolean to indicate if the full path is required
    :type fullPath: bool
    :return: DataFrame, filename
    :rtype: pd.DataFrame, str
    """
    if layout not in ['TSNE', 'UMAP', 'PCA', 'sfdp', 'twopi', 'map']:
        print(ValueError('Please select a valid visualisation method.'))
        return '../application/static/no_graph.html'

    if layout == 'map' and not networkGraphs.is_spatial():
        print(ValueError('Please select a valid visualisation method.'))
        return '../application/static/no_graph.html'

    if model not in ['SAGE', 'GAT', 'GCN']:
        print(ValueError('Please select a valid GNN.'))
        return '../application/static/no_graph.html'

    if method not in ['kmeans', 'spectral', 'agglomerative', 'dbscan']:
        print(ValueError('Please select a valid clustering method.'))
        return '../application/static/no_graph.html'

    emb = get_DL_embedding(networkGraphs, model=model, features=features, dimension=dimension)
    clusters = ml.get_communities(networkGraphs, method=method, noOfClusters=noOfCluster, embedding=emb)

    filename = f"DLEmbedding_{method}_{layout}.html"
    filepath = get_file_path(networkGraphs, filename)

    if layout == 'TSNE':
        TSNE_visualisation(networkGraphs, emb, filepath, clusters=clusters)
    elif layout == 'UMAP':
        umap_visualisation(networkGraphs, emb, filepath, clusters=clusters)
    elif layout == 'PCA':
        PCA_visualisation(networkGraphs, emb, filepath, clusters=clusters)
    elif layout in ['sfdp', 'twopi', 'map']:
        generate_static_cluster(networkGraphs, clusters, filepath, method, layout_=layout, nbr=noOfCluster)

    df = pd.DataFrame(emb)

    return df, filename if not fullPath else filepath
