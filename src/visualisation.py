"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Visualisation for the NetworkX graphs
"""

# ----------------------------------------------------------------------------------------

from src.visualisation_src.metrics_visualisation import *
from src.visualisation_src.basic_network_visualisation import *
from src.visualisation_src.ML_visualisation import *
from src.visualisation_src.temporal_visualisation import *
import src.machineLearning as ml
import numpy as np
import src.metrics as m
from pandas.api.types import is_numeric_dtype
from src.utils import memoize

# ----------------------------------------------------------------------------------------

@memoize
def plot_cluster(networkGraphs, clusterType, title=None, dynamic=False):
    """
    :Function: Plot the cluster for the given graph
    :param networkGraphs: Network graphs
    :param clusterType: Type of cluster
    :param title: Title of the plot
    :param dynamic: Boolean to indicate if the plot is dynamic or not
    :return:
    """
    cluster = ml.get_communities(networkGraphs, clusterType)

    return generate_static_cluster(networkGraphs, cluster, title, 'map', directed=False)


# ----------------------------------------------------------------------------------------

@memoize
def plot_metrics(networkGraphs, metrics, dynamic=False, layout='map'):
    """
    :Function: Plot the metrics for the given graph
    :param networkGraphs: Network graphs
    :param metrics: Metrics to be plotted
    :param dynamic: Boolean to indicate if the plot is dynamic or not
    :return: Pyplot plot
    """
    df = m.get_metrics(networkGraphs, metrics, clean=False)
    print(df)

    if df[df.columns.values[1]].isnull().values.any():
        return ValueError('Metric column is empty. Please select a different metric.')

    if dynamic:
        return generate_dynamic_metrics(networkGraphs, metrics)
    else:
        return generate_static_metric(networkGraphs, df, layout)


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



