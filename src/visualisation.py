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
from src.visualisation_src.temporal_visualisation import *


# ----------------------------------------------------------------------------------------

@memoize
def plot_cluster(networkGraphs, clusterType, dynamic=False, layout='map', plot=True):
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
    if plot:
        if dynamic:
            filename = filename.replace(f"_{layout}", "")
            generate_dynamic_cluster(networkGraphs, cluster, filename)
        else:
            generate_static_cluster(networkGraphs, cluster, filename, layout_='map')


# ----------------------------------------------------------------------------------------

@memoize
def plot_metric(networkGraphs, metrics, directed=False, dynamic=False, layout='map', plot=True):
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
    :return: Pyplot plot
    """
    df = m.get_metrics(networkGraphs, metrics, clean=False, directed=directed)

    if df[df.columns.values[1]].isnull().values.any():
        return ValueError('Metric column is empty. Please select a different metric.')

    filename = f"{metrics}_{'Directed' if directed else 'Undirected'}_{'Dynamic' if dynamic else 'Static'}_{layout}.html"
    if plot:
        if dynamic:
            filename = filename.replace(f"_{layout}", "")
            generate_dynamic_metric(networkGraphs, df, filename)
        else:
            generate_static_metric(networkGraphs, df, filename, layout_=layout)

    return df, filename


# ----------------------------------------------------------------------------------------

@memoize
def plot_all_metrics(networkGraphs, metrics, dynamic=False, directed=False, layout='map', plot=True):
    """
    :Function: Plot all the metrics for the given graph
    Metrics:
        - 'centralities'
        - 'nodes'
    :param networkGraphs: Network graphs
    :param metrics: Metrics to be plotted
    :param dynamic: Boolean to indicate if the plot is dynamic or not
    :param directed: Boolean to indicate if the graph is directed or not
    :param layout: Layout of the plot
    :param plot: Boolean to indicate if the html file should be generated
    :return: Pyplot plot
    """
    if metrics == 'centralities':
        df = m.compute_node_centralities(networkGraphs, directed=False)
    elif metrics == 'nodes':
        df = m.compute_node_metrics(networkGraphs, directed=False)
    else:
        return ValueError('Please select a valid metric, either "centralities" or "nodes"')

    filename = f"All_{metrics}_{directed}_{dynamic}_{layout}.html"
    if plot:
        if dynamic:
            return None
        else:
            generate_static_all_metrics(networkGraphs, df, filename, layout_=layout)
    return df, filename


# ----------------------------------------------------------------------------------------


def plot_histogram(df, column, log=False, title=None):
    """
    :Function: Plot the histogram for a given column
    :param df: Pandas dataframe
    :param column: Column name
    :param log: Boolean
    :param title: Title of the plot
    :return: Histogram
    """
    bins = np.linspace(-5, 5, 50)

    if log:
        plt.hist(df[column], bins=bins, log=True, color='blue', alpha=0.5, edgecolor='black')
    else:
        plt.hist(df[column], bins=bins, color='blue', alpha=0.5, edgecolor='black')

    if title:
        plt.title(title)

    return plt


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

    fig = generate_hotspot(networkGraphs, hotspot)

    fig.write_html('hotspot_coldspot.html')

    return fig
