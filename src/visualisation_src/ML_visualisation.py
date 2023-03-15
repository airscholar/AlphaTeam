from itertools import zip_longest

from tqdm import tqdm

import src.machineLearning as ml
from src.visualisation_src.utils_visualisation import *


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


def generate_hotspot(networkGraphs, hotspot_df):
    """
    :Function: Plot the hotspot for the given graph
    :param networkGraphs: Network graphs
    :param hotspot_df: Hotspot dataframe
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

    return fig
