"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Stochastic approximation algorithms
"""

# ------------------------------------------------------------------------------

# External import
import numpy as np
import networkx as nx
from random import random
from scipy.optimize import minimize
import pandas as pd
from tqdm import tqdm


# ------------------------------- UTILS FUNCTIONS -------------------------------------

def get_random_sample(nodes):
    """
    Get random sample of size m from n
    """
    return np.random.choice(nodes, size=2, replace=False)


# -------------------------------------------------------------------------------------

def get_random_node(nodes):
    """
    Get random node from n
    """
    return np.random.choice(nodes, size=1, replace=False)


# -------------------------------------- FUNCTIONS -------------------------------------


def estimate_shortest_path_length(G, iterations=10_000):
    nodes = list(G.nodes())
    lengths = []

    for _ in tqdm(range(iterations)):
        node1, node2 = get_random_sample(nodes)
        try:
            length = nx.shortest_path_length(G, node1, node2)
            lengths.append(length)
        except nx.NetworkXNoPath:
            pass

    df = pd.DataFrame(lengths, columns=['Length'])

    return df


# -------------------------------------------------------------------------------------


def estimate_clustering_coefficient(G, iterations=10_000):
    nodes = list(G.nodes())
    coefficients = []

    for _ in tqdm(range(iterations)):
        node = get_random_node(nodes)[0]
        coefficient = nx.clustering(G, node)
        coefficients.append(coefficient)

    df = pd.DataFrame(coefficients, columns=['Coefficient'])

    return df

# -------------------------------------------------------------------------------------
