from pyvis import network as net

from src.utils import memoize
from src.visualisation_src.utils_visualisation import *


# ----------------------------------------------------------------------------------------

@memoize
def static_visualisation(networkGraphs, filepath, directed=True, multi=False, layout_='map'):
    """
    :Function: Plot the NetworkX graph on as map
    :param networkGraphs: Network graphs
    :param directed: Boolean to indicate if the graph is directed or not
    :param multi: for multi graphs
    :return: Matplotlib plot
    """
    G = networkGraphs.Graph

    if not networkGraphs.is_spatial() and layout_ == 'map':
        return ValueError("Graph is not spatial with coordinates")

    pos = networkGraphs.pos[layout_]
    text = [f"Node: {node}" for node in G.nodes()]

    x_list = []
    y_list = []
    for node in G.nodes():
        x, y = pos[node]
        x_list.extend([x])
        y_list.extend([y])

    if layout_ == 'map':
        node_trace = go.Scattergeo(lon=x_list, lat=y_list, text=text, mode='markers', hoverinfo='text',
                                   marker=dict(showscale=True, color='black', size=5))
    else:
        node_trace = go.Scatter(x=x_list, y=y_list, text=text, mode='markers', hoverinfo='text',
                                marker=dict(showscale=True, color='black', size=5))

    edge_trace = generate_edge_trace(Graph=G, pos=pos, layout=layout_)

    layout = get_layout(networkGraphs, title=f"Visualisation using {layout_} layout", layout_=layout_)
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=layout)

    fig.write_html(filepath)

    return fig


# ----------------------------------------------------------------------------------------

@memoize
def dynamic_visualisation(networkGraphs, filepath, directed=True, multi=False):
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

    Net.write_html(filepath)

    return Net
