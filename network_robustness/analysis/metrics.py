import networkx as nx


def largest_component(G):
    biggest = max(nx.connected_components(G), key=len)
    return G.subgraph(biggest)


def baseline_metrics(G):
    n = G.number_of_nodes()
    lcc = largest_component(G)

    return {
        "nodes": n,
        "edges": G.number_of_edges(),
        "average_degree": 2 * G.number_of_edges() / n,
        "components": nx.number_connected_components(G),
        "lcc_size": lcc.number_of_nodes(),
        "lcc_fraction": lcc.number_of_nodes() / n,
        "average_shortest_path": nx.average_shortest_path_length(lcc),
        "diameter": nx.diameter(lcc),
        "global_efficiency": nx.global_efficiency(G),
        "clustering": nx.average_clustering(G),
    }