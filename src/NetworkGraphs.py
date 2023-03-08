"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Class containing the NetworkX graphs
"""

"""
INFORMATION ABOUT GRAPH ATTRIBUTES

NODES:
- 'pos': position of the node (x, y) as a tuple for spatial graphs

EDGES:
- 'weight': value of the edge (float) for value graphs
- 'start': time of the start of the edge (int) for temporal graphs
- 'end': time of the end of the edge (int) for temporal graphs
- 'color': color of the edge (string) for trajectory graphs

GRAPHS:
- 'name': name of the graph (string)
- 'type': type of the graph (string) - 'RAILWAY', 'CRYPTO' or 'CUSTOM'
- 'temporal': True if the graph is temporal, False otherwise
- 'spatial': True if the graph is spatial, False otherwise
- 'weighted': True if the graph is weighted, False otherwise

"""

# ----------------------------------------------------------------------------------------

# Imports
from src.preprocessing import *
from src.metrics import *
from src.visualisation import *

# ----------------------------------------------------------------------------------------


class NetworkGraphs:

    def __init__(self, filename, type, name=None, temporal=False, spatial=False, weighted=False):

        self.filename = filename

        if name is None:
            name = filename.split('/')[-1].split('.')[0]
            self.set_name(name)
        else :
            self.set_name(name)

        self.set_type(type)

        self.set_temporal(temporal)

        self.set_spatial(spatial)

        if type == 'RAILWAY':
            self.set_spatial(True)
            self.set_temporal(True)
            self.set_weighted(False)
            self.DiGraph, self.MultiDiGraph = preprocess_railway(filename)
            self.Graph, self.MultiGraph = self.DiGraph.to_undirected(), self.MultiDiGraph.to_undirected()
            self.colors = nx.get_edge_attributes(self.MultiDiGraph,'color').values()

        elif type == 'CRYPTO':
            self.set_spatial(False)
            self.set_temporal(True)
            self.set_weighted(True)
            self.DiGraph, self.MultiDiGraph = preprocess_crypto(filename)
            self.Graph, self.MultiGraph = self.DiGraph.to_undirected(), self.MultiDiGraph.to_undirected()
            self.colors = None

        if self.is_spatial():
            self.pos = nx.get_node_attributes(self.DiGraph, 'pos')

        if self.is_temporal():
            self.start = min(nx.get_edge_attributes(self.MultiDiGraph, 'start').values())
            self.end = max(nx.get_edge_attributes(self.MultiDiGraph, 'end').values())

        if self.is_weighted():
            self.weights = {}
            self.weights['Graph'] = list(nx.get_edge_attributes(self.Graph, 'weight').values())
            self.weights['MultiGraph'] = list(nx.get_edge_attributes(self.MultiGraph, 'weight').values())
            self.weights['DiGraph'] = list(nx.get_edge_attributes(self.DiGraph, 'weight').values())
            self.weights['MultiDiGraph'] = list(nx.get_edge_attributes(self.MultiDiGraph, 'weight').values())
            self.min_weight = min(nx.get_edge_attributes(self.MultiDiGraph, 'weight').values())
            self.max_weight = max(nx.get_edge_attributes(self.MultiDiGraph, 'weight').values())
            self.standardize_weights()

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_type(self, type):
        if type in ['RAILWAY', 'CRYPTO', 'CUSTOM']:
            self.type = type
        else:
            raise ValueError("The type must be 'RAILWAY', 'CRYPTO' or 'CUSTOM'")

    def get_type(self):
        return self.type

    def set_temporal(self, temporal):
        self.temporal = temporal

    def is_temporal(self):
        return self.temporal

    def set_spatial(self, spatial):
        self.spatial = spatial

    def is_spatial(self):
        return self.spatial

    def set_weighted(self, weighted):
        self.weighted = weighted

    def is_weighted(self):
        return self.weighted

    def get_graph(self, graph_type):
        if graph_type == 'DiGraph':
            return self.DiGraph
        elif graph_type == 'MultiDiGraph':
            return self.MultiDiGraph
        elif graph_type == 'Graph':
            return self.Graph
        elif graph_type == 'MultiGraph':
            return self.MultiGraph
        else:
            raise ValueError("The graph type must be 'DiGraph', 'MultiDiGraph', 'Graph' or 'MultiGraph'")

    def get_pos(self):
        if self.is_spatial():
            return self.pos
        else:
            raise ValueError("The graph is not spatial")

    def standardize_weights(self):
        if self.is_weighted():
            for weight in self.weights:
                self.weights[weight] = [(weight - self.min_weight) / (self.max_weight - self.min_weight) for weight in self.weights[weight]]
        else:
            raise ValueError("The graph is not weighted")


    def __str__(self):
        return "Name: " + self.get_name() + "\nType: " + self.get_type() + "\nTemporal: " + str(self.is_temporal()) + "\nSpatial: " + str(self.is_spatial())
