"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: NetworkGraphs.py contains the NetworkGraphs custom class
"""

# ----------------------------------------- Imports ----------------------------------------- #

# Internal imports
from src.preprocessing import *
from src.visualisation import *

# External imports
import scipy.io as sio
from pandas.api.types import is_numeric_dtype

"""
----------------------------------------------------------------------------------------

INFORMATION ABOUT GRAPH ATTRIBUTES

NODES:
- 'pos': position of the node (x, y) as a tuple, POS IS A DICTIONARY WITH LAYOUTS AS KEYS AND POSITIONS AS VALUES
    - pos['map'] = (lat, long)
    - pos['neato'] = (x, y)
    - pos['twopi'] = (x, y)
    - pos['sfdp'] = (x, y)
    
EDGES:
- 'weight': value of the edge (float) for value graphs, WEIGHT IS A DICTIONARY WITH GRAPH AS KEYS AND WEIGHTS AS VALUES
    - weight['MultiDiGraph'] = float
    - weight['MultiGraph'] = float
    - weight['DiGraph'] = float
    - weight['Graph'] = float
- 'start': time of the start of the edge (int) for temporal graphs
- 'end': time of the end of the edge (int) for temporal graphs
- 'color': color of the edge (string), COLOR IS A DICTIONARY WITH GRAPH AS KEYS AND COLORS AS VALUES
    - color['MultiDiGraph'] = string
    - color['MultiGraph'] = string
    - color['DiGraph'] = string
    - color['Graph'] = string

GRAPHS:
- 'name': name of the graph (string)
- 'type': type of the graph (string) - 'RAILWAY', 'CRYPTO' 'MTX' or 'CUSTOM'
- 'temporal': True if the graph is temporal, False otherwise
- 'spatial': True if the graph is spatial, False otherwise
- 'weighted': True if the graph is weighted, False otherwise

"""


class NetworkGraphs:
    """
    Class containing the NetworkX graphs wrapping functionalities to generalise the use of the MultiDiGraph,
    MultiGraph, DiGraph and Graph. This class store attributes of the graphs to allow effective use of the graphs.
    """

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------- CONSTRUCTOR ------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    def __init__(self, filename, type, session_folder=None, temporal=False, spatial=False, weighted=False):
        """
        Constructor of the NetworkGraphs class. It creates the NetworkX graphs and store the attributes of the graphs.

        File format accepted:
            - .csv
            - .mtx
            - .txt
        Type accepted:
            - 'RAILWAY'
            - 'CRYPTO'
            - 'MTX'
            - 'CUSTOM'
        :param filename: Path to the file containing the dataset to be loaded
        :type filename: str
        :param type: Type of the dataset to be loaded
        :type type: str
        :param session_folder: Path to the folder where the session is stored
        :type session_folder: str
        :param temporal: True if the graph is temporal, False otherwise
        :type temporal: bool
        :param spatial: True if the graph is spatial, False otherwise
        :type spatial: bool
        :param weighted: True if the graph is weighted, False otherwise
        :type weighted: bool
        :return: None
        :rtype: None

        Example:
            >>> graph1 = NetworkGraphs('data/RAILWAY/RAILWAY.csv', 'RAILWAY')
            >>> graph2 = NetworkGraphs('data/CRYPTO/CRYPTO.csv', 'CRYPTO')
            >>> graph3 = NetworkGraphs('data/MTX/MTX.mtx', 'MTX')
            >>> graph4 = NetworkGraphs('data/CUSTOM/CUSTOM.csv', 'CUSTOM')
        """

        self.name = None
        self.type = None
        self.max_lat = None
        self.min_lat = None
        self.max_long = None
        self.min_long = None
        self.temporal = None
        self.spatial = None
        self.weighted = None
        self.DiGraph = None
        self.MultiDiGraph = None
        self.Graph = None
        self.MultiGraph = None
        self.colors = None
        self.mid_lat = None
        self.mid_long = None
        self.session_folder = None
        self.filename = None

        self.set_filename(filename)
        name = filename.split('/')[-1].split('.')[0]
        self.set_name(name)
        self.set_type(type)
        self.set_session_folder(session_folder)

        # ---------------------------------------------- RAILWAY -------------------------------------------------------

        if type == 'RAILWAY':
            self.set_spatial(True)
            self.set_temporal(True)
            self.set_weighted(True)

            self.DiGraph, self.MultiDiGraph = preprocess_railway(filename)
            self.Graph, self.MultiGraph = self.DiGraph.to_undirected(), self.MultiDiGraph.to_undirected()

            self.colors = {'MultiDiGraph': nx.get_edge_attributes(self.MultiDiGraph, 'color').values(),
                           'MultiGraph': nx.get_edge_attributes(self.MultiGraph, 'color').values(),
                           'DiGraph': nx.get_edge_attributes(self.DiGraph, 'color').values(),
                           'Graph': nx.get_edge_attributes(self.Graph, 'color').values()}

            self.df = pd.read_csv(filename, low_memory=False)

        # ---------------------------------------------- CRYPTO --------------------------------------------------------

        elif type == 'CRYPTO':
            self.set_spatial(False)
            self.set_temporal(True)
            self.set_weighted(True)

            self.DiGraph, self.MultiDiGraph = preprocess_crypto(filename)
            self.Graph, self.MultiGraph = self.DiGraph.to_undirected(), self.MultiDiGraph.to_undirected()

            self.colors = None

            self.df = pd.read_csv(filename, low_memory=False)

        # ---------------------------------------------- CUSTOM --------------------------------------------------------

        elif type == 'MTX':
            self.set_spatial(False)
            self.set_temporal(False)
            self.set_weighted(True)

            self.DiGraph, self.MultiDiGraph = preprocess_mtx(filename)
            self.Graph, self.MultiGraph = self.DiGraph.to_undirected(), self.MultiDiGraph.to_undirected()

            self.colors = None

            mtx = sio.mmread(filename)
            coo = mtx.tocoo()
            self.df = pd.DataFrame({'source': coo.row, 'target': coo.col, 'weight': coo.data})

        # ---------------------------------------------- CUSTOM --------------------------------------------------------

        elif type == 'CUSTOM':

            self.DiGraph, self.MultiDiGraph = preprocess_custom(filename)
            self.Graph, self.MultiGraph = self.DiGraph.to_undirected(), self.MultiDiGraph.to_undirected()

            self.df = pd.read_csv(filename, low_memory=False)

            if 'lat1' in self.df.columns and 'lon1' in self.df.columns:
                self.set_spatial(True)

            if 'start' in self.df.columns:
                self.set_temporal(True)

            if 'weight' in self.df.columns:
                self.set_weighted(True)

            if 'color' in self.df.columns:
                self.colors = {'MultiDiGraph': nx.get_edge_attributes(self.MultiDiGraph, 'color').values(),
                               'MultiGraph': nx.get_edge_attributes(self.MultiGraph, 'color').values(),
                               'DiGraph': nx.get_edge_attributes(self.DiGraph, 'color').values(),
                               'Graph': nx.get_edge_attributes(self.Graph, 'color').values()}

        # ---------------------------------------------- SPATIAL -------------------------------------------------------

        self.pos = {}
        # print('start layout computation')
        # self.pos['neato'] = nx.nx_agraph.graphviz_layout(self.Graph, prog='neato')
        # print('neato')
        # self.pos['dot'] = nx.nx_agraph.graphviz_layout(self.Graph, prog='dot')
        # print('dot')
        self.pos['twopi'] = nx.nx_agraph.graphviz_layout(self.Graph, prog='twopi')
        print('twopi')
        # self.pos['fdp'] = nx.nx_agraph.graphviz_layout(self.Graph, prog='fdp')
        # print('fdp')
        self.pos['sfdp'] = nx.nx_agraph.graphviz_layout(self.Graph, prog='sfdp')
        print('sfdp')

        if self.is_spatial():
            self.pos['map'] = nx.get_node_attributes(self.Graph, 'pos')
            location = self.pos['map'].values()
            # add space around the graph
            self.set_min_long(min(location, key=lambda x: x[0])[0] - 0.5)
            self.set_min_lat(min(location, key=lambda x: x[1])[1] - 0.5)
            self.set_max_long(max(location, key=lambda x: x[0])[0] + 0.5)
            self.set_max_lat(max(location, key=lambda x: x[1])[1] + 0.5)
            self.set_mid_long()
            self.set_mid_lat()

        # ---------------------------------------------- TEMPORAL ------------------------------------------------------

        if self.is_temporal():
            self.start = min(nx.get_edge_attributes(self.MultiDiGraph, 'start').values())
            self.end = max(nx.get_edge_attributes(self.MultiDiGraph, 'end').values())

        # ---------------------------------------------- WEIGHTED ------------------------------------------------------

        if self.is_weighted():
            self.weights = {'Graph': list(nx.get_edge_attributes(self.Graph, 'weight').values()),
                            'MultiGraph': list(nx.get_edge_attributes(self.MultiGraph, 'weight').values()),
                            'DiGraph': list(nx.get_edge_attributes(self.DiGraph, 'weight').values()),
                            'MultiDiGraph': list(nx.get_edge_attributes(self.MultiDiGraph, 'weight').values())}
            self.min_weight = {'Graph': min(nx.get_edge_attributes(self.Graph, 'weight').values()),
                               'MultiGraph': min(nx.get_edge_attributes(self.MultiGraph, 'weight').values()),
                               'DiGraph': min(nx.get_edge_attributes(self.DiGraph, 'weight').values()),
                               'MultiDiGraph': min(nx.get_edge_attributes(self.MultiDiGraph, 'weight').values())}

            self.max_weight = {'Graph': max(nx.get_edge_attributes(self.Graph, 'weight').values()),
                               'MultiGraph': max(nx.get_edge_attributes(self.MultiGraph, 'weight').values()),
                               'DiGraph': max(nx.get_edge_attributes(self.DiGraph, 'weight').values()),
                               'MultiDiGraph': max(nx.get_edge_attributes(self.MultiDiGraph, 'weight').values())}

            self.standardize_weights()

        self.clean_dataset()

    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------- END CONSTRUCTOR ---------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ---------------------------------------------- ATTRIBUTES --------------------------------------------------------

    def standardize_weights(self):
        """
        :Function: Standardize the weights of the graph between 0 and 1
        :return: None
        """
        if self.is_weighted():
            for weight in self.weights:
                self.weights[weight] = [(w / self.max_weight[weight]) for w in self.weights[weight]]
        else:
            raise ValueError("The graph is not weighted")

    def update_attributes(self):
        """
        :Function: Update the attributes of the graph
        :return: None
        """
        if self.colors is not None:
            self.colors = {'MultiDiGraph': nx.get_edge_attributes(self.MultiDiGraph, 'color').values(),
                           'MultiGraph': nx.get_edge_attributes(self.MultiGraph, 'color').values(),
                           'DiGraph': nx.get_edge_attributes(self.DiGraph, 'color').values(),
                           'Graph': nx.get_edge_attributes(self.Graph, 'color').values()}

        if self.is_weighted():
            self.weights = {'Graph': list(nx.get_edge_attributes(self.Graph, 'weight').values()),
                            'MultiGraph': list(nx.get_edge_attributes(self.MultiGraph, 'weight').values()),
                            'DiGraph': list(nx.get_edge_attributes(self.DiGraph, 'weight').values()),
                            'MultiDiGraph': list(nx.get_edge_attributes(self.MultiDiGraph, 'weight').values())}
            self.min_weight = {'Graph': min(nx.get_edge_attributes(self.Graph, 'weight').values()),
                               'MultiGraph': min(nx.get_edge_attributes(self.MultiGraph, 'weight').values()),
                               'DiGraph': min(nx.get_edge_attributes(self.DiGraph, 'weight').values()),
                               'MultiDiGraph': min(nx.get_edge_attributes(self.MultiDiGraph, 'weight').values())}

            self.max_weight = {'Graph': max(nx.get_edge_attributes(self.Graph, 'weight').values()),
                               'MultiGraph': max(nx.get_edge_attributes(self.MultiGraph, 'weight').values()),
                               'DiGraph': max(nx.get_edge_attributes(self.DiGraph, 'weight').values()),
                               'MultiDiGraph': max(nx.get_edge_attributes(self.MultiDiGraph, 'weight').values())}

            self.standardize_weights()

        self.pos = {}
        self.pos['twopi'] = nx.nx_agraph.graphviz_layout(self.Graph, prog='twopi')
        self.pos['sfdp'] = nx.nx_agraph.graphviz_layout(self.Graph, prog='sfdp')

        if self.is_spatial():
            self.pos['map'] = nx.get_node_attributes(self.Graph, 'pos')
            location = self.pos['map'].values()
            self.set_min_long(min(location, key=lambda x: x[0])[0] - 0.5)
            self.set_min_lat(min(location, key=lambda x: x[1])[1] - 0.5)
            self.set_max_long(max(location, key=lambda x: x[0])[0] + 0.5)
            self.set_max_lat(max(location, key=lambda x: x[1])[1] + 0.5)
            self.set_mid_long()
            self.set_mid_lat()

        if self.is_temporal():
            self.start = min(nx.get_edge_attributes(self.MultiDiGraph, 'start').values())
            self.end = max(nx.get_edge_attributes(self.MultiDiGraph, 'end').values())

    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------- METHODS -----------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    def clean_dataset(self):
        """
        :Function: Clean the dataframe by formatting the columns values and rounding the float values for display
        purpose
        :return: None
        """

        # if the columns is float round it to 6 decimals
        for column in self.df.columns:
            # if the columns is a number round it to 6 decimals
            if is_numeric_dtype(self.df[column]):
                self.df[column] = self.df[column].round(6)

            if self.df[column].dtype == object:
                self.df[column] = self.df[column].apply(
                    lambda x: x[:6] + '...' + x[-6:] if len(x) > 15 and x[:2] == '0x' else x[:12])

    # ---------------------------------------------- SETTERS -----------------------------------------------------------
    def set_name(self, name):
        """
        :Function: Set the name of the graph
        :param name: the name of the graph
        :return: None
        """
        self.name = name

    def set_type(self, data_type):
        """
        :Function: Set the type of the graph
        Data type can be
         - 'RAILWAY'
         - 'CRYPTO'
         - 'CUSTOM'
        :param data_type:
        :type data_type: str
        :return: None
        """
        if data_type in ['RAILWAY', 'CRYPTO', 'CUSTOM', 'MTX']:
            self.type = data_type
        else:
            raise ValueError("The type must be 'RAILWAY', 'CRYPTO' or 'CUSTOM'")

    def set_max_lat(self, max_lat):
        """
        :Function: Set the maximum latitude of the graph
        :param max_lat: the maximum latitude of the graph
        :type max_lat: float
        :return: None
        """
        self.max_lat = max_lat

    def set_temporal(self, temporal):
        """
        :Function: Set the temporal attribute of the graph
        :param temporal: True if the graph is temporal, False otherwise
        :type temporal: bool
        :return: None
        """
        self.temporal = temporal

    def set_min_lat(self, min_lat):
        """
        :Function: Set the minimum latitude of the graph
        :param min_lat: the minimum latitude of the graph
        :type min_lat: float
        :return: None
        """
        self.min_lat = min_lat

    def set_spatial(self, spatial):
        """
        :Function: Set the spatial attribute of the graph
        :param spatial: True if the graph is spatial, False otherwise
        :type spatial: bool
        :return: None
        """
        self.spatial = spatial

    def set_weighted(self, weighted):
        """
        :Function: Set the weighted attribute of the graph
        :param weighted: True if the graph is weighted, False otherwise
        :type weighted: bool
        :return: None
        """
        self.weighted = weighted

    def set_min_long(self, min_long):
        """
        :Function: Set the minimum longitude of the graph
        :param min_long: the minimum longitude of the graph
        :type min_long: float
        :return: None
        """
        self.min_long = min_long

    def set_max_long(self, max_long):
        """
        :Function: Set the maximum longitude of the graph
        :param max_long: the maximum longitude of the graph
        :type max_long: float
        :return: None
        """
        self.max_long = max_long

    def set_mid_long(self):
        """
        :Function: Set the middle longitude of the graph
        :return: None
        """
        self.mid_long = (self.max_long + self.min_long) / 2

    def set_mid_lat(self):
        """
        :Function: Set the middle latitude of the graph
        :return: None
        """
        self.mid_lat = (self.max_lat + self.min_lat) / 2

    def set_session_folder(self, session_folder):
        """
        :Function: Set the session folder of the graph
        :param session_folder: the session folder of the graph
        :type session_folder: str
        :return: None
        """
        self.session_folder = session_folder

    def set_filename(self, filename):
        """
        :Function: Set the filename of the graph
        :param filename: the filename of the graph
        :type filename: str
        :return: None
        """
        self.filename = filename

    # ---------------------------------------------- IS  -----------------------------------------------------------

    def is_temporal(self):
        """
        :Function: Return True if the graph is temporal, False otherwise
        :return: True if the graph is temporal, False otherwise
        :rtype: bool
        """
        return self.temporal

    def is_spatial(self):
        """
        :Function: Return True if the graph is spatial, False otherwise
        :return: True if the graph is spatial, False otherwise
        :rtype: bool
        """
        return self.spatial

    def is_weighted(self):
        """
        :Function: Return True if the graph is weighted, False otherwise
        :return: True if the graph is weighted, False otherwise
        :rtype: bool
        """
        return self.weighted

    # ---------------------------------------------- GETTERS -----------------------------------------------------------

    def get_graph(self, graph_type):
        """
        :Function: Return the graph of the specified type
        Graph type can be:
            - 'DiGraph'
            - 'MultiDiGraph'
            - 'Graph'
            - 'MultiGraph'
        :param graph_type: the type of the graph
        :type graph_type: str
        :return: the graph of the specified type
        :rtype: networkx.DiGraph or networkx.MultiDiGraph or networkx.Graph or networkx.MultiGraph
        """
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
        """
        :Function: Return the position of the nodes
        :return: the position of the nodes
        :rtype: dict
        """
        if self.is_spatial():
            return self.pos
        else:
            raise ValueError("The graph is not spatial")

    def get_min_long(self):
        """
        :Function: Return the minimum longitude of the graph
        :return: the minimum longitude of the graph
        :rtype: float
        """
        return self.min_long

    def get_max_long(self):
        """
        :Function: Return the maximum longitude of the graph
        :return: the maximum longitude of the graph
        :rtype: float
        """
        return self.max_long

    def get_type(self):
        """
        :Function: Return the type of the graph
        :return: the type of the graph
        :rtype: str
        """
        return self.type

    def get_min_lat(self):
        """
        :Function: Return the minimum latitude of the graph
        :return: the minimum latitude of the graph
        :rtype: float
        """
        return self.min_lat

    def get_max_lat(self):
        """
        :Function: Return the maximum latitude of the graph
        :return: the maximum latitude of the graph
        :rtype: float
        """
        return self.max_lat

    def get_name(self):
        """
        :Function: Return the name of the graph
        :return: the name of the graph
        :rtype: str
        """
        return self.name

    def get_colors(self):
        """
        :Function: Return the colors of the graph
        :return: the colors of the graph
        :rtype: dict
        """
        return self.colors

    def get_weights(self, graph_type):
        """
        :Function: Return the weights of the graph
        :param graph_type: the type of the graph
        :type graph_type: str
        :return: the weights of the graph
        :rtype: dict
        """
        if self.is_weighted():
            return self.weights[graph_type]
        else:
            raise ValueError("The graph is not weighted")

    def get_start(self):
        """
        :Function: Return the start of the graph
        :return: the start of the graph
        :rtype: str
        """
        if self.is_temporal():
            return self.start
        else:
            raise ValueError("The graph is not temporal")

    def get_end(self):
        """
        :Function: Return the end of the graph
        :return: the end of the graph
        :rtype: str
        """
        if self.is_temporal():
            return self.end
        else:
            raise ValueError("The graph is not temporal")

    def get_df(self):
        """
        :Function: Return the dataframe of the graph
        :return: the dataframe of the graph
        :rtype: pandas.DataFrame
        """
        return self.df

    # ---------------------------------------------- PRINT -----------------------------------------------------------

    def __str__(self):
        """
        :Function: Return a string representation of the graph
        :return: a string representation of the graph
        :rtype: str
        """
        return "Name: " + self.get_name() + "\nType: " + self.get_type() + "\nTemporal: " + str(
            self.is_temporal()) + "\nSpatial: " + str(self.is_spatial())
