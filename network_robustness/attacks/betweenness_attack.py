import networkx as nx
from .base import run_attack


def pick_highest_betweenness(H):
    scores = nx.betweenness_centrality(H)
    return max(scores, key=scores.get)


def betweenness_attack(G):
    return run_attack(G, pick_highest_betweenness)