import networkx as nx


def node_scores(G):
    return {
        "degree": nx.degree_centrality(G),
        "betweenness": nx.betweenness_centrality(G),
        "core": nx.core_number(G),
    }


def top_nodes(scores, k=5):
    return sorted(scores, key=scores.get, reverse=True)[:k]