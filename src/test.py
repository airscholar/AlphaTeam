# FILE TO TEST THE FUNCTIONS IN THE SRC FOLDER
import matplotlib.pyplot as plt

from src.NetworkGraphs import NetworkGraphs
from src.preprocessing import *
from src.metrics import *
from src.visualisation import *
from src.machineLearning import *
import time

networkGraph = NetworkGraphs('../datasets/Dune_Eth_transaction.csv', session_folder='plots', type="CRYPTO")
# networkGraph = NetworkGraphs('../datasets/Railway.csv', session_folder='plots', type="RAILWAY")
# spectral_clustering(networkGraph)

# agglomerative_clustering(networkGraph)
plot_cluster(networkGraph, 'dbscan', dynamic=False, layout='sfdp')
# hierarchical_clustering(networkGraph)

import networkx as nx
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt



# def hierarchical_clustering(G):
#     # create a distance matrix based on the shortest path length between nodes in the graph
#     distance_matrix = nx.floyd_warshall_numpy(G)
#
#     # perform hierarchical clustering using the distance matrix
#     linkage_matrix = linkage(distance_matrix, method='average')
#
#     # plot the dendrogram
#     dendrogram(linkage_matrix, labels=list(G.nodes()))
#     plt.xlabel('Nodes')
#     plt.ylabel('Distance')
#     plt.show()
#
# hierarchical_clustering(networkGraph.Graph)