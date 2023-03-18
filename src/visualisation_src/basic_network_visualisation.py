from itertools import zip_longest

from pyvis import network as net

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
                                    marker=dict(showscale=True, color='black', size=5)))
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
                                 marker=dict(showscale=True, color='black', size=5)))

    layout = get_layout(networkGraphs, title=f"Visualisation using {layout_} layout", layout_=layout_)
    fig.update_layout(layout)

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
