import networkx as nx


def weak_points(G):
    return {
        "articulation_points": list(nx.articulation_points(G)),
        "bridges": list(nx.bridges(G)),
        "node_connectivity": nx.node_connectivity(G),
        "edge_connectivity": nx.edge_connectivity(G),
    }