"""
:Author: Alpha Team Group Project
:Date: March 2023
:Purpose: Preprocess the datasets and create generals NetworkX graphs
"""

# ----------------------------------------------------------------------------------------

from random import randint

# External imports
import networkx as nx
import pandas as pd
import partridge as ptg
import scipy.io as sio


# ----------------------------------------------------------------------------------------


def preprocess_railway(filename_: str):
    """
    :Function: Preprocess the railway dataset and create NetworkX graphs
    :param filename_: Path to the file (csv)
    :type filename_: str
    :return: NetworkX graphs (DiGraph and MultiDiGraph)
    :rtype: list of NetworkX graphs
    """
    network = {}
    station_id = {}
    excluded = 0

    colormap = {
        "G": "red",
        "C": "yellow",
        "D": "green",
        "Z": "blue",
        "T": "purple",
        "K": "orange",
        "Y": "pink",
        "1": "grey", "2": "grey", "3": "grey", "4": "grey", "5": "grey", "6": "grey", "7": "grey", "8": "grey",
        "9": "grey"}

    with open(filename_, 'r') as f:
        excluded = 0
        prev_train = None
        prev_station = None

        for line in f:

            # skip header
            if line.startswith("train"):
                continue

            train, st_no, st_id, date, arr_time, dep_time, stay_time, mileage, lat, lon = line.split(",")
            lat = float(lat)
            lon = float(lon)

            try:
                dep_time = int(dep_time.split(":")[0]) * 60 + int(dep_time.split(":")[1])
            except:
                dep_time = int(float(dep_time) * 24 * 60)

            try:
                arr_time = int(arr_time.split(":")[0]) * 60 + int(arr_time.split(":")[1])
            except:
                arr_time = int(float(arr_time) * 24 * 60)

            if date == "Day 2":
                arr_time += 24 * 60
                dep_time += 24 * 60

            elif date == "Day 3":
                arr_time += 48 * 60
                dep_time += 48 * 60

            elif date == "Day 4":
                arr_time += 72 * 60
                dep_time += 72 * 60

            if train != prev_train:
                prev_station = None
                network[train] = []

            station = {
                "id": int(st_id),
                "name": f"Station {st_id}",
                "lat": lat,
                "lon": lon,
                "start": dep_time,
                "end": None,
                "from": prev_station["lat"] if prev_station else None,
                "to": None,
                "color": None,
            }

            network[train].append(station)

            if prev_station:
                prev_station["to"] = (lat, lon)
                prev_station["end"] = arr_time
                prev_station["color"] = colormap[train[0]]

            prev_train = train
            prev_station = station

    for train in network:
        for station in network[train]:
            station_id[(station['lat'], station['lon'])] = station['id']

    print(f"Excluded {excluded} stations")

    multi_di_graph = create_multi_DiGraph_railway(network, station_id)
    di_graph = convert_to_DiGraph(multi_di_graph)

    multi_di_graph.remove_edges_from(nx.selfloop_edges(multi_di_graph))
    di_graph.remove_edges_from(nx.selfloop_edges(di_graph))
    return [di_graph, multi_di_graph]


# ----------------------------------------------------------------------------------------

def create_multi_DiGraph_railway(network, station_id):
    """
    :Function: Create a MultiDiGraph from the railway dataset JSON object
    :param network: JSON object of the railway dataset
    :type network: dict
    :param station_id: Dictionary of station id per location
    :type station_id: dict
    :return: NetworkX MultiDiGraph
    :rtype: NetworkX MultiDiGraph
    """
    multi_graph = nx.MultiDiGraph()

    for stations in network:
        for station in network[stations]:
            multi_graph.add_node(station['id'], pos=(station['lon'], station['lat']))
            from_node = station['id']

            if type(station['to']) is tuple:
                to_node = station_id[station['to']]
                multi_graph.add_edge(from_node, to_node, start=station['start'], end=station['end'],
                                     color=station['color'], weight=1)
            else:
                continue

    return multi_graph


# ----------------------------------------------------------------------------------------


def convert_to_DiGraph(multi_graph):
    """
    :Function: Create a DiGraph from a MultiDiGraph with the same nodes and edges containing the sum of the weights,
    and conserving the first edge's attributes
    :param multi_graph: NetworkX MultiDiGraph
    :type multi_graph: NetworkX MultiDiGraph
    :return: NetworkX DiGraph
    :rtype: NetworkX DiGraph
    """
    g_directed = nx.DiGraph()
    for u, data in multi_graph.nodes(data=True):
        g_directed.add_node(u)
        for k_, v_ in data.items():
            g_directed.nodes[u][k_] = v_

    for u, v, data in multi_graph.edges(data=True):
        if g_directed.has_edge(u, v):
            # if weight exists, add the new weight to the existing one
            if 'weight' in g_directed.edges[u, v]:
                g_directed.edges[u, v]['weight'] += data['weight']
            continue
        else:
            g_directed.add_edge(u, v)
            for k_, v_ in data.items():
                g_directed.edges[u, v][k_] = v_

    return g_directed


# ----------------------------------------------------------------------------------------


def convert_to_undirected(g_directed):
    """
    :Function: Convert a DiGraph to an undirected graph using NetworkX to_undirected() function
    :param g_directed: NetworkX DiGraph
    :type g_directed: NetworkX DiGraph
    :return: NetworkX Graph
    :rtype: NetworkX Graph
    """
    return g_directed.to_undirected()


# ----------------------------------------------------------------------------------------


def create_temporal_subgraph(networkGraphs, start_time, end_time, step):
    """
    :Function: Create a temporal subgraph from a NetworkGraphs object using the start_time, end_time and step parameters
    :param networkGraphs: Custom NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param start_time: Start time of the temporal subgraph
    :type start_time: int
    :param end_time: End time of the temporal subgraph
    :type end_time: int
    :param step: Step size of the temporal subgraph
    :type step: int
    :return: List of NetworkX DiGraphs
    :rtype: list
    """
    temporal_graphs = []
    for i in range(start_time, end_time, step):
        G = nx.DiGraph()
        # add edges
        for u, v, d in networkGraphs.DiGraph.edges(data=True):
            if d['start'] is None or d['end'] is None:
                continue
            if d['start'] <= i and d['end'] >= i:
                G.add_edge(u, v)
                for k_, v_ in d.items():
                    G.edges[u, v][k_] = v_
        # add node positions
        for u, d in networkGraphs.DiGraph.nodes(data=True):
            G.add_node(u)
            for k_, v_ in d.items():
                G.nodes[u][k_] = v_

        temporal_graphs.append(G)

        print(
            f"\rCreating temporal graphs: {i - start_time + 1}/{end_time - start_time} ({(i - start_time + 1) / (end_time - start_time) * 100:.2f}%)",
            end="")
    return temporal_graphs


# ----------------------------------------------------------------------------------------


def preprocess_crypto(filename_: str):
    """
    :Function: Preprocess the crypto dataset and return a NetworkX DiGraph and MultiDiGraph
    :param filename_: Path to the crypto dataset
    :type filename_: str
    :return: List of NetworkX DiGraph and MultiDiGraph
    :rtype: list
    """
    df = pd.read_csv(filename_)

    MultiDiGraph = nx.MultiDiGraph()
    MultiDiGraph.add_nodes_from(df['from'].unique())
    MultiDiGraph.add_nodes_from(df['to'].unique())
    for from_, to_, value_, time_ in df[['from', 'to', 'value', 'block_time']].values:
        MultiDiGraph.add_edge(from_, to_, weight=value_, start=time_, end=time_ + 1)

    DiGraph = convert_to_DiGraph(MultiDiGraph)

    MultiDiGraph.remove_edges_from(nx.selfloop_edges(MultiDiGraph))
    DiGraph.remove_edges_from(nx.selfloop_edges(DiGraph))

    return [DiGraph, MultiDiGraph]


# ----------------------------------------------------------------------------------------


def preprocess_mtx(filename_: str):
    """
    :Function: Preprocess the mtx dataset and return a NetworkX DiGraph and MultiDiGraph
    :param filename_: Path to the mtx dataset
    :type filename_: str
    :return: List of NetworkX DiGraph and MultiDiGraph
    :rtype: list
    """
    mtx = sio.mmread(filename_)

    MultiDiGraph = nx.MultiDiGraph(mtx)

    # convert node labels to strings to avoid errors when using pyvis from_nx() function
    temp = {}
    for node in MultiDiGraph.nodes():
        temp[node] = str(node)
    MultiDiGraph = nx.relabel_nodes(MultiDiGraph, temp)
    temp = {}
    for edge in MultiDiGraph.edges():
        temp[edge] = str(edge)
    MultiDiGraph = nx.relabel_nodes(MultiDiGraph, temp)

    DiGraph = convert_to_DiGraph(MultiDiGraph)

    MultiDiGraph.remove_edges_from(nx.selfloop_edges(MultiDiGraph))
    DiGraph.remove_edges_from(nx.selfloop_edges(DiGraph))

    return [DiGraph, MultiDiGraph]


# ----------------------------------------------------------------------------------------

def preprocess_custom(filename_: str):
    """
    :Function: Preprocess the custom dataset and return a NetworkX DiGraph and MultiDiGraph
    Dataset must have the following columns:
        - from: Source node
        - to: Target node
    Dataset could have the following columns:
        - weight: Edge weight
        - start: Start time of the edge
        - end: End time of the edge
        - color: Color of the edge
        - lat1: Latitude of the source node
        - lon1: Longitude of the source node
        - lat2: Latitude of the target node
        - lon2: Longitude of the target node
    :param filename_: Path to the custom dataset
    :type filename_: str
    :return: List of NetworkX DiGraph and MultiDiGraph
    :rtype: list
    """
    df = pd.read_csv(filename_)
    df.sort_values(by=['from', 'to'], inplace=True)
    MultiDiGraph = nx.MultiDiGraph()

    # Convert labels to string to avoid errors when using pyvis from_nx() function
    df['from'] = df['from'].astype(str)
    df['to'] = df['to'].astype(str)

    if not 'from' in df.columns and not 'to' in df.columns:
        print('No "from" and "to" columns in the dataset')
        return None

    MultiDiGraph.add_nodes_from(df['from'].unique())
    MultiDiGraph.add_nodes_from(df['to'].unique())

    for from_, to_ in df[['from', 'to']].values:
        MultiDiGraph.add_edge(from_, to_, weight=1)

    if 'lat1' in df.columns and 'lon1' in df.columns:
        for node, lat, lon in df[['from', 'lat1', 'lon1']].values:
            MultiDiGraph.nodes[node]['pos'] = (lon, lat)

    if 'lat2' in df.columns and 'lon2' in df.columns:
        for node, lat, lon in df[['to', 'lat2', 'lon2']].values:
            if not 'pos' in MultiDiGraph.nodes[node]:
                MultiDiGraph.nodes[node]['pos'] = (lon, lat)

    if 'weight' in df.columns:
        idx = [(u, v, k) for u, v, k in MultiDiGraph.edges(keys=True)]
        for i, weight_ in enumerate(df['weight'].values):
            MultiDiGraph.edges[idx[i]]['weight'] = weight_

    if 'start' in df.columns and not 'end' in df.columns:
        for from_, to_, start_ in df[['from', 'to', 'start']].values:
            MultiDiGraph.edges[from_, to_]['start'] = start_
            MultiDiGraph.edges[from_, to_]['end'] = start_

    if 'start' in df.columns and 'end' in df.columns:
        for from_, to_, start_, end_ in df[['from', 'to', 'start', 'end']].values:
            MultiDiGraph.edges[from_, to_]['start'] = start_
            MultiDiGraph.edges[from_, to_]['end'] = end_

    if 'color' in df.columns:
        idx = [(u, v, k) for u, v, k in MultiDiGraph.edges(keys=True)]
        for i, color_ in enumerate(df['color'].values):
            MultiDiGraph.edges[idx[i]]['color'] = color_

    DiGraph = convert_to_DiGraph(MultiDiGraph)
    MultiDiGraph.remove_edges_from(nx.selfloop_edges(MultiDiGraph))
    DiGraph.remove_edges_from(nx.selfloop_edges(DiGraph))
    return [DiGraph, MultiDiGraph]


# ----------------------------------------------------------------------------------------

def preprocess_gtfs(zip_file):
    """
    :Function: Preprocess the gtfs dataset and return a NetworkX DiGraph and MultiDiGraph
    :param zip_file: Path to the gtfs dataset
    :type zip_file: str
    :return: List of NetworkX DiGraph and MultiDiGraph
    :rtype: list
    """
    feed = ptg.load_feed(zip_file)
    stops = feed.stops
    routes = feed.routes
    stop_times = feed.stop_times

    G = nx.MultiDiGraph()

    for index, stop in stops.iterrows():
        G.add_node(stop['stop_id'], pos=(stop['stop_lon'], stop['stop_lat']))

    stop_times_grouped = stop_times.groupby('trip_id')

    for trip_id, trip_stop_times in stop_times_grouped:
        trip_stop_times_sorted = trip_stop_times.sort_values('stop_sequence')
        color = '#%06X' % randint(0, 0xFFFFFF)

        for i in range(len(trip_stop_times_sorted) - 1):
            origin = trip_stop_times_sorted.iloc[i]
            destination = trip_stop_times_sorted.iloc[i + 1]
            G.add_edge(origin['stop_id'], destination['stop_id'], start=origin['departure_time'],
                       end=destination['arrival_time'], color=color, weight=1)

    DiGraph = convert_to_DiGraph(G)
    G.remove_edges_from(nx.selfloop_edges(G))
    DiGraph.remove_edges_from(nx.selfloop_edges(DiGraph))

    return [DiGraph, G]
