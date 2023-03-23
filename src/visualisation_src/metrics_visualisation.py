import matplotlib as mpl
import networkx as nx
from pyvis import network as net
from tqdm import tqdm

from src.visualisation_src.utils_visualisation import *

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
        print(ValueError('No spatial graph'))
        return 'no_graph.html'

    pos = networkGraphs.pos[layout_]

    metrics_name = df_.columns[1]
    df_['std'] = (df_[metrics_name] - df_[metrics_name].min()) / (df_[metrics_name].max() - df_[metrics_name].min())
    size_ = 5 / df_['std'].mean()  # normalise the size of the nodes

    x_list = []
    y_list = []
    text_list = []
    for node in tqdm(G.nodes()):
        x, y = pos[node]
        x_list.extend([x])
        y_list.extend([y])
        metric_df = df_[df_['Node'] == node]
        node_info = f"Node: {node}<br>"
        node_info += f"{metrics_name}: {str(metric_df[metrics_name].values[0])}<br>"
        text_list.extend([node_info])

    if layout_ == 'map':
        node_trace = go.Scattergeo(lon=x_list, lat=y_list, text=text_list, mode='markers', hoverinfo='text',
                                   marker=dict(showscale=True,
                                               colorbar=dict(thickness=10, title=metrics_name, xanchor='left',
                                                             titleside='right'), color=df_[metrics_name],
                                               size=df_['std'] * size_))
    else:
        node_trace = go.Scatter(x=x_list, y=y_list, text=text_list, mode='markers', hoverinfo='text',
                                marker=dict(showscale=True,
                                            colorbar=dict(thickness=10, title=metrics_name, xanchor='left',
                                                          titleside='right'), color=df_[metrics_name],
                                            size=df_['std'] * size_))

    edge_trace = generate_edge_trace(Graph=G, pos=pos, layout=layout_)

    layout = get_layout(networkGraphs, title=f"{metrics_name} visualisation using {layout_} layout", layout_=layout_)
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=layout)

    fig.write_html(filename)
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
        print(ValueError('No spatial graph'))
        return 'no_graph.html'

    pos = networkGraphs.pos[layout_]

    metrics_names = df_.columns[1:]

    x_list = []
    y_list = []
    text_list = []
    for node in G.nodes():
        x, y = pos[node]
        x_list.extend([x])
        y_list.extend([y])
        metric_df = df_[df_['Node'] == node]
        node_info = f"Node: {node}<br>"
        for metric in metrics_names:
            node_info += f"{metric}: {str(metric_df[metric].values[0])}<br>"
        text_list.extend([node_info])

    if layout_ == 'map':
        node_trace = go.Scattergeo(lon=x_list, lat=y_list, text=text_list, mode='markers', hoverinfo='text',
                                   marker=dict(showscale=False, size=3, color='black'))
    else:
        node_trace = go.Scatter(x=x_list, y=y_list, text=text_list, mode='markers', hoverinfo='text',
                                marker=dict(showscale=False, size=3, color='black'))

    edge_trace = generate_edge_trace(Graph=G, pos=pos, layout=layout_)

    layout = get_layout(networkGraphs, title=f"Metrics visualisation using {layout_} layout", layout_=layout_)
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=layout)

    fig.write_html(filename)
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


# ----------------------------------------------------------------------------------------

def generate_histogram_metric(df_, filename):
    """
    :Function: Generate histogram of the metrics
    :param df_: Dataframe with the metrics
    :type df_: pd.DataFrame
    :param filename: Name of the file to be saved
    :type filename: str
    :return: Plotly plot
    :rtype: plotly.graph_objects.Figure
    """
    metrics_names = df_.columns[1:]
    metrics = df_[metrics_names].values
    title = f"Histogram distribution of the metric{'s' if len(metrics_names) > 1 else ''}: {', '.join(metrics_names)}"

    fig = go.Figure()
    for i, metric in enumerate(metrics_names):
        fig.add_trace(go.Histogram(x=metrics[:, i], name=metric))

    fig.update_layout(barmode='overlay',
                      title_text=title,
                      xaxis_title="Values",
                      yaxis_title="Count",
                      bargap=0.1, )
    fig.update_traces(opacity=0.75)

    fig.write_html(filename)

    return fig


# ----------------------------------------------------------------------------------------

def generate_boxplot_metric(df_, filename):
    """
    :Function: Generate boxplot of the metrics
    :param df_: Dataframe with the metrics
    :type df_: pd.DataFrame
    :param filename: Name of the file to be saved
    :type filename: str
    :return: Plotly plot
    :rtype: plotly.graph_objects.Figure
    """
    metrics_names = df_.columns[1:]
    metrics = df_[metrics_names].values
    title = f"Boxplot of the metric{'s' if len(metrics_names) > 1 else ''}: {', '.join(metrics_names)}"

    fig = go.Figure()
    for i, metric in enumerate(metrics_names):
        fig.add_trace(go.Box(y=metrics[:, i], name=metric))

    fig.update_layout(title_text=title,
                      xaxis_title="Metrics",
                      yaxis_title="Values",
                      )

    fig.write_html(filename)

    return fig


# ----------------------------------------------------------------------------------------

def generate_violin_metric(df_, filename):
    """
    :Function: Generate violin plot of the metrics
    :param df_: Dataframe with the metrics
    :type df_: pd.DataFrame
    :param filename: Name of the file to be saved
    :type filename: str
    :return: Plotly plot
    :rtype: plotly.graph_objects.Figure
    """
    metrics_names = df_.columns[1:]
    metrics = df_[metrics_names].values
    title = f"Violin plot of the metric{'s' if len(metrics_names) > 1 else ''}: {', '.join(metrics_names)}"

    fig = go.Figure()
    for i, metric in enumerate(metrics_names):
        fig.add_trace(go.Violin(y=metrics[:, i], name=metric, box_visible=True, meanline_visible=True))

    fig.update_layout(title_text=title,
                      xaxis_title="Metrics",
                      yaxis_title="Values",
                      )

    fig.write_html(filename)

    return fig


# ----------------------------------------------------------------------------------------


def generate_heatmap(networkGraph, filename):
    """
    :Function: Show the heatmap of the graph
    :param networkGraph: Network graph
    :type networkGraph: NetworkGraph
    :param filename: Name of the file to be saved
    :type filename: str
    :return: Plotly plot
    """
    G = networkGraph.Graph

    mat = nx.to_scipy_sparse_array(G, nodelist=G.nodes(), weight=None, dtype=None, format='csc')
    mat = mat.todense()
    ax = [str(i) for i in G.nodes()]

    fig = go.Figure(data=go.Heatmap(z=mat, x=ax, y=ax))
    fig.update_layout(title_text="Heatmap of connections between nodes")

    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    fig.write_html(filename)
    return fig
