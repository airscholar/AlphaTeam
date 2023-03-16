import matplotlib.pyplot as plt
import networkx as nx
from plotly import graph_objects as go
from src.visualisation_src.utils_visualisation import *
from tqdm import tqdm
from itertools import zip_longest
from pyvis import network as net
import matplotlib as mpl
import json


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

def generate_static_metric(networkGraphs, df_, filename, layout_='map'):  # USING PLOTLY
    """
    :Function: Plot the metrics on the graph
    :param networkGraphs: Network graphs
    :param df_: Dataframe with the metrics (first column is the node id) (second column is the metric)
    :param filename: Name of the file to be saved
    :param layout_: Layout to be used
    :return: Plotly plot
    """

    G = networkGraphs.Graph

    if not networkGraphs.is_spatial() and layout_ == 'map':
        layout_ = 'sfdp'
    pos = networkGraphs.pos[layout_]

    metrics_name = df_.columns[1]
    df_['std'] = (df_[metrics_name] - df_[metrics_name].min()) / (df_[metrics_name].max() - df_[metrics_name].min())
    size_ = 5 / (df_['std'].mean())  # normalise the size of the nodes

    if layout_ == 'map':
        node_trace = go.Scattergeo(lon=[], lat=[], text=[], mode='markers', hoverinfo='text',
                                   marker=dict(showscale=True,
                                               colorbar=dict(thickness=10, title=metrics_name, xanchor='left',
                                                             titleside='right'), color=df_[metrics_name],
                                               size=df_['std'] * size_))
    else:
        node_trace = go.Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text',
                                marker=dict(showscale=True,
                                            colorbar=dict(thickness=10, title=metrics_name, xanchor='left',
                                                          titleside='right'), color=df_[metrics_name],
                                            size=df_['std'] * size_))

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
        node_info = f"Node: {node}<br>"
        node_info += f"{metrics_name}: {str(metric_df[metrics_name].values[0])}<br>"
        node_trace['text'] += tuple([node_info])

    layout = get_layout(networkGraphs, title=f"{metrics_name} visualisation using {layout_} layout", layout_=layout_)
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=layout)

    fig.write_html(filename, auto_open=True)
    return fig


# ----------------------------------------------------------------------------------------

def generate_static_all_metrics(networkGraphs, df_, filename, layout_='map'):  # USING PLOTLY
    """
    :Function: Plot the metrics on the graph
    :param networkGraphs: Network graphs
    :param df_: Dataframe with the metrics
    :param filename: Name of the file to be saved
    :param layout_: Layout to be used
    :return: Plotly plot
    """

    G = networkGraphs.Graph

    if not networkGraphs.is_spatial() and layout_ == 'map':
        layout_ = 'sfdp'
    pos = networkGraphs.pos[layout_]

    metrics_names = df_.columns[1:]

    if layout_ == 'map':
        node_trace = go.Scattergeo(lon=[], lat=[], text=[], mode='markers', hoverinfo='text',
                                   marker=dict(showscale=False, size=3, color='black'))
    else:
        node_trace = go.Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text',
                                marker=dict(showscale=False, size=3, color='black'))

    edge_trace = generate_edge_trace(Graph=G, pos=pos, layout=layout_)

    for node in G.nodes():
        x, y = pos[node]
        if layout_ == 'map':
            node_trace['lon'] += tuple([x])
            node_trace['lat'] += tuple([y])
        else:
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
        metric_df = df_[df_['Node'] == node]
        node_info = f"Node: {node}<br>"
        for metric in metrics_names:
            node_info += f"{metric}: {str(metric_df[metric].values[0])}<br>"
        node_trace['text'] += tuple([node_info])

    layout = get_layout(networkGraphs, title=f"Metrics visualisation using {layout_} layout", layout_=layout_)
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=layout)

    fig.write_html(filename, auto_open=True)
    return fig


# ----------------------------------------------------------------------------------------

def generate_dynamic_metric(networkGraphs, df_, filename):  # USING PYVIS
    """
    :Function: Plot the metrics on the graph
    :param networkGraphs: Network graphs
    :param df_: Dataframe with the metrics
    :param filename: Name of the file to be saved
    :return: Pyvis plot
    """
    G = networkGraphs.Graph
    metrics_name = df_.columns[1]
    df_['std'] = df_[metrics_name].apply(
        lambda x: (x - min(df_[metrics_name])) / (max(df_[metrics_name]) - min(df_[metrics_name])))
    size_ = 5 / df_['std'].mean()

    cmap = plt.cm.plasma

    for u, d in G.nodes(data=True):
        metric_df = df_[df_['Node'] == u]
        c = cmap(metric_df['std'].values[0])
        d['color'] = mpl.colors.rgb2hex(c)
        d['size'] = metric_df['std'].values[0] * size_
        d['title'] = f"Node: {u}; {metrics_name}: {str(metric_df[metrics_name].values[0])}"

    for u, v, d in G.edges(data=True):
        d.clear()

    Net = net.Network(height="750px", width="100%", bgcolor="#E4ECF6", font_color="black", notebook=True)
    Net.from_nx(G)
    Net.show_buttons(filter_=['physics', 'edges', 'nodes'])
    Net.options.physics.use_force_atlas_2based(
        params={'central_gravity': 0.01, 'gravity': -50, 'spring_length': 100, 'spring_strength': 0.08, 'damping': 0.4,
                'overlap': 0})
    print(f"Saving {filename}...")
    Net.write_html(filename)

    return Net
