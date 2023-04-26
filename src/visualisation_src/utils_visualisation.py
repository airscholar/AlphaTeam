"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Visualisation utilities module contains functions for visualising the network graphs
"""

# ----------------------------------------- Imports ----------------------------------------- #

# External imports
import os

import geopandas as gpd
import matplotlib.pyplot as plt
from plotly import graph_objects as go

# Internal imports
from src.utils import memoize


# ----------------------------------------------------------------------------------------

@memoize
def plot_map(networkGraphs, background=True, edges=True):  # FOR MATPLOTLIB
    """
    :Function: Plot the map of the location of the graphs
    :param networkGraphs: Network graphs
    :type networkGraphs: NetworkGraphs
    :param background: Boolean to indicate if the background is to be plotted or not
    :type background: bool
    :param edges: Boolean to indicate if the edges are to be plotted or not
    :type edges: bool
    :return: Matplotlib plot
    :rtype: matplotlib.pyplot
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
def get_layout(networkGraphs, title=None, layout_='map'):  # FOR PLOTLY
    """
    :Function: Get the layout of the graph
    :param networkGraphs: Network graphs
    :type networkGraphs: NetworkGraphs
    :param title: Title of the graph
    :type title: str
    :param layout_: layout of the graph
    :type layout_: str
    :return: Plotly layout
    :rtype: plotly.graph_objects
    """
    if layout_ == 'map':
        if networkGraphs.type == 'GTFS':
            resolution = 50
        else:
            resolution = 110
        layout = go.Layout(
            title=f'<br>{title}',
            titlefont=dict(size=16, color='Black'),
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
            margin=dict(l=0, r=0, t=0, b=0),
            geo=dict(
                scope='world',
                lataxis_range=[networkGraphs.min_lat, networkGraphs.max_lat],
                lonaxis_range=[networkGraphs.min_long, networkGraphs.max_long],
                center=dict(lat=networkGraphs.mid_lat, lon=networkGraphs.mid_long),
                showland=True,
                showcountries=True,
                resolution=resolution,
            ),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )

    else:
        layout = go.Layout(
            title=f'<br>{title}',
            titlefont=dict(size=16, color='Black'),
            showlegend=False,
            hovermode='closest',
            margin=dict(l=0, r=0, t=0, b=0),
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
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )

    return layout


# ----------------------------------------------------------------------------------------

@memoize
def generate_edge_trace(Graph, pos, layout):
    """
    :Function: Generate the edge trace for the plotly plot, leveraging the memoize decorator for cache optimization
    :param Graph: Network graph
    :type Graph: NetworkGraph
    :param pos: Position of the nodes
    :type pos: dict
    :param layout: Layout of the plot
    :type layout: str
    :return: Edge trace
    :rtype: plotly.graph_objects
    """
    x_list = []
    y_list = []
    for edge in Graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        x_list.extend([x0, x1, None])
        y_list.extend([y0, y1, None])

    if layout == 'map':
        edge_trace = go.Scattergeo(lon=x_list, lat=y_list, hoverinfo='none', mode='lines',
                                   line=dict(width=0.5, color='#888'))
    else:
        edge_trace = go.Scatter(x=x_list, y=y_list, hoverinfo='none', mode='lines', line=dict(width=0.5, color='#888'))

    return edge_trace


def get_file_path(networkGraphs, file_name):
    """
    :Function: Get the file path for the plotly plot
    :param networkGraphs: Network graph
    :type networkGraphs: NetworkGraph
    :param file_name: Name of the file
    :type file_name: str
    :return: Filepath
    :rtype: str
    """
    folder = f"{networkGraphs.session_folder}/"
    if not os.path.isdir(folder):
        os.mkdir(folder)

    return f"{folder}{file_name}"
