# from src.metrics import
from _md5 import md5

# import jenkins hashing function

red = "\033[0;91m"
green = "\033[0;92m"
yellow = "\033[0;93m"
blue = "\033[0;94m"

networkGraphs_cache = {}

def memoize(func):
    cache = {}
    def wrapper(*args, **kwargs):
        key = (func, args, tuple(sorted(kwargs.items())))
        key_hash = md5(str(key).encode('utf-8')).hexdigest()
        if key_hash in cache:
            print(f"{green}CACHE: Using cache for {func.__name__}, hash: {yellow}{key_hash}")
            return cache[key_hash]
        print(f"{blue}CACHE: Computing value for {func.__name__}, hash: {yellow}{key_hash} ")
        result = func(*args, **kwargs)
        cache[key_hash] = result
        return result

    return wrapper

def set_networkGraph(networkGraph, session_id):
    """
    Set the network graph
    :param networkGraph: Network graph
    :return: None
    """
    networkGraphs_cache[session_id] = networkGraph
    return 0

@memoize
def get_networkGraph(session_id):
    """
    Get the network graph
    :return: Network graph
    """
    return networkGraphs_cache[session_id]

# def cache_data1(networkGraph):
#     """
#     Cache the data for the network graph for metrics functions
#     :param networkGraph: Network graph
#     :return: None
#     """
#     for directed in [True, False]:
#         for multi in [True, False]:
#             compute_eigen_centrality(networkGraph, directed=directed, multi=multi)
#             compute_betweeness_centrality(networkGraph, directed=directed, multi=multi)
#             compute_closeness_centrality(networkGraph, directed=directed, multi=multi)
#             compute_degree_centrality(networkGraph, directed=directed, multi=multi)
#             compute_load_centrality(networkGraph, directed=directed, multi=multi)
#             compute_kcore(networkGraph, directed=directed, multi=multi)
#             compute_nodes_degree(networkGraph, directed=directed, multi=multi)
#             compute_page_rank(networkGraph, directed=directed, multi=multi)
#             compute_triangles(networkGraph, directed=directed, multi=multi)
# def cache_data2(networkGraph):
#     """
#     Cache the data for the network graph for global metrics functions
#     :param networkGraph: Network graph
#     :return: None
#     """
#     compute_global_metrics(networkGraph)
#     print('Computed global metrics')
#
# def cache_data3(networkGraph):
#     """
#     Cache the data for the network graph for node metrics functions
#     :param networkGraph: Network graph
#     :return: Nones
#     """
#     for directed in [True, False]:
#         for multi in [True, False]:
#             compute_node_metrics(networkGraph, directed=directed, multi=multi)
#             compute_node_centralities(networkGraph, directed=directed, multi=multi)
