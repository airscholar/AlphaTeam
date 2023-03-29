"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Deep learning module contains functions for deep learning
"""

# ----------------------------------------- Imports ----------------------------------------- #

import networkx as nx
import os as os

# ----------------------------------------- CONSTANT ----------------------------------------- #

DIR = 'lib/node2vec-master/src/main.py'

# ----------------------------------------- Functions ----------------------------------------- #

def node_embedding(networkGraph, multi=False, directed=False):
    """
    Generate a node embedding for the network graph
    :param networkGraph: Network graph
    :return: None
    """
    # if multi:
    #     G = networkGraph.MultiGraph if directed else networkGraph.MultiDiGraph
    # else:
    #     G = networkGraph.Graph if directed else networkGraph.DiGraph
    G = networkGraph
    edge_list = nx.generate_edgelist(G, data=True)
    nx.write_edgelist(G, 'emb/graph.edgelist', data=True)

    # Precompute probabilities and generate walks
    os.system(f"python {DIR}\
              --input {'emb/graph.edgelist'}\
              --output {'emb/graph.emb'}\
              --weighted {'--directed' if directed else ''}")

node_embedding(nx.karate_club_graph(), multi=False, directed=False)