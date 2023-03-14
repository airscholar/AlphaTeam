import matplotlib.pyplot as plt
import networkx as nx
from plotly import graph_objects as go


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

    # Add colobar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=metric_.min(), vmax=metric_.max()))
    sm.set_array([])
    cbar = plt.colorbar(sm)
    cbar.set_label(f"{metrics_names} values", rotation=270, labelpad=15)

    return plt


# ----------------------------------------------------------------------------------------


def plot_metrics_on_map(networkGraphs, metrics, title, directed=False, layout='map'):  # USING PLOTLY
    G = networkGraphs.Graph if not directed else networkGraphs.DiGraph

    if not networkGraphs.is_spatial() and layout == 'map':
        layout = 'sfdp'
    pos = networkGraphs.pos[layout]

    if layout == 'map':
        edge_trace = go.Scattergeo(lon=[], lat=[], hoverinfo='none', mode='lines', line=dict(width=0.5, color='#888'))
        node_trace = go.Scattergeo(lon=[], lat=[], text=[], mode='markers', hoverinfo='text',
                                   marker=dict(showscale=True, color=['red'], size=3,
                                               colorbar=dict(thickness=10, title='Node Connections', xanchor='left',
                                                             titleside='right'), line=dict(width=2, color='#FF0000')))
    else:
        edge_trace = go.Scatter(x=[], y=[], hoverinfo='none', mode='lines', line=dict(width=0.5, color='#888'))
        node_trace = go.Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text',
                                marker=dict(showscale=True, color=['red'], size=3,
                                            colorbar=dict(thickness=10, title='Node Connections', xanchor='left',
                                                          titleside='right'), line=dict(width=2, color='#FF0000')))

    for idx, edge in enumerate(G.edges()):
        if layout == 'map':
            edge_trace['lon'] += tuple([pos[edge[0]][0], pos[edge[1]][0], None])
            edge_trace['lat'] += tuple([pos[edge[0]][1], pos[edge[1]][1], None])
        else:
            edge_trace['x'] += tuple([pos[edge[0]][0], pos[edge[1]][0], None])
            edge_trace['y'] += tuple([pos[edge[0]][1], pos[edge[1]][1], None])

    for node in G.nodes():
        if layout == 'map':
            node_trace['lon'] += tuple([pos[node][0]])
            node_trace['lat'] += tuple([pos[node][1]])
        else:
            node_trace['x'] += tuple([pos[node][0]])
            node_trace['y'] += tuple([pos[node][1]])
        df_ = metrics[metrics['Node'] == node]
        node_info = f"Node: {node}<br>Connections: {str(G.degree[node])}<br>"
        for col in df_.columns[1:]:
            node_info += f"{col}: {str(df_[col].values[0])}<br>"

        node_trace['text'] += tuple([node_info])

    layout = get_layout(networkGraphs, title, layout_=layout)
    # plot the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=layout)
    # hash the fig to avoid overwriting the file
    filename = "metrics_visualisation.html"
    fig.write_html(filename)
    return fig
