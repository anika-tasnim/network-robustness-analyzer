import networkx as nx


def load_gexf(path):
    return nx.Graph(nx.read_gexf(path))