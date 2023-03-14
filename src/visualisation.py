"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Visualisation for the NetworkX graphs
"""

# ----------------------------------------------------------------------------------------

# Imports
import os
from itertools import zip_longest

import cv2
import geopandas as gpd
import ipywidgets as widgets
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.graph_objs as go
from IPython.display import display

import src.machineLearning as ml
from src.utils import *


# ----------------------------------------------------------------------------------------


def dyn_visualisation(networkX_):
    # return html file
    return 0


# ----------------------------------------------------------------------------------------

def plot_map(networkGraphs, background=True, edges=True):
    """
    :Function: Plot the map of the location of the graphs
    :param networkGraphs: Network graphs
    :param background: Boolean to indicate if the background is to be plotted or not
    :param edges: Boolean to indicate if the edges are to be plotted or not
    :return: Matplotlib plot
    """
    if not networkGraphs.is_spatial():
        return 0

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world[(world.pop_est > 0) & (world.name != "Antarctica")]
    ax = world.plot(figsize=(10, 10), edgecolor='black' if edges else 'white',
                    color='white' if background else None)
    ax.set_xlim(networkGraphs.get_min_long(), networkGraphs.get_max_long())
    ax.set_ylim(networkGraphs.get_min_lat(), networkGraphs.get_max_lat())

    return plt


# ----------------------------------------------------------------------------------------


@memoize
def static_visualisation(networkGraphs, title, directed=True, multi=False, background=True, edges=True, layout='map'):
    """
    :Function: Plot the NetworkX graph on a map
    :param networkGraphs: Network graphs
    :param title: Title of the plot
    :param directed: Boolean to indicate if the graph is directed or not
    :param multi: for multi graphs
    :param background: Boolean to indicate if the background is to be plotted or not
    :param edges: Boolean to indicate if the edges are to be plotted or not
    :return: Matplotlib plot
    """
    if not networkGraphs.is_spatial() and layout == 'map':
        ValueError("Graph is not spatial with coordinates")

    if layout == 'map':
        plot_map(networkGraphs, background=background, edges=edges)

    pos = networkGraphs.pos[layout]

    if directed:
        if multi:
            nx.draw(networkGraphs.MultiDiGraph, pos, with_labels=False, node_size=1,
                    edge_color=networkGraphs.colors['MultiDiGraph'], node_color='red', width=0.5)
        else:
            nx.draw(networkGraphs.DiGraph, pos, with_labels=False, node_size=1,
                    edge_color=networkGraphs.colors['DiGraph'], node_color='red', width=0.5)
    else:
        if multi:
            nx.draw(networkGraphs.MultiGraph, pos, with_labels=False, node_size=1,
                    width=0.5)
        else:
            nx.draw(networkGraphs.Graph, pos, with_labels=False, node_size=1, node_color='red',
                    width=0.5)

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
    china.plot(ax=ax, color='white', edgecolor='black')
    colors = nx.get_edge_attributes(temporal_graphs[0], 'color').values()
    nx.draw(temporal_graphs[0], pos=nx.get_node_attributes(temporal_graphs[0], 'pos'), edge_color=colors,
            with_labels=False, node_size=1,
            node_color='red', width=0.5, ax=ax)
    ax.set_title(f"Temporal Graph at {0 // 1440}:{(0 // 60) % 24:02d}:{0 % 60:02d}")

    # Create a slider widget
    slider = widgets.IntSlider(min=0, max=len(temporal_graphs) - 1, value=0, description='Timeframe')

    # Define a function to update the plot when the slider is changed
    def update_plot(val):
        val = val['new']
        ax.clear()
        china.plot(ax=ax, color='white', edgecolor='black')
        colors = nx.get_edge_attributes(temporal_graphs[val], 'color').values()
        nx.draw(temporal_graphs[val], pos=nx.get_node_attributes(temporal_graphs[0], 'pos'), with_labels=False,
                node_size=1, node_color='red', edge_color=colors, width=0.5, ax=ax)
        ax.set_title(f"Temporal Graph at {val // 1440}:{(val // 60) % 24:02d}:{val % 60:02d}")
        plt.show()

    # Attach the update function to the slider
    slider.observe(update_plot, names='value')
    display(slider)
    plt.show()
    return [slider, plt]
    # # Display the slider widget and plot
    # display(slider)
    # plt.show()


# ----------------------------------------------------------------------------------------


def plot_shortest_distance(NetworkX_, path_):
    # return plotly figure
    return 0


# ----------------------------------------------------------------------------------------


def plot_metrics(networkGraphs, df_, layout='map'):
    """
    :Function: Plot the metrics on the graph
    :param networkGraphs: Network graphs
    :param df_: Dataframe with the metrics (first column is the node id) (second column is the metric)
    :param layout: Layout to be used
    :return: Matplotlib plot
    """
    if not networkGraphs.is_spatial() and layout == 'map':
        ValueError("Graph is not spatial with coordinates")
        plt.title("Graph is not spatial with coordinates")
        return plt

    if layout == 'map':
        plot_map(networkGraphs)
    pos = networkGraphs.pos[layout]

    # get the metrics and standardise them
    metrics_names = df_.columns[1]
    metric_ = df_[metrics_names]
    metric_ = (metric_ - metric_.min()) / (metric_.max() - metric_.min())

    fig, ax = plt.subplots(figsize=(10, 6))
    cmap = plt.cm.plasma
    nx.draw(networkGraphs.Graph, pos, node_color=metric_, cmap=cmap, node_size=metric_ * 30, with_labels=False,
            width=0.5)
    plt.title(f"{metrics_names} visualisation using {layout} layout")

    # Add colobar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=metric_.min(), vmax=metric_.max()))
    sm.set_array([])
    cbar = plt.colorbar(sm)
    cbar.set_label(f"{metrics_names} values", rotation=270, labelpad=15)

    return plt


# ----------------------------------------------------------------------------------------


def plot_metrics_on_map(networkGraphs, metrics, title, directed=False):
    G = networkGraphs.Graph if not directed else networkGraphs.DiGraph

    pos = networkGraphs.pos['map']
    edge_trace = go.Scattergeo(lon=[], lat=[], hoverinfo='none', mode='lines', line=dict(width=0.5, color='#888'))

    for idx, edge in enumerate(G.edges()):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['lon'] += tuple([x0, x1, None])
        edge_trace['lat'] += tuple([y0, y1, None])

    node_trace = go.Scattergeo(lon=[], lat=[], text=[], mode='markers', hoverinfo='text',
                               marker=dict(showscale=True, color=['red'], size=3,
                                           colorbar=dict(thickness=10, title='Node Connections', xanchor='left',
                                                         titleside='right'), line=dict(width=2, color='#FF0000')))
    for node in G.nodes():
        x, y = pos[node]
        node_trace['lon'] += tuple([x])
        node_trace['lat'] += tuple([y])
        node_centrality = metrics[metrics['Node'] == node]
        node_info = f"Node: {node}<br>Connections: {str(G.degree[node])}<br>" \
                    f"Degree Centrality: {str(node_centrality['Degree Centrality'].values[0])}<br>" \
                    f"Eigenvector Centrality: {str(node_centrality['Eigenvector Centrality'].values[0])}<br>" \
                    f"Closeness Centrality: {str(node_centrality['Closeness Centrality'].values[0])}<br>" \
                    f"Betweenness Centrality: {str(node_centrality['Betweeness Centrality'].values[0])}"
        node_trace['text'] += tuple([node_info])

    layout = get_map_layout(networkGraphs, title)
    # plot the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=layout)
    # export to html
    filename = f'metrics_map_directed.html' if directed else f'metrics_map_undirected.html'
    fig.write_html(filename)

    return fig


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

def create_frames(temporal_graphs):
    """
    :Function: Create a list of frames for the dynamic temporal graphs
    :param temporal_graphs: List of NetworkX Digraphs
    :return: List of frames
    """
    path = "frames/"
    for i in range(len(temporal_graphs)):
        fig, ax = plt.subplots()
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        china = world[world['name'] == 'China']
        china.plot(ax=ax, color='white', edgecolor='black')
        colors = nx.get_edge_attributes(temporal_graphs[i], 'color').values()
        nx.draw(temporal_graphs[i], pos=nx.get_node_attributes(temporal_graphs[i], 'pos'), edge_color=colors,
                with_labels=False, node_size=0.5,
                node_color='red', width=1.5, ax=ax)
        ax.set_title(f"Temporal Graph")
        plt.savefig(path + f"{i}.png")
        plt.close()
        # free memory
        del fig
        del ax
        print(f"\rCreating frames: {i + 1}/{len(temporal_graphs)}", end="")

    return 1


def plot_cluster(networkGraphs, clusterType, title=None, dynamic=False):
    cluster = ml.get_communities(networkGraphs, clusterType)

    color_map = {
        k: (cluster[cluster['node'] == k]['color'].values[0], cluster[cluster['node'] == k]['cluster_id'].values[0])
        for k in networkGraphs.Graph.nodes}

    plot_clustering_on_map(networkGraphs, cluster, color_map, title, 'map', directed=False)


def get_map_layout(networkGraphs, title=None):
    return go.Layout(
        title=f'<br>{title}',
        titlefont=dict(size=16, color='White'),
        showlegend=False,
        hovermode='closest',
        annotations=[
            dict(
                text="Alpha Team - 2023",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002,
                font=dict(color='black')
            )
        ],
        geo=dict(
            scope='world',
            lataxis_range=[networkGraphs.min_lat, networkGraphs.max_lat],
            lonaxis_range=[networkGraphs.min_long, networkGraphs.max_long],
            center=dict(lat=networkGraphs.mid_lat, lon=networkGraphs.mid_long),
            showland=True,
        ),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        height=1000
    )


def plot_clustering_on_map(networkGraphs, cluster_df, color_map, title, layout='map', directed=False):
    G = networkGraphs.Graph if not directed else networkGraphs.DiGraph

    pos = networkGraphs.pos[layout]

    edge_trace = go.Scattergeo(lon=[], lat=[], hoverinfo='none', mode='lines', line=dict(width=0.5, color='#888'))
    node_trace = go.Scattergeo(lon=[], lat=[], text=[], mode='markers', hoverinfo='text',
                               marker=dict(showscale=True, color=['red'], size=5,
                                           colorbar=dict(thickness=10, title='Node Connections', xanchor='left',
                                                         titleside='right')))

    for idx, vals in enumerate(zip_longest(G.edges(), G.nodes())):
        edge, node = vals
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['lon'] += tuple([x0, x1, None])
        edge_trace['lat'] += tuple([y0, y1, None])

        if idx < len(G.nodes()):
            x, y = pos[node]
            node_trace['lon'] += tuple([x])
            node_trace['lat'] += tuple([y])
            cluster = color_map[node]
            node_info = f"Node: {node}<br>Cluster Id: {str(cluster[1])}<br>"
            node_trace['text'] += tuple([node_info])
            node_trace['marker']['color'] += tuple([cluster[0]])

    layout = get_map_layout(networkGraphs, title)

    # plot the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=layout)
    # export to html
    filename = f'{title}_map_directed.html' if directed else f'{title}_map_undirected.html'
    fig.write_html(filename)

    return fig


# ----------------------------------------------------------------------------------------

def create_mp4():
    """
    :Function: Create a video from the frames
    :return: 1 if successful
    """
    frames_folder = 'frames/'
    frame_filenames = os.listdir(frames_folder)
    frame_filenames.sort(key=lambda x: int(x[:-4]))

    # Read the first frame to get its dimensions
    frame = cv2.imread(frames_folder + frame_filenames[0])
    height, width, layers = frame.shape

    # Create a VideoWriter object to write the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter('output.mp4', fourcc, 30, (width, height))

    # Loop through the frames and add them to the video
    i = 0
    for filename in frame_filenames:
        frame = cv2.imread(frames_folder + filename)
        video.write(frame)
        print(f"\r{i / 2764 * 100:.2f}%", end="")
        i += 1

    video.release()
    print('\nVideo saved as output.mp4')

    return 1
