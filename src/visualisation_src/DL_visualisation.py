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


def umap_visualisation(networkGraphs, embeddings, filename):
    nodes = list(networkGraphs.Graph.nodes())

    umap_model = umap.UMAP(n_neighbors=30, min_dist=0.3, metric='euclidean', random_state=42)
    embeddings_2d = umap_model.fit_transform(embeddings)

    fig = go.Figure()
    fig = get_dl_layout_update(fig, embeddings_2d, nodes, title='UMAP')
    fig.write_html(filename, full_html=False, include_plotlyjs='cdn')

    return filename


# ----------------------------------------------------------------------------------


def TSNE_visualisation(networkGraphs, embeddings, filename):
    nodes = list(networkGraphs.Graph.nodes())

    tsne_model = TSNE(n_components=2, random_state=42)
    embeddings_2d = tsne_model.fit_transform(embeddings)

    fig = go.Figure()
    fig = get_dl_layout_update(fig, embeddings_2d, nodes, title='TSNE')
    fig.write_html(filename, full_html=False, include_plotlyjs='cdn')

    return filename


# ----------------------------------------------------------------------------------


def PCA_visualisation(networkGraphs, embeddings, filename):
    nodes = list(networkGraphs.Graph.nodes())

    pca_model = PCA(n_components=2, random_state=42)
    embeddings_2d = pca_model.fit_transform(embeddings)

    fig = go.Figure()
    fig = get_dl_layout_update(fig, embeddings_2d, nodes, title='PCA')
    fig.write_html(filename, full_html=False, include_plotlyjs='cdn')

    return filename


def get_dl_layout_update(fig, embeddings_2d, nodes, title=None):
    """
    :Function: Get the DL layout update for the plotly plot
    :param fig: Figure
    :param embeddings_2d: 2D embeddings
    :param nodes: Nodes
    :param title: Title of the plot
    :return: Figure
    """
    fig.add_trace(go.Scatter(x=embeddings_2d[:, 0], y=embeddings_2d[:, 1], hovertext=nodes, mode='markers'))

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