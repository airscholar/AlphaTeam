"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: DL_visualisation module contains functions for visualising deep learning
"""

# ----------------------------------- Imports -----------------------------------

import numpy as np
import umap
import plotly.graph_objects as go
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA


# ----------------------------------- Functions -----------------------------------


def umap_visualisation(networkGraphs, embeddings, filename):
    nodes = list(networkGraphs.Graph.nodes())

    umap_model = umap.UMAP(n_neighbors=30, min_dist=0.3, metric='euclidean', random_state=42)
    embeddings_2d = umap_model.fit_transform(embeddings)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=embeddings_2d[:, 0], y=embeddings_2d[:, 1], hovertext=nodes, mode='markers'))

    fig.update_layout(
        title='UMAP visualisation of node embeddings',
        xaxis_title='UMAP x',
        yaxis_title='UMAP y',
        hovermode='closest',
        showlegend=False,
    )
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))

    fig.write_html(filename, full_html=False, include_plotlyjs='cdn')

    return filename


# ----------------------------------------------------------------------------------


def TSNE_visualisation(networkGraphs, embeddings, filename):
    nodes = list(networkGraphs.Graph.nodes())

    tsne_model = TSNE(n_components=2, random_state=42)
    embeddings_2d = tsne_model.fit_transform(embeddings)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=embeddings_2d[:, 0], y=embeddings_2d[:, 1], hovertext=nodes, mode='markers'))

    fig.update_layout(
        title='TSNE visualisation of node embeddings',
        xaxis_title='TSNE x',
        yaxis_title='TSNE y',
        hovermode='closest',
        showlegend=False,
    )
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))

    fig.write_html(filename, full_html=False, include_plotlyjs='cdn')

    return filename


# ----------------------------------------------------------------------------------


def PCA_visualisation(networkGraphs, embeddings, filename):
    nodes = list(networkGraphs.Graph.nodes())

    pca_model = PCA(n_components=2, random_state=42)
    embeddings_2d = pca_model.fit_transform(embeddings)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=embeddings_2d[:, 0], y=embeddings_2d[:, 1], hovertext=nodes, mode='markers'))

    fig.update_layout(
        title='PCA visualisation of node embeddings',
        xaxis_title='PCA x',
        yaxis_title='PCA y',
        hovermode='closest',
        showlegend=False,
    )
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))

    fig.write_html(filename, full_html=False, include_plotlyjs='cdn')

    return filename
