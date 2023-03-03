from pyvis.network import Network
import networkx as nx
import pandas as pd
import json
import numpy as np
import geopandas as gpd
class Railway:
    def __init__(self, filename):
        self.filename = filename
        self.G = None
        self.network = {}
        self.station_id = {}
        self.data = []

    def load_data(self):
        with open(self.filename, 'r') as f:
            prev_train = None
            prev_station = None

            for line in f:
                train, st_no, st_id, date, arr_time, dep_time, stay_time, mileage, lat, lon = line.split(",")
                lat = float(lat)
                lon = float(lon)

                if train != prev_train:
                    prev_station = None
                    self.network[train] = []

                station = {
                    "id": int(st_id),
                    "name": f"Station {st_id}",
                    "lat": lat,
                    "lon": lon,
                    "from": prev_station["lat"] if prev_station else None,
                    "to": None,
                }

                self.network[train].append(station)

                if prev_station:
                    prev_station["to"] = (lat, lon)

                prev_train = train
                prev_station = station
    def set_station_id(self):
        # create hashtable of station id and (lat,long) as key
        for train in self.network:
            for station in self.network[train]:
                self.station_id[(station['lat'], station['lon'])] = station['id']

    def create_network_graph(self):
        # create a network graph of the railway network
        # create an empty graph
        G = nx.Graph()

        # add nodes to the graph
        for stations in self.network:
            for station in self.network[stations]:
                # print(station)
                # add note with the localisation for visualization
                G.add_node(station['id'], pos=(station['lon'], station['lat']))

        # add edges to the graph
        for stations in self.network:
            for station in self.network[stations]:
                from_node = station['id']
                to_node = None

                if type(station['to']) is tuple:
                    # if the 'to' value is a tuple, create a new node
                    to_node = self.station_id[station['to']]
                    G.add_edge(from_node, to_node)
                else:
                    # # if the 'to' value is an existing node, add an edge
                    # to_node = station['to']
                    # G.add_edge(from_node, to_node)
                    continue

        # add the graph to the class
        self.G = G

    def plot_graph(self):
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        china = world[world['name'] == 'China']
        china.plot(figsize=(10, 10))
        import matplotlib.pyplot as plt
        pos = nx.get_node_attributes(self.G, 'pos')
        nx.draw(self.G, pos, with_labels=False, node_size=3, node_color='red')
        # plot axes
        plt.axis('on')
        plt.title("Alpha Team")
        # plot title
        plt.show()

    def get_shortest_path(self, source, target):
        method = "dijkstra"
        weight = "unweighted"

        if source is None:
            if target is None:
                # Find paths between all pairs.
                paths = dict(nx.all_pairs_dijkstra_path(self.G, weight=weight))
            else:
                # Find paths from all nodes co-accessible to the target.
                if self.G.is_directed():
                    self.G = self.G.reverse(copy=False)
                paths = nx.single_source_dijkstra_path(self.G, target, weight=weight)
                # Now flip the paths so they go from a source to the target.
                for target in paths:
                    paths[target] = list(reversed(paths[target]))
        else:
            if target is None:
                # Find paths to all nodes accessible from the source.
                paths = nx.single_source_dijkstra_path(self.G, source, weight=weight)
            else:
                # Find shortest source-target path.
                _, paths = nx.bidirectional_dijkstra(self.G, source, target, weight)

        return paths

    def plot_shortest_path(self, path):
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        china = world[world['name'] == 'China']
        china.plot(figsize=(10, 10))
        import matplotlib.pyplot as plt
        pos = nx.get_node_attributes(self.G, 'pos')
        nx.draw(self.G, pos, with_labels=False, node_size=1, node_color='red')

        nx.draw_networkx_nodes(self.G, pos, nodelist=path, node_size=10, node_color='yellow')
        nx.draw_networkx_edges(self.G, pos, edgelist=list(zip(path, path[1:])), edge_color='yellow',
                               width=3)
        plt.axis('on')
        plt.title(f"Shortest Path between {path[0]} and {path[-1]}")
        plt.show()


if __name__ == '__main__':
    r = Railway('datasets/Railway.csv')
    r.load_data()
    r.set_station_id()
    r.create_network_graph()
    r.plot_graph()
    shortest_path = r.get_shortest_path(1136, 1095)
    print(shortest_path)
    r.plot_shortest_path(shortest_path)
