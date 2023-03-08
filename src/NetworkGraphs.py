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
- 'value': value of the edge (float) for value graphs
- 'start': time of the start of the edge (int) for temporal graphs
- 'end': time of the end of the edge (int) for temporal graphs

GRAPHS:
- 'name': name of the graph (string)
- 'type': type of the graph (string) - 'RAILWAY', 'CRYPTO' or 'CUSTOM'
- 'temporal': True if the graph is temporal, False otherwise
- 'spatial': True if the graph is spatial, False otherwise

"""

# ----------------------------------------------------------------------------------------

# Imports
from src.preprocessing import *
from src.metrics import *
from src.visualisation import *

# ----------------------------------------------------------------------------------------


class NetworkGraphs:

    def __init__(self, filename, type, name=None, temporal=False, spatial=False):

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
            self.DiGraph, self.MultiDiGraph = preprocess_railway(filename)
            self.Graph, self.MultiGraph = self.DiGraph.to_undirected(), self.MultiDiGraph.to_undirected()

        if self.is_spatial():
            self.pos = nx.get_node_attributes(self.Graph, 'pos')

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

    def __str__(self):
        return "Name: " + self.get_name() + "\nType: " + self.get_type() + "\nTemporal: " + str(self.is_temporal()) + "\nSpatial: " + str(self.is_spatial())
