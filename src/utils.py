from src.metrics import *

def memoize(func):
    cache = {}

    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key in cache:
            return cache[key]
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper

def cache_data1(networkGraph):
    """
    Cache the data for the network graph for metrics functions
    :param networkGraph: Network graph
    :return: None
    """
    for directed in [True, False]:
        for multi in [True, False]:
            compute_eigen_centrality(networkGraph, directed=directed, multi=multi)
            compute_betweeness_centrality(networkGraph, directed=directed, multi=multi)
            compute_closeness_centrality(networkGraph, directed=directed, multi=multi)
            compute_degree_centrality(networkGraph, directed=directed, multi=multi)
            compute_load_centrality(networkGraph, directed=directed, multi=multi)
            compute_kcore(networkGraph, directed=directed, multi=multi)
            compute_nodes_degree(networkGraph, directed=directed, multi=multi)
            compute_page_rank(networkGraph, directed=directed, multi=multi)
            compute_triangles(networkGraph, directed=directed, multi=multi)
def cache_data2(networkGraph):
    """
    Cache the data for the network graph for global metrics functions
    :param networkGraph: Network graph
    :return: None
    """
    compute_global_metrics(networkGraph)
    print('Computed global metrics')

def cache_data3(networkGraph):
    """
    Cache the data for the network graph for node metrics functions
    :param networkGraph: Network graph
    :return: Nones
    """
    for directed in [True, False]:
        for multi in [True, False]:
            compute_node_metrics(networkGraph, directed=directed, multi=multi)
            compute_node_centralities(networkGraph, directed=directed, multi=multi)