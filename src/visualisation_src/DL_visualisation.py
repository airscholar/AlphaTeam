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

from src.visualisation_src.utils_visualisation import get_dl_layout_update


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
