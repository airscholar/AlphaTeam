"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Visualisation for the NetworkX graphs
"""

# ----------------------------------------------------------------------------------------

from visualisation_src.metrics_visualisation import *
from visualisation_src.basic_network_visualisation import *
from visualisation_src.ML_visualisation import *
from visualisation_src.temporal_visualisation import *
import src.machineLearning as ml
import numpy as np

# ----------------------------------------------------------------------------------------


def plot_cluster(networkGraphs, clusterType, title=None, dynamic=False):
    cluster = ml.get_communities(networkGraphs, clusterType)

    color_map = {
        k: (cluster[cluster['node'] == k]['color'].values[0], cluster[cluster['node'] == k]['cluster_id'].values[0]) \
        for k in networkGraphs.Graph.nodes}

    return generate_static_cluster(networkGraphs, color_map, title, 'map', directed=False)


# ----------------------------------------------------------------------------------------


def histogram(df, column, log=False, title=None):
    """
    :Function: Plot the histogram for a given column
    :param df: Pandas dataframe
    :param column: Column name
    :param log: Boolean
    :return: Histogram
    """

    # Define the histogram bins and their edges
    bins = np.linspace(-5, 5, 50)

    if log:
        # y-axis of the histogram will be displayed on a logarithmic scale
        plt.hist(df[column], bins=bins, log=True, color='blue', alpha=0.5, edgecolor='black')
    else:
        plt.hist(df[column], bins=bins, color='blue', alpha=0.5, edgecolor='black')

    if title:
        plt.title(title)

    # return plotly figure
    return plt


# ----------------------------------------------------------------------------------------



