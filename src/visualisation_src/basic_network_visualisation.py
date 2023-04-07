"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Basic network visualisation module contains functions for basic network visualisation
"""

# ----------------------------------------- Imports ----------------------------------------- #

# Internal imports
from src.visualisation_src.utils_visualisation import *
from src.JS_scripts import scripts

# External imports
from itertools import zip_longest
from pyvis import network as net


# ----------------------------------------------------------------------------------------

@memoize
def static_visualisation(networkGraphs, filepath, layout_='map'):
    """
    :Function: Plot the NetworkX graph on as map
    :param networkGraphs: Network graphs
    :type networkGraphs: NetworkGraphs
    :param filepath: File path to save the plot
    :type filepath: str
    :param layout_: layout of the graph
    :type layout_: str
    :return: Matplotlib plot
    :rtype: matplotlib.pyplot
    """
    G = networkGraphs.Graph

    if not networkGraphs.is_spatial() and layout_ == 'map':
        print(ValueError('No spatial graph'))
        return '../application/static/no_graph.html'

    pos = networkGraphs.pos[layout_]
    text = [f"Node: {node}" for node in G.nodes()]

    if networkGraphs.colors is None:
        colors = ['red' for _ in range(len(G.edges()))]
    else:
        colors = list(networkGraphs.colors['Graph'])

    if networkGraphs.is_weighted() is None:
        weights = [5 for _ in range(len(G.edges()))]
    else:
        weights = list(networkGraphs.weights['Graph'])
        weights = [w * 10 for w in weights]

    x_ = []
    y_ = []
    x_list = []
    y_list = []
    for idx, vals in enumerate(zip_longest(G.nodes(), G.edges())):
        node, edge = vals
        if idx < len(G.edges()):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            x_list.extend([x0, x1, None])
            y_list.extend([y0, y1, None])
        if idx < len(G.nodes()):
            x, y = pos[node]
            x_.extend([x])
            y_.extend([y])

    fig = go.Figure()

    if layout_ == 'map':
        for i, edge in enumerate(G.edges()):
            fig.add_trace(
                go.Scattergeo(
                    lon=[pos[edge[0]][0], pos[edge[1]][0]],
                    lat=[pos[edge[0]][1], pos[edge[1]][1]],
                    mode='lines', line=dict(width=weights[i], color=colors[i]),
                )
            )
        fig.add_trace(go.Scattergeo(lon=x_, lat=y_, text=text, mode='markers', hoverinfo='text',
                                    marker=dict(showscale=False, color='black', size=2)))
    else:
        for i, edge in enumerate(G.edges()):
            fig.add_trace(
                go.Scatter(
                    x=[pos[edge[0]][0], pos[edge[1]][0]],
                    y=[pos[edge[0]][1], pos[edge[1]][1]],
                    mode='lines', line=dict(width=weights[i], color=colors[i]),
                )
            )
        fig.add_trace(go.Scatter(x=x_, y=y_, text=text, mode='markers', hoverinfo='text',
                                 marker=dict(showscale=False, color='black', size=2)))

    layout = get_layout(networkGraphs, title=f"Visualisation using {layout_} layout", layout_=layout_)
    fig.update_layout(layout)

    fig.write_html(filepath, full_html=False, include_plotlyjs='cdn')
    # open the file and append the JS scripts at the end
    if layout_ == 'map':
        with open(filepath, 'a') as f:
            f.write(scripts['to_clipboard_map'])
    with open(filepath, 'a') as f:
        f.write(scripts['to_clipboard_no_map'])

    return fig


# ----------------------------------------------------------------------------------------

@memoize
def dynamic_visualisation(networkGraphs, filepath, directed=True, multi=False):
    """
    :Function: Plot the NetworkX graph on a dynamic map using pyvis
    :param networkGraphs: Network graphs
    :type networkGraphs: NetworkGraphs
    :param filepath: Path to save the plot
    :type filepath: str
    :param directed: Boolean to indicate if the graph is directed or not
    :type directed: bool
    :param multi: for multi graphs
    :type multi: bool
    :return: Plotly plot
    """
    if multi:
        G = networkGraphs.MultiGraph if not directed else networkGraphs.MultiDiGraph
    else:
        G = networkGraphs.Graph if not directed else networkGraphs.DiGraph

    # noramlise the weights
    weights = [G[u][v]['weight'] for u, v in G.edges()]
    weights = [w / max(weights) * 25 for w in weights]

    # change the weights
    for i, (u, v) in enumerate(G.edges()):
        G[u][v]['weight'] = weights[i]

    Net = net.Network(height="750px", width="100%", bgcolor="grey", font_color="black")
    Net.from_nx(G)
    Net.show_buttons(filter_=['physics', 'edges', 'nodes'])
    Net.options.physics.use_force_atlas_2based(
        params={'central_gravity': 0.01, 'gravity': -50, 'spring_length': 100, 'spring_strength': 0.08, 'damping': 0.4,
                'overlap': 0})

    Net.write_html(filepath)

    return Net
