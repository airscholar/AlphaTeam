from enum import Enum
from typing import Type
import networkx as nx


class DatasetType(Enum):
    RAILWAY = 'RAILWAY'
    CRYPTO = 'CRYPTO'
    CUSTOM = 'CUSTOM'


def preprocess(filename_: str, dataset_type: Type[DatasetType]):
    switch = {
        DatasetType.RAILWAY: preprocess_railway,
        DatasetType.CRYPTO: preprocess_crypto,
        DatasetType.CUSTOM: preprocess_custom,
    }
    func = switch.get(dataset_type, lambda _: None)
    return func(filename_)


def preprocess_railway(filename_: str):
    network = {}
    station_id = {}
    with open(filename_, 'r') as f:
        prev_train = None
        prev_station = None

        for line in f:
            train, st_no, st_id, date, arr_time, dep_time, stay_time, mileage, lat, lon = line.split(",")
            lat = float(lat)
            lon = float(lon)

            if train != prev_train:
                prev_station = None
                network[train] = []

            station = {
                "id": int(st_id),
                "name": f"Station {st_id}",
                "lat": lat,
                "lon": lon,
                "from": prev_station["lat"] if prev_station else None,
                "to": None,
            }

            network[train].append(station)

            if prev_station:
                prev_station["to"] = (lat, lon)

            prev_train = train
            prev_station = station

    for train in network:
        for station in network[train]:
            station_id[(station['lat'], station['lon'])] = station['id']

    return convert_to_DiGraph(create_multi_DiGraph(network, station_id))


def create_multi_DiGraph(network, station_id):
    multi_graph = nx.MultiDiGraph()

    # add nodes to the graph
    for stations in network:
        for station in network[stations]:
            # print(station)
            # add note with the localisation for visualization
            multi_graph.add_node(station['id'], pos=(station['lon'], station['lat']))

            from_node = station['id']

            if type(station['to']) is tuple:
                # if the 'to' value is a tuple, create a new node
                to_node = station_id[station['to']]
                multi_graph.add_edge(from_node, to_node)
            else:
                continue

    return multi_graph


def convert_to_DiGraph(multi_graph):
    g_directed = nx.DiGraph()
    for u, v in multi_graph.nodes(data=True):
        g_directed.add_node(u, pos=v['pos'])
    for u, v in multi_graph.edges():
        if g_directed.has_edge(u, v):
            continue
        else:
            g_directed.add_edge(u, v)
    return g_directed


def convert_to_undirected(g_directed):
    return g_directed.to_undirected()

def preprocess_crypto(filename_: str):
    return 0


def preprocess_custom(filename_: str):
    return 0
