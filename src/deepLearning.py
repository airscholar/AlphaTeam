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

# ----------------------------------------- CONSTANT ----------------------------------------- #


# ----------------------------------------- Functions ----------------------------------------- #

def node2vec_embedding(networkGraph, p=1, q=1, dimensions=64, walk_length=80, num_walks=10, workers=4):
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
