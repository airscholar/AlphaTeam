"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Visualisation for the NetworkX graphs
"""

# ----------------------------------------------------------------------------------------

# Imports
import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display

# ----------------------------------------------------------------------------------------


def static_visualisation(networkX_):
    # return plotly figure
    return 0

# ----------------------------------------------------------------------------------------


def dyn_visualisation(networkX_):
    # return html file
    return 0

# ----------------------------------------------------------------------------------------


def plot_static_on_map(networkGraphs, title, directed=True):
    """
    :Function: Plot the NetworkX graph on a map
    :param networkGraphs: Network graphs
    :param title: Title of the plot
    :param directed: Boolean to indicate if the graph is directed or not
    :return: Matplotlib plot
    """
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    china = world[world['name'] == 'China']

    if directed:
        china.plot(figsize=(10, 10), color='white', edgecolor='black')
        nx.draw(networkGraphs.DiGraph, networkGraphs.pos, with_labels=False, node_size=1, edge_color=networkGraphs.colors, node_color='red', width=0.5)
    else:
        china.plot(figsize=(10, 10), edgecolor='black')
        nx.draw(networkGraphs.Graph, networkGraphs.pos, with_labels=False, node_size=1, node_color='red')

    # plot axes
    plt.axis('on')
    plt.title(title)

    return plt

# ----------------------------------------------------------------------------------------


def plot_temporal_graphs(temporal_graphs):
    """
    :Function: Plot the dynamic temporal graphs on a map using a slider
    :param temporal_graphs: List of NetworkX Digraphs
    :return: Matplotlib plot with slider
    """
    # Create a figure and subplot
    fig, ax = plt.subplots()

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    china = world[world['name'] == 'China']
    # Draw the first graph
    china.plot(ax=ax)
    colors = nx.get_edge_attributes(temporal_graphs[0], 'color').values()
    nx.draw(temporal_graphs[0], pos=nx.get_node_attributes(temporal_graphs[0], 'pos'), edge_color=colors, with_labels=False, node_size=1,
            node_color='red', width=0.5, ax=ax)
    ax.set_title(f"Temporal Graph at {0 // 1440}:{(0 // 60) % 24:02d}:{0 % 60:02d}")

    # Create a slider widget
    slider = widgets.IntSlider(min=0, max=len(temporal_graphs) - 1, value=0, description='Timeframe')

    # Define a function to update the plot when the slider is changed
    def update_plot(val):
        val = val['new']
        ax.clear()
        china.plot(ax=ax)
        colors = nx.get_edge_attributes(temporal_graphs[0], 'color').values()
        nx.draw(temporal_graphs[val], pos=nx.get_node_attributes(temporal_graphs[0], 'pos'), with_labels=False,
                node_size=1, node_color='red', edge_color=colors, width=0.5, ax=ax)
        ax.set_title(f"Temporal Graph at {val // 1440}:{(val // 60) % 24:02d}:{val % 60:02d}")
        plt.show()

    # Attach the update function to the slider
    slider.observe(update_plot, names='value')

    return [slider, plt]
    # # Display the slider widget and plot
    # display(slider)
    # plt.show()

# ----------------------------------------------------------------------------------------


def plot_shortest_distance(NetworkX_, path_):
    # return plotly figure
    return 0

# ----------------------------------------------------------------------------------------


def plot_metrics(NetworkX_, dataFrame_, title_):
    # return plotly figure
    return 0

# ----------------------------------------------------------------------------------------


def plot_metrics_on_map(NetworkX_, dataFrame_, title_):
    # return plotly figure
    return 0

# ----------------------------------------------------------------------------------------


def plot_histogram(NetworkX_, dataFrame_, title_):
    # return plotly figure
    return 0
