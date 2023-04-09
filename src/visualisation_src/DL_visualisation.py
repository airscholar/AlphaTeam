"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: DL_visualisation module contains functions for visualising deep learning
"""

# ----------------------------------- Imports -----------------------------------

import plotly.graph_objects as go
import umap.umap_ as umap
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


# ----------------------------------- Functions -----------------------------------


def umap_visualisation(networkGraphs, embeddings, filename, clusters=None):
    """
    :Function: UMAP visualisation
    :param networkGraphs: networkGraphs
    :type networkGraphs: src.networkGraphs_src.networkGraphs
    :param embeddings: Embeddings
    :type embeddings: numpy.ndarray
    :param filename: filename
    :type filename: str
    :param clusters: number of clusters
    :type clusters: pandas.DataFrame
    :return: filename
    :rtype: str
    """
    nodes = list(networkGraphs.Graph.nodes())

    umap_model = umap.UMAP(n_neighbors=30, min_dist=0.3, metric='euclidean', random_state=42)
    embeddings_2d = umap_model.fit_transform(embeddings)

    fig = go.Figure()
    fig = get_dl_layout_update(fig, embeddings_2d, nodes, title='UMAP', clusters=clusters)
    fig.write_html(filename, full_html=False, include_plotlyjs='cdn')

    return filename


# ----------------------------------------------------------------------------------


def TSNE_visualisation(networkGraphs, embeddings, filename, clusters=None):
    """
    :Function: TSNE visualisation
    :param networkGraphs: networkGraphs
    :type networkGraphs: src.networkGraphs_src.networkGraphs
    :param embeddings: Embeddings
    :type embeddings: numpy.ndarray
    :param filename: filename
    :type filename: str
    :param clusters: number of clusters
    :type clusters: pandas.DataFrame
    :return: filename
    :rtype: str
    """
    nodes = list(networkGraphs.Graph.nodes())

    tsne_model = TSNE(n_components=2, random_state=42)
    embeddings_2d = tsne_model.fit_transform(embeddings)

    fig = go.Figure()
    fig = get_dl_layout_update(fig, embeddings_2d, nodes, title='TSNE', clusters=clusters)
    fig.write_html(filename, full_html=False, include_plotlyjs='cdn')

    return filename


# ----------------------------------------------------------------------------------


def PCA_visualisation(networkGraphs, embeddings, filename, clusters=None):
    """
    :Function: PCA visualisation
    :param networkGraphs: networkGraphs
    :type networkGraphs: src.networkGraphs_src.networkGraphs
    :param embeddings: Embeddings
    :type embeddings: numpy.ndarray
    :param filename:
    :type filename: str
    :param clusters:
    :type clusters: pandas.DataFrame
    :return: filename
    :rtype: str
    """
    nodes = list(networkGraphs.Graph.nodes())

    pca_model = PCA(n_components=2, random_state=42)
    embeddings_2d = pca_model.fit_transform(embeddings)

    fig = go.Figure()
    fig = get_dl_layout_update(fig, embeddings_2d, nodes, title='PCA', clusters=clusters)
    fig.write_html(filename, full_html=False, include_plotlyjs='cdn')

    return filename


def get_dl_layout_update(fig, embeddings_2d, nodes, title=None, clusters=None):
    """
    :Function: Get the DL layout update for the plotly plot
    :param fig: Figure
    :type fig: plotly.graph_objects.Figure
    :param embeddings_2d: 2D embeddings
    :type embeddings_2d: numpy.ndarray
    :param nodes: Nodes
    :type nodes: list
    :param title: Title of the plot
    :type title: str
    :param clusters: Clusters
    :type clusters: pandas.DataFrame
    :return: Figure
    """
    fig.add_trace(go.Scatter(x=embeddings_2d[:, 0], y=embeddings_2d[:, 1], hovertext=nodes, mode='markers'))

    if clusters is not None:
        color_list = []
        for node in nodes:
            metric_df = clusters[clusters['Node'] == node]
            color_list.extend([metric_df['Color'].values[0]])
        fig.update_traces(marker=dict(color=color_list))

    fig.update_layout(
        title=f'{title} visualisation of node embeddings',
        xaxis_title=f'{title} x',
        yaxis_title=f'{title} y',
        hovermode='closest',
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))

    return fig

# ----------------------------------------------------------------------------------


