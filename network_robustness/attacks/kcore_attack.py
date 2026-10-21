import networkx as nx
from .base import run_attack


def pick_highest_core(H):
    core = nx.core_number(H)
    degree = dict(H.degree())
    return max(H.nodes, key=lambda v: (core[v], degree[v]))


def kcore_attack(G):
    return run_attack(G, pick_highest_core)