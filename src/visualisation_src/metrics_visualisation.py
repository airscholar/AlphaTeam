import matplotlib.pyplot as plt
import networkx as nx
from plotly import graph_objects as go
from src.visualisation_src.utils_visualisation import *
from tqdm import tqdm
from itertools import zip_longest


# ----------------------------------------------------------------------------------------

def plot_metrics(networkGraphs, df_, layout='map'):  # USING MATPLOTLIB
    """
    :Function: Plot the metrics on the graph
    :param networkGraphs: Network graphs
    :param df_: Dataframe with the metrics (first column is the node id) (second column is the metric)
    :param layout: Layout to be used
    :return: Matplotlib plot
    """
    if not networkGraphs.is_spatial() and layout == 'map':
        ValueError("Graph is not spatial with coordinates")
        plt.title("Graph is not spatial with coordinates")
        return plt

    if layout == 'map':
        plot_map(networkGraphs)
    pos = networkGraphs.pos[layout]

    # get the metrics and standardise them
    metrics_names = df_.columns[1]
    metric_ = df_[metrics_names]
    metric_ = (metric_ - metric_.min()) / (metric_.max() - metric_.min())

    fig, ax = plt.subplots(figsize=(10, 6))
    cmap = plt.cm.plasma
    nx.draw(networkGraphs.Graph, pos, node_color=metric_, cmap=cmap, node_size=metric_ * 30, with_labels=False,
            width=0.5)
    plt.title(f"{metrics_names} visualisation using {layout} layout")

    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=metric_.min(), vmax=metric_.max()))
    sm.set_array([])
    cbar = plt.colorbar(sm)
    cbar.set_label(f"{metrics_names} values", rotation=270, labelpad=15)

    return plt


# ----------------------------------------------------------------------------------------

def generate_static_metric(networkGraphs, df_, layout_='map'):  # USING PLOTLY
    """
    :Function: Plot the metrics on the graph
    :param networkGraphs: Network graphs
    :param df_: Dataframe with the metrics (first column is the node id) (second column is the metric)
    :param layout_: Layout to be used
    :return: Plotly plot
    """

    G = networkGraphs.Graph

    if not networkGraphs.is_spatial() and layout_ == 'map':
        layout_ = 'sfdp'
    pos = networkGraphs.pos[layout_]

    metrics_name = df_.columns[1]
    df_['std'] = (df_[metrics_name] - df_[metrics_name].min()) / (df_[metrics_name].max() - df_[metrics_name].min())
    size_ = 5/df_['std'].mean()  # normalise the size of the nodes

    if layout_ == 'map':
        edge_trace = go.Scattergeo(lon=[], lat=[], hoverinfo='none', mode='lines', line=dict(width=0.5, color='#888'))
        node_trace = go.Scattergeo(lon=[], lat=[], text=[], mode='markers', hoverinfo='text',
                                   marker=dict(showscale=True,
                                               colorbar=dict(thickness=10, title=metrics_name, xanchor='left',
                                                             titleside='right'), color=df_[metrics_name],
                                               size=df_['std'] * size_))
    else:
        edge_trace = go.Scatter(x=[], y=[], hoverinfo='none', mode='lines', line=dict(width=0.5, color='#888'))
        node_trace = go.Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text',
                                marker=dict(showscale=True,
                                            colorbar=dict(thickness=10, title=metrics_name, xanchor='left',
                                                          titleside='right'), color=df_[metrics_name],
                                            size=df_['std'] * size_))

    for idx, vals in tqdm(enumerate(zip_longest(G.edges(), G.nodes())), total=G.number_of_edges()):
        edge, node = vals
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        if layout_ == 'map':
            edge_trace['lon'] += (x0, x1, None)
            edge_trace['lat'] += (y0, y1, None)
        else:
            edge_trace['x'] += (x0, x1, None)
            edge_trace['y'] += (y0, y1, None)
        if idx < len(G.nodes()):
            x, y = pos[node]
            if layout_ == 'map':
                node_trace['lon'] += tuple([x])
                node_trace['lat'] += tuple([y])
            else:
                node_trace['x'] += tuple([x])
                node_trace['y'] += tuple([y])
            metric_df = df_[df_['Node'] == node]
            node_info = f"Node: {node}<br>"
            node_info += f"{metrics_name}: {str(metric_df[metrics_name].values[0])}<br>"
            node_trace['text'] += tuple([node_info])

    layout = get_layout(networkGraphs, f"{metrics_name} visualisation using {layout_} layout", layout_=layout_)
    # plot the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=layout)

    fig.write_html(metrics_name+"_visualisation_"+layout_+".html", auto_open=True)
    return fig
