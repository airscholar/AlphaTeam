"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Deep learning embedding module contains functions for deep learning embedding
"""

# ----------------------------------------- Imports ----------------------------------------- #

# External imports
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv, SAGEConv
from torch_geometric.utils import from_networkx
import numpy as np
import random


# Internal imports

# ----------------------------------------- CONSTANT ----------------------------------------- #

# ------------------------------------------- MODEL ------------------------------------------ #


class GCN(torch.nn.Module):
    def __init__(self, num_features, hidden_dim, embed_dim):
        super(GCN, self).__init__()
        self.encoder = GCNConv(num_features, hidden_dim)
        self.decoder = torch.nn.Linear(hidden_dim, embed_dim)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        z = self.encoder(x, edge_index)
        x = self.decoder(z)
        return x


# --------------------------------------------------------------------------------------------- #


class GAT(torch.nn.Module):
    def __init__(self, num_features, hidden_dim, embed_dim):
        super(GAT, self).__init__()
        self.encoder = GATConv(num_features, hidden_dim)
        self.decoder = torch.nn.Linear(hidden_dim, embed_dim)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        z = self.encoder(x, edge_index)
        x = self.decoder(z)
        return x


# --------------------------------------------------------------------------------------------- #


class SAGE(torch.nn.Module):
    def __init__(self, num_features, hidden_dim, embed_dim):
        super(SAGE, self).__init__()
        self.encoder = SAGEConv(num_features, hidden_dim)
        self.decoder = torch.nn.Linear(hidden_dim, embed_dim)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        z = self.encoder(x, edge_index)
        x = self.decoder(z)
        return x


# ------------------------------------------- LOSS ------------------------------------------- #

def unsupervised_loss(recon_x, x):
    mse_loss = F.mse_loss(recon_x, x)
    return mse_loss


# --------------------------------------------------------------------------------------------- #


def contrastive_loss(embeddings, positive_pairs, negative_pairs, margin=1.0):
    positive_distances = torch.norm(embeddings[positive_pairs[:, 0]] - embeddings[positive_pairs[:, 1]], dim=1)
    negative_distances = torch.norm(embeddings[negative_pairs[:, 0]] - embeddings[negative_pairs[:, 1]], dim=1)

    positive_loss = torch.mean(torch.square(positive_distances))
    negative_loss = torch.mean(torch.square(torch.clamp(margin - negative_distances, min=0.0)))

    loss = 0.5 * (positive_loss + negative_loss)
    return loss


# ----------------------------------------- TRAINING ----------------------------------------- #


def train(model, optimizer, data, device, proximity=False):
    model.train()
    optimizer.zero_grad()
    out = model(data.to(device))
    if proximity:
        loss = contrastive_loss(out, data.positive_pairs, data.negative_pairs)
    else:
        loss = unsupervised_loss(out[data.train_mask], data.x[data.train_mask])
    loss.backward()
    optimizer.step()
    return loss.item()


# --------------------------------------------------------------------------------------------- #


def test(model, data, device, proximity=False):
    model.eval()
    out = model(data.to(device))
    if proximity:
        loss = contrastive_loss(out, data.positive_pairs, data.negative_pairs)
    else:
        loss = unsupervised_loss(out[data.test_mask], data.x[data.test_mask])
    return loss.item()


# --------------------------------------------------------------------------------------------- #


def train_model(model, optimizer, data, device, epochs, proximity=False):
    best_loss = float('inf')
    best_weights = None
    for epoch in range(1, epochs + 1):
        loss = train(model, optimizer, data, device, proximity=proximity)
        test_loss = test(model, data, device, proximity=proximity)
        if test_loss < best_loss:
            best_loss = test_loss
            best_weights = model.state_dict()
        if test_loss < 0.01:  # early stopping
            break
        print('Epoch: {:03d}, Loss: {:.5f}, Test Loss: {:.5f}'.format(epoch, loss, test_loss))
    model.load_state_dict(best_weights)
    return model


# ---------------------------------------- PREPROCESS ---------------------------------------- #


def generate_pairs(networkx_graph, num_negative_pairs=None):
    nodes = list(networkx_graph.nodes())

    positive_pairs = np.array([[u, v] for u, v in networkx_graph.edges])

    if num_negative_pairs is None:
        num_negative_pairs = len(positive_pairs)

    negative_pairs = []
    while len(negative_pairs) < num_negative_pairs:
        u, v = random.sample(nodes, 2)
        if not networkx_graph.has_edge(u, v):
            negative_pairs.append([u, v])
    negative_pairs = np.array(negative_pairs)

    return positive_pairs, negative_pairs


# --------------------------------------------------------------------------------------------- #


def pairs_to_indices(data, positive_pairs, negative_pairs):
    node_to_index = {node: i for i, node in enumerate(data.mapping)}

    positive_indices = np.array([[node_to_index.get(u), node_to_index.get(v)] for u, v in positive_pairs if
                                 u in node_to_index and v in node_to_index])
    negative_indices = np.array([[node_to_index.get(u), node_to_index.get(v)] for u, v in negative_pairs if
                                 u in node_to_index and v in node_to_index])

    return positive_indices, negative_indices


# --------------------------------------------------------------------------------------------- #


def preprocess_data(networkx_graph, node_features):
    """
    :Function: Preprocess
    :param networkx_graph: Networkx graph
    :param node_features: Node features
    :return: data
    :rtype: torch_geometric.data.Data
    """
    # Convert to torch_geometric.data.Data
    data = from_networkx(networkx_graph)

    # Add node features
    data.x = torch.tensor(node_features, dtype=torch.float)

    # Add train and test mask
    data.train_mask = torch.zeros(data.num_nodes, dtype=torch.uint8)
    data.train_mask[:data.num_nodes // 2] = 1
    data.test_mask = torch.zeros(data.num_nodes, dtype=torch.uint8)
    data.test_mask[data.num_nodes // 2:] = 1
    data.mapping = {node: i for i, node in enumerate(networkx_graph.nodes)}

    return data


# --------------------------------------------------------------------------------------------- #


def get_embeddings(model, data):
    model.eval()
    with torch.no_grad():
        x, edge_index = data.x, data.edge_index
        embeddings = model.encoder(x, edge_index)
    return embeddings.detach().cpu().numpy()
