from pyvis import network as net
from tqdm import tqdm

from src.visualisation_src.utils_visualisation import *


# ----------------------------------------------------------------------------------------

def generate_static_cluster(networkGraphs, df_, filename, algo, layout_='map', nbr=0):  # USING PLOTLY

    G = networkGraphs.Graph

    if not networkGraphs.is_spatial() and layout_ == 'map':
        print(ValueError('No spatial graph'))
        return 'no_graph.html'

    pos = networkGraphs.pos[layout_]

    x_list = []
    y_list = []
    text_list = []
    color_list = []
    for node in tqdm(G.nodes()):
        x, y = pos[node]
        x_list.extend([x])
        y_list.extend([y])
        metric_df = df_[df_['Node'] == node]
        node_info = f"Node: {node}<br>Cluster Id: {str(metric_df['Cluster_id'].values[0])}<br>"
        text_list.extend([node_info])
        color_list.extend([metric_df['Color'].values[0]])

    if layout_ == 'map':
        node_trace = go.Scattergeo(lon=x_list, lat=y_list, text=text_list, mode='markers', hoverinfo='text',
                                   marker=dict(showscale=False, size=5, color=color_list))
    else:
        node_trace = go.Scatter(x=x_list, y=y_list, text=text_list, mode='markers', hoverinfo='text',
                                marker=dict(showscale=False, size=5, color=color_list))

    edge_trace = generate_edge_trace(Graph=G, pos=pos, layout=layout_)

    layout = get_layout(networkGraphs,
                        title=f"{algo} {f'with {nbr} ' if nbr > 0 else ''}clusters using {layout_} layout",
                        layout_=layout_)
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=layout)

    fig.write_html(filename, full_html=False, include_plotlyjs='cdn')
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

    x_list = []
    y_list = []
    for edge in tqdm(G.edges()):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        x_list.extend([x0, x1, None])
        y_list.extend([y0, y1, None])

    fig = go.Figure(go.Densitymapbox(lat=latitude, lon=longitude, z=degree, radius=20, hoverinfo='none'))
    fig.add_scattermapbox(lat=latitude, lon=longitude, mode="markers", text=[], name='Nodes', hoverinfo='none',
                          marker=go.scattermapbox.Marker(size=3, color="white"))
    fig.add_scattermapbox(lat=y_list, lon=x_list, text=[], mode="lines", name='Edges', hoverinfo='none',
                          line=dict(width=0.5, color="darkgrey"))

    fig.update_layout(mapbox_style="stamen-terrain", mapbox_center_lon=networkGraphs.mid_long,
                      mapbox_center_lat=networkGraphs.mid_lat, mapbox_zoom=3.5, margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      legend=dict(orientation="h", yanchor="bottom", y=0.1, xanchor="right", x=1, title="Show/Hide"))

    fig.write_html(filename, full_html=False, include_plotlyjs='cdn')

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

    for u, d in G.nodes(data=True):
        metric_df = df_[df_['Node'] == u]
        d['color'] = metric_df['Color'].values[0]
        d['size'] = 5
        d['title'] = f"Node: {u}; Cluster Id: {str(metric_df['Cluster_id'].values[0])}"

    for u, v, d in G.edges(data=True):
        d.clear()

    Net = net.Network(height="750px", width="100%", bgcolor="#E4ECF6", font_color="black", notebook=True)
    Net.from_nx(G)
    Net.options.physics.use_force_atlas_2based(
        params={'central_gravity': 0.01, 'gravity': -50, 'spring_length': 100, 'spring_strength': 0.08, 'damping': 0.4,
                'overlap': 0})
    Net.write_html(filename, full_html=False, include_plotlyjs='cdn')

    return Net
