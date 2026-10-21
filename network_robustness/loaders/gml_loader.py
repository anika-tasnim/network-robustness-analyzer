import networkx as nx


def load_gml(path):
    return nx.Graph(nx.read_gml(path))