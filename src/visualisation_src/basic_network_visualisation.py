import matplotlib.pyplot as plt
from src.visualisation_src.utils_visualisation import *
from src.utils import memoize
import networkx as nx
from pyvis import network as net

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

    if layout_ == 'map':
        node_trace = go.Scattergeo(lon=[], lat=[], text=[], mode='markers', hoverinfo='text',
                                   marker=dict(showscale=True, color='black', size=5))
    else:
        node_trace = go.Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text',
                                marker=dict(showscale=True, color='black',size=5))

    edge_trace = generate_edge_trace(Graph=G, pos=pos, layout=layout_)

    for node in tqdm(G.nodes()):
        x, y = pos[node]
        if layout_ == 'map':
            node_trace['lon'] += tuple([x])
            node_trace['lat'] += tuple([y])
        else:
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])

    layout = get_layout(networkGraphs, title=f"Visualisation using {layout_} layout", layout_=layout_)
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=layout)

    fig.write_html(filepath, auto_open=True)

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