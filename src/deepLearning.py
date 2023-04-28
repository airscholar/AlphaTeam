"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Deep learning module contains functions for deep learning
"""

# ----------------------------------------- Imports ----------------------------------------- #

# External imports
from node2vec import Node2Vec

# Internal imports
from src.DeepLearning.embedding import *
from src.metrics import get_metrics
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


def get_similar_nodes(networkGraph, node, model, k=10):
    """
    :Function: Get similar nodes to a given node using Node2Vec embedding model
    :param networkGraph: Network graph
    :param node: Node
    :param model: Node2Vec model
    :param k: Number of similar nodes (default: 10)
    :return: similar_nodes
    :rtype: list
    """
    similar_nodes = model.wv.most_similar(str(node), topn=k)
    # similar_nodes = [int(node[0]) for node in similar_nodes]
    similar_nodes = [node for node in similar_nodes if node in networkGraph.Graph.nodes()]

    return similar_nodes


# --------------------------------------------------------------------------------------------- #


def get_DL_embedding(networkGraphs, model, features, dimension=128, epochs=200):
    """
    :Function: Get deep learning embedding
    :param networkGraphs: Network graphs
    :param model: Deep learning model
    :param features: Features
    :param dimension: Dimension of the embedding
    :return: embeddings
    :rtype: numpy.ndarray
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    if features == ['proximity']:
        nodes = networkGraphs.Graph.number_of_nodes()
        data_features = np.eye(nodes)
        proximity = True
    else:
        data_features = []
        for metric in features:
            proximity = False
            df = get_metrics(networkGraphs, metric, directed=False, multi=False)
            np_arr = np.array(df.iloc[:, 1].values)
            if np.isnan(np_arr).any():
                np_arr = np.nan_to_num(np_arr)
            # np_arr = (np_arr - np_arr.min()) / (np_arr.max() - np_arr.min())
            data_features.append(np_arr)
        data_features = np.array(data_features).T

    data = preprocess_data(networkGraphs.Graph, data_features)
    if features == ['proximity']:
        positive_pairs, negative_pairs = generate_pairs(networkGraphs.Graph, num_negative_pairs=1000)
        positive_indices, negative_indices = pairs_to_indices(data, positive_pairs, negative_pairs)
        data.positive_pairs = positive_indices
        data.negative_pairs = negative_indices
    embed_dim = data.num_features

    model = get_model(model, data, dimension, embed_dim)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    model = train_model(model, optimizer, data, device, epochs=epochs, proximity=proximity)

    embeddings = get_embeddings(model, data)

    return embeddings


# --------------------------------------------------------------------------------------------- #


def get_model(model, data, dimension, embed_dim):
    """
    :Function: Get deep learning model
    :param model: Deep learning model
    :param data: Data
    :param dimension: Dimension of the embedding
    :param embed_dim: Embedding dimension
    :return: model
    :rtype: torch.nn.Module
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    if model == "GCN":
        model = GCN(data.num_features, dimension, embed_dim).to(device)
    elif model == "SAGE":
        model = SAGE(data.num_features, dimension, embed_dim).to(device)
    elif model == "GAT":
        model = GAT(data.num_features, dimension, embed_dim).to(device)
    else:
        raise ValueError("Model not found")

    return model
