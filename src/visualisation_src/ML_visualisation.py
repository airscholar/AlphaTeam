import plotly.graph_objects as go
from itertools import zip_longest
from src.visualisation_src.utils_visualisation import *


# ----------------------------------------------------------------------------------------

def generate_static_cluster(networkGraphs, color_map, title, layout='map', directed=False):  # USING PLOTLY
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

    layout = get_layout(networkGraphs, title, layout)

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=layout)

    filename = f'{title}_map_directed.html' if directed else f'{title}_map_undirected.html'
    fig.write_html(filename)
    return fig
