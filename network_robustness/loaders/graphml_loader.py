import networkx as nx


def load_graphml(path):
    return nx.Graph(nx.read_graphml(path))