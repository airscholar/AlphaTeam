"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Visualisation for the NetworkX graphs
"""

# ----------------------------------------------------------------------------------------

import os

import cv2
# Imports
import geopandas as gpd
import ipywidgets as widgets
from IPython.display import display
import plotly.graph_objs as go

from src.metrics import *


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
def static_visualisation(networkGraphs, title, directed=True, multi=False, background=True, edges=True):
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
    if directed:
        if networkGraphs.is_spatial():
            plot_map(networkGraphs, background=background, edges=edges)

        if multi:
            nx.draw(networkGraphs.MultiDiGraph, networkGraphs.pos, with_labels=False, node_size=1,
                    edge_color=networkGraphs.colors['MultiDiGraph'], node_color='red', width=0.5)
        else:
            nx.draw(networkGraphs.DiGraph, networkGraphs.pos, with_labels=False, node_size=1,
                    edge_color=networkGraphs.colors['DiGraph'], node_color='red', width=0.5)
    else:
        if networkGraphs.is_spatial():
            plot_map(networkGraphs, background=background, edges=edges)

        if multi:
            nx.draw(networkGraphs.MultiGraph, networkGraphs.pos, with_labels=False, node_size=1, node_color='red',
                    width=0.5)
        else:
            nx.draw(networkGraphs.Graph, networkGraphs.pos, with_labels=False, node_size=1, node_color='red', width=0.5)

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


def plot_metrics(NetworkX_, dataFrame_, title_):
    # return plotly figure
    return 0


# ----------------------------------------------------------------------------------------


def plot_metrics_on_map(networkGraphs, metrics, title_, directed=False):
    G = networkGraphs.Graph if not directed else networkGraphs.DiGraph

    pos = networkGraphs.pos
    edge_trace = go.Scatter(x=[], y=[], hoverinfo='none', mode='lines', line=dict(width=0.5, color='#888'))

    for idx, edge in enumerate(G.edges()):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text',
                            marker=dict(showscale=True, color=['red'], size=3,
                                        colorbar=dict(thickness=10, title='Node Connections', xanchor='left',
                                                      titleside='right'), line=dict(width=2, color='#FF0000')))
    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_centrality = metrics[metrics['Node'] == node]
        node_info = f"Node: {node}<br>Connections: {str(G.degree[node])}<br>" \
                    f"Degree Centrality: {str(node_centrality['Degree Centrality'].values[0])}<br>" \
                    f"Eigenvector Centrality: {str(node_centrality['Eigenvector Centrality'].values[0])}<br>" \
                    f"Closeness Centrality: {str(node_centrality['Closeness Centrality'].values[0])}<br>" \
                    f"Betweenness Centrality: {str(node_centrality['Betweeness Centrality'].values[0])}"
        node_trace['text'] += tuple([node_info])

    layout = go.Layout(
        title=f'<br>{title_}',
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
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        height=1000
    )
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
