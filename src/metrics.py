import pandas as pd
import networkx as nx
import numpy as np


def compute_global_metrics(networkx_):
    # compute for directed
    directed = compute_metrics(networkx_)
    # compute for undirected
    undirected = compute_metrics(networkx_.to_undirected())

    return pd.merge(directed, undirected, how='inner',
                    on='Metrics').rename(columns={'Values_x': 'Directed', 'Values_y': 'Undirected'})


def compute_metrics(networkx_):
    # return pandas dataframe
    df = pd.DataFrame()

    try:
        clustering_coefficient = nx.average_clustering(networkx_)
    except:
        clustering_coefficient = 0

    try:
        avg_shortest_path_length = nx.average_shortest_path_length(networkx_)
    except:
        avg_shortest_path_length = 0

    try:
        diameter = nx.diameter(networkx_)
    except:
        diameter = 0

    try:
        radius = nx.radius(networkx_)
    except:
        radius = 0

    records = [
        {"Metrics": "Clustering Coefficient", "Values": clustering_coefficient},
        {"Metrics": "Avg. Shortest Path Length", "Values": avg_shortest_path_length},
        {"Metrics": "Diameter", "Values": diameter},
        {"Metrics": "Radius", "Values": radius},
        {"Metrics": "Number of Nodes", "Values": networkx_.number_of_nodes()},
        {"Metrics": "Number of Edges", "Values": networkx_.number_of_edges()},
        {"Metrics": "Density", "Values": nx.density(networkx_)},
        {"Metrics": "Transitivity", "Values": nx.transitivity(networkx_)},
        {"Metrics": "Avg. Degree", "Values": np.mean(list(dict(networkx_.degree()).values()))},
        {"Metrics": "Avg. Clustering", "Values": np.mean(list(nx.clustering(networkx_).values()))},
        {"Metrics": "Avg. Eigenvector Centrality",
         "Values": np.mean(list(nx.eigenvector_centrality(networkx_).values()))},
        {"Metrics": "Avg. Betweenness Centrality",
         "Values": np.mean(list(nx.betweenness_centrality(networkx_).values()))},
        {"Metrics": "Avg. Closeness Centrality", "Values": np.mean(list(nx.closeness_centrality(networkx_).values()))},
        {"Metrics": "Avg. Degree Centrality", "Values": np.mean(list(nx.degree_centrality(networkx_).values()))},
        {"Metrics": "Avg. Page Rank", "Values": np.mean(list(nx.pagerank(networkx_).values()))},
        {"Metrics": "Avg. Load Centrality", "Values": np.mean(list(nx.load_centrality(networkx_).values()))}
    ]

    for record in records:
        df = pd.concat([df, pd.DataFrame(record, index=[0])], ignore_index=True)

    return df


def compute_connectivity(networkx_):
    return 0


def compute_node_metrics(networkx):
    degree_centrality = compute_degree_centrality(networkx)
    closeness_centrality = compute_closeness_centrality(networkx)
    betweeness_centrality = compute_betweeness_centrality(networkx)
    eigen_centrality = compute_eigen_centrality(networkx)

    df = pd.DataFrame([degree_centrality, closeness_centrality, betweeness_centrality, eigen_centrality]).T
    df.columns = ['Degree Centrality', 'Closeness Centrality', 'Betweeness Centrality', 'Eigenvector Centrality']

    return df


def compute_degree_centrality(networkx_):
    return nx.degree_centrality(networkx_)


def compute_eigen_centrality(networkx_):
    return nx.eigenvector_centrality(networkx_)


def compute_closeness_centrality(networkx_):
    return nx.closeness_centrality(networkx_)


def compute_betweeness_centrality(networkx_):
    return nx.betweenness_centrality(networkx_)