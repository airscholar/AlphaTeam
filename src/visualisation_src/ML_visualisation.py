import plotly.graph_objects as go
from itertools import zip_longest
from src.visualisation_src.utils_visualisation import *
from tqdm import tqdm
from pyvis import network as net

import src.machineLearning as ml
from src.visualisation_src.utils_visualisation import *


# ----------------------------------------------------------------------------------------

def generate_static_cluster(networkGraphs, df_, filename, layout_='map'):  # USING PLOTLY

    G = networkGraphs.Graph

    if not networkGraphs.is_spatial() and layout_ == 'map':
        layout_ = 'sfdp'
    pos = networkGraphs.pos[layout_]

    if layout_ == 'map':
        node_trace = go.Scattergeo(lon=[], lat=[], text=[], mode='markers', hoverinfo='text',
                                   marker=dict(showscale=False, size=5, color=[]))
    else:
        node_trace = go.Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text',
                                marker=dict(showscale=False, size=5, color=[]))

    edge_trace = generate_edge_trace(Graph=G, pos=pos, layout=layout_)

    for node in tqdm(G.nodes()):
        x, y = pos[node]
        if layout_ == 'map':
            node_trace['lon'] += tuple([x])
            node_trace['lat'] += tuple([y])
        else:
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
        metric_df = df_[df_['Node'] == node]
        node_info = f"Node: {node}<br>Cluster Id: {str(metric_df['Cluster_id'].values[0])}<br>"
        node_trace['text'] += tuple([node_info])
        node_trace['marker']['color'] += tuple([metric_df['Color'].values[0]])

    layout = get_layout(networkGraphs, title=f"Cluster visualisation using {layout_} layout", layout_=layout_)
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=layout)

    fig.write_html(filename, auto_open=True)
    return fig


# ----------------------------------------------------------------------------------------

def generate_hotspot(networkGraphs, hotspot_df, filename):
    """
    :Function: Plot the hotspot for the given graph
    :param networkGraphs: Network graphs
    :param hotspot_df: Hotspot dataframe
    :param filename: Filename
    :return:
    """
    latitude = hotspot_df['Latitude']
    longitude = hotspot_df['Longitude']
    degree = hotspot_df['Degree']
    pos = networkGraphs.pos['map']
    G = networkGraphs.Graph

    fig = go.Figure(go.Densitymapbox(lat=latitude, lon=longitude, z=degree, radius=20, hoverinfo='none'))
    fig.add_scattermapbox(lat=latitude, lon=longitude, mode="markers", text=[], name='Nodes', hoverinfo='none',
                          marker=go.scattermapbox.Marker(size=3, color="white"))
    fig.add_scattermapbox(lat=[], lon=[], text=[], mode="lines", name='Edges', hoverinfo='none',
                          line=dict(width=0.5, color="darkgrey"))

    for idx, vals in tqdm(enumerate(zip_longest(G.edges(), G.nodes())), total=G.number_of_edges()):
        edge, node = vals
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        fig.data[2]['lon'] += (x0, x1, None)
        fig.data[2]['lat'] += (y0, y1, None)

    fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=networkGraphs.mid_long,
                      mapbox_center_lat=networkGraphs.mid_lat, mapbox_zoom=3.5, margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      legend=dict(orientation="h", yanchor="bottom", y=0.1, xanchor="right", x=1, title="Show/Hide"))

    fig.write_html(filename, auto_open=True)

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

    Net = net.Network(height="750px", width="100%", bgcolor="#E4ECF6", font_color="black", notebook=True)
    Net.from_nx(G)
    # Net.show_buttons(filter_=['physics', 'edges', 'nodes'])
    Net.options.physics.use_force_atlas_2based(
        params={'central_gravity': 0.01, 'gravity': -50, 'spring_length': 100, 'spring_strength': 0.08, 'damping': 0.4,
                'overlap': 0})
    print(f"Saving {filename}...")
    Net.write_html(filename)

    return Net
