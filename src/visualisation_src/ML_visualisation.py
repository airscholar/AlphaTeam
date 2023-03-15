import plotly.graph_objects as go
from itertools import zip_longest
from src.visualisation_src.utils_visualisation import *
from tqdm import tqdm
from pyvis import network as net


# ----------------------------------------------------------------------------------------

def generate_static_cluster(networkGraphs, df_, filename, layout_='map'):  # USING PLOTLY

    G = networkGraphs.Graph

    pos = networkGraphs.pos[layout_]

    edge_trace = go.Scattergeo(lon=[], lat=[], hoverinfo='none', mode='lines', line=dict(width=0.5, color='#888'))
    node_trace = go.Scattergeo(lon=[], lat=[], text=[], mode='markers', hoverinfo='text',
                               marker=dict(showscale=True, size=5, color=[],
                                           colorbar=dict(thickness=10, title='Node Connections', xanchor='left',
                                                         titleside='right')))

    for idx, vals in tqdm(enumerate(zip_longest(G.edges(), G.nodes())), total=G.number_of_edges()):
        edge, node = vals
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['lon'] += tuple([x0, x1, None])
        edge_trace['lat'] += tuple([y0, y1, None])

        if idx < len(G.nodes()):
            x, y = pos[node]
            node_trace['lon'] += tuple([x])
            node_trace['lat'] += tuple([y])
            metric_df = df_[df_['Node'] == node]
            node_info = f"Node: {node}<br>Cluster Id: {str(metric_df['Cluster_id'].values[0])}<br>"
            node_trace['text'] += tuple([node_info])
            node_trace['marker']['color'] += tuple([metric_df['Color'].values[0]])

    layout = get_layout(networkGraphs, title=f"Cluster visualisation using {layout_} layout", layout_=layout_)

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=layout)
    fig.write_html(filename)
    return fig


# ----------------------------------------------------------------------------------------

def generate_dynamic_cluster(networkGraphs, df_, filename):  # USING PYVIS
    """
    :Function: Plot the metrics on the graph
    :param networkGraphs: Network graphs
    :param df_: Dataframe with the metrics
    :param filename: Name of the file to be saved
    :return: Pyvis plot
    """
    G = networkGraphs.Graph
    metrics_name = df_.columns[1]

    for u, d in G.nodes(data=True):
        metric_df = df_[df_['Node'] == u]
        d['color'] = metric_df['Color'].values[0]
        d['size'] = 5
        d['title'] = f"Node: {u}; Cluster Id: {str(metric_df['Cluster_id'].values[0])}"

    for u, v, d in G.edges(data=True):
        d.clear()

    Net = net.Network(height="750px", width="100%", bgcolor="grey", font_color="black", notebook=True)
    Net.from_nx(G)
    # Net.show_buttons(filter_=['physics', 'edges', 'nodes'])
    Net.options.physics.use_force_atlas_2based(
        params={'central_gravity': 0.01, 'gravity': -50, 'spring_length': 100, 'spring_strength': 0.08, 'damping': 0.4,
                'overlap': 0})
    print(f"Saving {filename}...")
    Net.write_html(filename)

    return Net
