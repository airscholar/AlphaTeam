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
from threading import Thread


# ----------------------------------------------------------------------------------------

@memoize
def plot_cluster(networkGraphs, clusterType, dynamic=False, layout='map', plot=True):
    """
    :Function: Plot the cluster for the given graph
    :param networkGraphs: Network graphs
    :param clusterType: Type of cluster
    :param dynamic: Boolean to indicate if the plot is dynamic or not
    :param plot: Boolean to indicate if the html file should be generated
    :param layout: Layout of the plot
    :return:
    """
    cluster = ml.get_communities(networkGraphs, clusterType)

    filename = f"{clusterType}_{dynamic}_{layout}.html"
    if plot:
        generate_static_cluster(networkGraphs, cluster, filename, layout_='map')


# ----------------------------------------------------------------------------------------

@memoize
def plot_metric(networkGraphs, metrics, directed=False, dynamic=False, layout='map', plot=True):
    """
    :Function: Plot the metric for the given graph
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

    filename = f"{metrics}_{directed}_{dynamic}_{layout}.html"
    if plot:
        if dynamic:
            return None
            # return generate_dynamic_metrics(networkGraphs, metrics)
        else:
            generate_static_metric(networkGraphs, df, filename, layout_=layout)

    return df, filename


# ----------------------------------------------------------------------------------------

@memoize
def plot_all_metrics(networkGraphs, metrics, dynamic=False, directed=False, layout='map', plot=True):
    """
    :Function: Plot all the metrics for the given graph
    :param networkGraphs: Network graphs
    :param dynamic: Boolean to indicate if the plot is dynamic or not
    :param directed: Boolean to indicate if the graph is directed or not
    :param layout: Layout of the plot
    :param metrics: Metrics to be plotted
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
