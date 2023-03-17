"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Visualisation for the NetworkX graphs
"""

# ----------------------------------------------------------------------------------------

import numpy as np

import src.machineLearning as ml
import src.metrics as m
from src.utils import memoize
from src.visualisation_src.ML_visualisation import *
from src.visualisation_src.metrics_visualisation import *
from src.visualisation_src.basic_network_visualisation import *
from src.visualisation_src.temporal_visualisation import *
from pandas.api.types import is_numeric_dtype
import os


# ----------------------------------------------------------------------------------------

@memoize
def plot_network(networkGraphs, layout='map', dynamic=False):
    """
    :Function: Plot the NetworkX graph on as map
    :param networkGraphs: Network graphs
    :param directed: Boolean to indicate if the graph is directed or not
    :param multi: for multi graphs
    :return: Matplotlib plot
    """
    if not networkGraphs.is_spatial() and layout == 'map':
        ValueError("Graph is not spatial with coordinates")

    filename = f"{'Dynamic' if dynamic else 'Static'}_{layout}.html"
    filepath = f"../application/{networkGraphs.session_folder}/{filename}"
    if dynamic:
        filepath = filepath.replace(f"_{layout}", "")

    if not os.path.isfile(filepath):
        if dynamic:
            return 0
            # dynamic_visualisation(networkGraphs, filepath)
        else:
            static_visualisation(networkGraphs, filepath, layout_=layout)

    return filename


# ----------------------------------------------------------------------------------------

@memoize
def plot_cluster(networkGraphs, clusterType, dynamic=False, layout='map'):
    """
    :Function: Plot the cluster for the given graph
    Clusters:
        - 'louvain'
        - 'greedy_modularity'
        - 'label_propagation'
        - 'asyn_lpa'
        - 'girvan_newman',
        - 'edge_betweenness'
        - 'k_clique'
    :param networkGraphs: Network graphs
    :param clusterType: Type of cluster
    :param dynamic: Boolean to indicate if the plot is dynamic or not
    :param plot: Boolean to indicate if the html file should be generated
    :param layout: Layout of the plot
    :return:
    """
    cluster = ml.get_communities(networkGraphs, clusterType)

    filename = f"{clusterType}_{'Dynamic' if dynamic else 'Static'}_{layout}.html"
    filepath = f"../application/{networkGraphs.session_folder}/{filename}"
    if dynamic:
        filepath = filepath.replace(f"_{layout}", "")

    if not os.path.isfile(filepath):
        if dynamic:
            generate_dynamic_cluster(networkGraphs, cluster, filepath)
        else:
            generate_static_cluster(networkGraphs, cluster, filepath, layout_=layout)

    return cluster, filename


# ----------------------------------------------------------------------------------------

@memoize
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
    :param networkGraphs: Network graphs
    :param metrics: Metrics to be plotted
    :param dynamic: Boolean to indicate if the plot is dynamic or not
    :param plot: Boolean to indicate if the html file should be generated
    :param layout: Layout of the plot
    :param directed: Boolean to indicate if the graph is directed or not
    :param multi: for multi graphs
    :return: Pyplot plot
    """
    df = m.get_metrics(networkGraphs, metrics, clean=False, directed=directed, multi=multi)

    if df.empty or df.isnull().values.any() or not is_numeric_dtype(df[df.columns.values[1]]):
        return ValueError('Metric column is empty. Please select a different metric.')

    filename = f"{metrics}_{'Directed' if directed else 'Undirected'}_{'Dynamic' if dynamic else 'Static'}_{layout}.html"
    filepath = f"../application/{networkGraphs.session_folder}/{filename}"
    if dynamic:
        filepath = filepath.replace(f"_{layout}", "")

    if not os.path.isfile(filepath):
        if dynamic:
            generate_dynamic_metric(networkGraphs, df, filepath)
        else:
            generate_static_metric(networkGraphs, df, filepath, layout_=layout)

    return df, filename


# ----------------------------------------------------------------------------------------

@memoize
def plot_all_metrics(networkGraphs, metrics, directed=True, multi=True, layout='map'):
    """
    :Function: Plot all the metrics for the given graph
    Metrics:
        - 'centralities'
        - 'nodes'
    :param networkGraphs: Network graphs
    :param metrics: Metrics to be plotted
    :param directed: Boolean to indicate if the graph is directed or not
    :param multi: for multi graphs
    :param layout: Layout of the plot
    :return: Pyplot plot
    """
    if metrics == 'centralities':
        df = m.compute_node_centralities(networkGraphs, directed=False, multi=multi, clean=False)
    elif metrics == 'nodes':
        df = m.compute_node_metrics(networkGraphs, directed=False, multi=multi, clean=False)
    else:
        return ValueError('Please select a valid metric, either "centralities" or "nodes"')

    filename = f"All_{metrics}_{'Directed' if directed else 'Undirected'}_{layout}.html"
    filepath = f"../application/{networkGraphs.session_folder}/{filename}"

    if not os.path.isfile(filepath):
        generate_static_all_metrics(networkGraphs, df, filepath, layout_=layout)

    return df, filename


# ----------------------------------------------------------------------------------------


def plot_histogram(networkGraphs, metrics, directed=True, multi=True):
    """
    :Function: Plot the histogram for a given column
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
        - 'centralities'
        - 'nodes'
    :param networkGraphs: Network graphs
    :param metrics: Metrics to be plotted
    :param directed: Boolean to indicate if the graph is directed or not
    :param multi: for multi graphs
    :return: df and filename
    """
    if metrics == 'centralities':
        df = m.compute_node_centralities(networkGraphs, directed=False, multi=multi, clean=False)
    elif metrics == 'nodes':
        df = m.compute_node_metrics(networkGraphs, directed=False, multi=multi, clean=False)
    else:
        m.get_metrics(networkGraphs, metrics, directed=False, multi=multi, clean=False)

    filename = f"{metrics}_{'Directed' if directed else 'Undirected'}_Histogram.html"





# ----------------------------------------------------------------------------------------


def plot_hotspot(networkGraphs):
    """
    :Function: Plot the hotspot and coldspot for the given graph
    :param networkGraphs:
    :return:
    """
    if not networkGraphs.is_spatial():
        return ValueError('Graph is not spatial. Please select a spatial graph.')

    hotspot = ml.get_hotspot(networkGraphs)

    filename = f"Density_hotspot.html"
    filepath = f"../application/{networkGraphs.session_folder}/{filename}"
    print(filepath)

    if not os.path.isfile(filepath):
        generate_hotspot(networkGraphs, hotspot, filepath)

    return hotspot, filename
