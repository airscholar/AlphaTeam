import plotly.graph_objects as go
from itertools import zip_longest
from src.visualisation_src.utils_visualisation import *
from tqdm import tqdm


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
