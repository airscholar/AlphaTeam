import matplotlib.pyplot as plt
import os
import sys
sys.path.insert(0, os.path.abspath('../'))
from visualisation_src.utils_visualisation import *
from utils import memoize
import networkx as nx
from pyvis import network as net

# ----------------------------------------------------------------------------------------

@memoize
def static_visualisation(networkGraphs, directed=True, multi=False, layout='map'):
    """
    :Function: Plot the NetworkX graph on as map
    :param networkGraphs: Network graphs
    :param directed: Boolean to indicate if the graph is directed or not
    :param multi: for multi graphs
    :return: Matplotlib plot
    """
    if not networkGraphs.is_spatial() and layout == 'map':
        ValueError("Graph is not spatial with coordinates")

    if layout == 'map':
        plot_map(networkGraphs)

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
    plt.title(f"{networkGraphs.name} using {layout}")

    return plt

# ----------------------------------------------------------------------------------------

@memoize
def dynamic_visualisation(networkGraphs, directed=True, multi=False):
    """
    :Function: Plot the NetworkX graph on a dynamic map using pyvis
    :param networkGraphs: Network graphs
    :param directed: Boolean to indicate if the graph is directed or not
    :param multi: for multi graphs
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
    filename = f"Dynamic_{directed}_{multi}.html"
    Net.write_html(filename)

    return Net