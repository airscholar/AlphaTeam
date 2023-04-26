"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Temporal visualisation module contains functions for generating temporal visualisations
"""

# ----------------------------------------- Imports ----------------------------------------- #

# Internal imports
from src.visualisation_src.utils_visualisation import get_layout

# External imports
import networkx as nx
import plotly.graph_objects as go
import numpy as np
from tqdm import tqdm


# ----------------------------------------------------------------------------------------


def generate_temporal(networkGraphs, filename, layout_='map'):
    """
    :Function: Generate temporal visualisation of the network
    :param networkGraphs: Network graphs
    :type networkGraphs: NetworkGraphs
    :param filename: File name
    :type filename: str
    :param layout_: Layout
    :type layout_: str
    :return: Plotly plot
    :rtype: plotly.graph_objects
    """
    if not networkGraphs.is_spatial() and layout_ == 'map':
        print(ValueError('The graph is not spatial, please choose a different layout'))
        return '../application/static/no_graph.html'

    G = networkGraphs.MultiDiGraph

    fig = go.Figure()

    start = networkGraphs.get_start()
    end = networkGraphs.get_end()
    step = (end - start) / 100

    node_x = []
    node_y = []
    text_list = []
    for node in G.nodes():
        pos = networkGraphs.pos[layout_]
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_info = f"Node: {node}<br>"
        text_list.append(node_info)

    if layout_ == 'map':
        node_trace = go.Scattergeo(
            lon=node_x, lat=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                reversescale=True,
                color='black',
                size=1,
                line_width=1, ),
            text=text_list)
    else:
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                reversescale=True,
                color='black',
                size=1,
                line_width=1, ),
            text=text_list)

    fig.add_trace(node_trace)

    for t in tqdm(np.arange(start, end + step, step)):
        G2 = nx.DiGraph(((source, target, attr) for source, target, attr in G.edges(data=True) if
                         attr['start'] <= t and t <= attr['end']))

        lat = []
        lon = []
        for edge in G2.edges():
            pos = networkGraphs.pos[layout_]
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            lon.extend([x0, x1, None])
            lat.extend([y0, y1, None])

        if layout_ == 'map':
            edge_trace = go.Scattergeo(
                lon=lon, lat=lat,
                mode='lines',
                line=dict(width=1, color='red'),
                opacity=0.8,
            )
        else:
            edge_trace = go.Scatter(
                x=lon, y=lat,
                mode='lines',
                line=dict(width=1, color='red'),
                opacity=0.8,
            )

        fig.add_trace(edge_trace)

    # Create and add slider
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method="update",
            args=[{"visible": [True] + [False] * len(fig.data)},
                  {"title": "Date time " + str(i)}],  # layout attribute
        )
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Frequency: "},
        pad={"t": 50},
        steps=steps,
    )]

    fig.update_layout(sliders=sliders)
    layout = get_layout(networkGraphs, layout_)
    fig.update_layout(layout)

    fig.write_html(filename, full_html=False, include_plotlyjs='cdn')

    return filename
