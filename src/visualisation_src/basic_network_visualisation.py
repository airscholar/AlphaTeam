import matplotlib.pyplot as plt
import os
import sys
sys.path.insert(0, os.path.abspath('../'))
from visualisation_src.utils_visualisation import *
from utils import memoize
import networkx as nx

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