"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Deep learning module contains functions for deep learning
"""

# ----------------------------------------- Imports ----------------------------------------- #

# External imports
from node2vec import Node2Vec
import numpy as np
import plotly.graph_objects as go
from src.utils import memoize

# ----------------------------------------- CONSTANT ----------------------------------------- #


# ----------------------------------------- Functions ----------------------------------------- #

@memoize
def node2vec_embedding(networkGraph, p=1, q=1, dimensions=64, walk_length=80, num_walks=10, workers=4):
    """
    :Function: Node2Vec embedding
    :param networkGraph: Network graph
    :param p: Return hyper parameter (default: 1)
    :param q: Inout parameter (default: 1)
    :param dimensions: Dimension of the embedding (default: 64)
    :param walk_length: Length of the random walk (default: 80)
    :param num_walks: Number of random walks (default: 10)
    :param workers: Number of workers (default: 4)
    :return: model_node2vec, embeddings
    :rtype: node2vec.Node2Vec, numpy.ndarray
    """
    node2vec = Node2Vec(networkGraph.DiGraph,
                        dimensions=dimensions,
                        walk_length=walk_length,
                        num_walks=num_walks,
                        workers=workers,
                        p=p,
                        q=q,
                        seed=42)
    model_node2vec = node2vec.fit(window=10, min_count=1, batch_words=4)
    nodes = list(networkGraph.Graph.nodes())
    embeddings = np.array([model_node2vec.wv[str(node)] for node in nodes])

    return model_node2vec, embeddings


# --------------------------------------------------------------------------------------------- #
