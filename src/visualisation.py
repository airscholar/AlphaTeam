"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Visualisation for the NetworkX graphs
"""

# ----------------------------------------------------------------------------------------

import numpy as np

import src.machineLearning as ml
import src.metrics as m
from src.utils import *
from src.visualisation_src.ML_visualisation import *
from src.visualisation_src.metrics_visualisation import *
from src.visualisation_src.utils_visualisation import *


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
    :param layout: Layout of the plot
    :return: Pyplot plot
    """
    df = m.get_metrics(networkGraphs, metrics, clean=False)
    print(df)

    if df[df.columns.values[1]].isnull().values.any():
        return ValueError('Metric column is empty. Please select a different metric.')

    if dynamic:
        return None
        # return generate_dynamic_metrics(networkGraphs, metrics)
    else:
        return generate_static_metric(networkGraphs, df, layout)


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


def plot_hotspot(networkGraphs, title=None):
    """
    :Function: Plot the hotspot for the given graph
    :param networkGraphs: Network graphs
    :param title: Title of the plot
    :return:
    """
    if not networkGraphs.is_spatial():
        return ValueError('Graph is not spatial. Please select a spatial graph.')

    hotspot = ml.get_hotspot(networkGraphs)
    latitude = hotspot['Latitude']
    longitude = hotspot['Longitude']
    degree = hotspot['Degree']
    pos = networkGraphs.pos['map']
    G = networkGraphs.Graph

    fig = go.Figure(go.Densitymapbox(lat=latitude, lon=longitude, z=degree, radius=20, hoverinfo='none'))
    fig.add_scattermapbox(lat=latitude, lon=longitude, mode="markers", text=[], name='Nodes', hoverinfo='none',
                          marker=go.scattermapbox.Marker(size=3, color="white"))
    fig.add_scattermapbox(lat=[], lon=[], text=[], mode="lines", name='Edges', hoverinfo='none',
                          line=dict(width=0.5, color="darkgrey"))

    for idx, vals in tqdm(enumerate(zip_longest(G.edges(), G.nodes())), total=G.number_of_edges()):
        edge, node = vals
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        fig.data[2]['lon'] += (x0, x1, None)
        fig.data[2]['lat'] += (y0, y1, None)

    fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=networkGraphs.mid_long,
                      mapbox_center_lat=networkGraphs.mid_lat, mapbox_zoom=3.5, margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      title=title,
                      legend=dict(orientation="h", yanchor="bottom", y=0.1, xanchor="right", x=1, title="Show/Hide"))

    fig.write_html('hotspot_coldspot.html')

    return fig
