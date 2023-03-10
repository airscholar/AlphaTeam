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
from src.visualisation import *


# ----------------------------------------------------------------------------------------


class NetworkGraphs:

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------- CONSTRUCTOR ------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    def __init__(self, filename, type, name=None, temporal=False, spatial=False, weighted=False):

        self.filename = filename
        if name is None:
            name = filename.split('/')[-1].split('.')[0]
            self.set_name(name)
        else:
            self.set_name(name)
        self.set_type(type)

        # ---------------------------------------------- RAILWAY -------------------------------------------------------

        if type == 'RAILWAY':
            self.set_spatial(True)
            self.set_temporal(True)
            self.set_weighted(False)

            self.DiGraph, self.MultiDiGraph = preprocess_railway(filename)
            self.Graph, self.MultiGraph = self.DiGraph.to_undirected(), self.MultiDiGraph.to_undirected()

            self.colors = {}
            self.colors['MultiDiGraph'] = nx.get_edge_attributes(self.MultiDiGraph, 'color').values()
            self.colors['MultiGraph'] = nx.get_edge_attributes(self.MultiGraph, 'color').values()
            self.colors['DiGraph'] = nx.get_edge_attributes(self.DiGraph, 'color').values()
            self.colors['Graph'] = nx.get_edge_attributes(self.Graph, 'color').values()

            self.df = pd.read_csv(filename)

        # ---------------------------------------------- CRYPTO --------------------------------------------------------

        elif type == 'CRYPTO':
            self.set_spatial(False)
            self.set_temporal(True)
            self.set_weighted(True)

            self.DiGraph, self.MultiDiGraph = preprocess_crypto(filename)
            self.Graph, self.MultiGraph = self.DiGraph.to_undirected(), self.MultiDiGraph.to_undirected()

            self.colors = None

            self.df = pd.read_csv(filename)

        # ---------------------------------------------- CUSTOM --------------------------------------------------------

        elif type == 'CUSTOM':
            self.set_spatial(False)
            self.set_temporal(False)
            self.set_weighted(False)

            self.DiGraph, self.MultiDiGraph = preprocess_custom(filename)
            self.Graph, self.MultiGraph = self.DiGraph.to_undirected(), self.MultiDiGraph.to_undirected()

            self.colors = None

            self.df = pd.read_csv(filename)

        # ---------------------------------------------- SPATIAL -------------------------------------------------------

        if self.is_spatial():
            self.pos = nx.get_node_attributes(self.Graph, 'pos')
            location = self.pos.values()
            # add space around the graph
            self.set_min_long(min(location, key=lambda x: x[0])[0] - 0.5)
            self.set_min_lat(min(location, key=lambda x: x[1])[1] - 0.5)
            self.set_max_long(max(location, key=lambda x: x[0])[0] + 0.5)
            self.set_max_lat(max(location, key=lambda x: x[1])[1] + 0.5)

        # ---------------------------------------------- TEMPORAL ------------------------------------------------------

        if self.is_temporal():
            self.start = min(nx.get_edge_attributes(self.MultiDiGraph, 'start').values())
            self.end = max(nx.get_edge_attributes(self.MultiDiGraph, 'end').values())

        # ---------------------------------------------- WEIGHTED ------------------------------------------------------

        if self.is_weighted():
            self.weights = {}

            self.weights['Graph'] = list(nx.get_edge_attributes(self.Graph, 'weight').values())
            self.weights['MultiGraph'] = list(nx.get_edge_attributes(self.MultiGraph, 'weight').values())
            self.weights['DiGraph'] = list(nx.get_edge_attributes(self.DiGraph, 'weight').values())
            self.weights['MultiDiGraph'] = list(nx.get_edge_attributes(self.MultiDiGraph, 'weight').values())

            self.min_weight = min(nx.get_edge_attributes(self.MultiDiGraph, 'weight').values())
            self.max_weight = max(nx.get_edge_attributes(self.MultiDiGraph, 'weight').values())

            self.standardize_weights()

    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------- END CONSTRUCTOR ---------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ---------------------------------------------- ATTRIBUTES --------------------------------------------------------

    def standardize_weights(self):
        if self.is_weighted():
            for weight in self.weights:
                self.weights[weight] = [(weight - self.min_weight) / (self.max_weight - self.min_weight) for weight in
                                        self.weights[weight]]
        else:
            raise ValueError("The graph is not weighted")

    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------- METHODS -----------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ---------------------------------------------- SETTERS -----------------------------------------------------------
    def set_name(self, name):
        self.name = name

    def set_type(self, type):
        if type in ['RAILWAY', 'CRYPTO', 'CUSTOM']:
            self.type = type
        else:
            raise ValueError("The type must be 'RAILWAY', 'CRYPTO' or 'CUSTOM'")

    def set_max_lat(self, max_lat):
        self.max_lat = max_lat

    def set_temporal(self, temporal):
        self.temporal = temporal

    def set_min_lat(self, min_lat):
        self.min_lat = min_lat

    def set_spatial(self, spatial):
        self.spatial = spatial

    def set_weighted(self, weighted):
        self.weighted = weighted

    def set_min_long(self, min_long):
        self.min_long = min_long

    def set_max_long(self, max_long):
        self.max_long = max_long

    # ---------------------------------------------- IS  -----------------------------------------------------------

    def is_temporal(self):
        return self.temporal

    def is_spatial(self):
        return self.spatial

    def is_weighted(self):
        return self.weighted

    # ---------------------------------------------- GETTERS -----------------------------------------------------------

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

    def get_min_long(self):
        return self.min_long

    def get_max_long(self):
        return self.max_long

    def get_type(self):
        return self.type

    def get_min_lat(self):
        return self.min_lat

    def get_max_lat(self):
        return self.max_lat

    def get_name(self):
        return self.name

    def get_colors(self):
        return self.colors

    def get_weights(self, graph_type):
        if self.is_weighted():
            return self.weights[graph_type]
        else:
            raise ValueError("The graph is not weighted")

    def get_start(self):
        if self.is_temporal():
            return self.start
        else:
            raise ValueError("The graph is not temporal")

    def get_end(self):
        if self.is_temporal():
            return self.end
        else:
            raise ValueError("The graph is not temporal")

    def get_df(self):
        return self.df

    # ---------------------------------------------- PRINT -----------------------------------------------------------

    def __str__(self):
        return "Name: " + self.get_name() + "\nType: " + self.get_type() + "\nTemporal: " + str(
            self.is_temporal()) + "\nSpatial: " + str(self.is_spatial())
