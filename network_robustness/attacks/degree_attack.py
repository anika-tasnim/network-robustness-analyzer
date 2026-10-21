import networkx as nx

from .base import run_attack


def pick_highest_degree(H):
    degrees = dict(H.degree())
    return max(degrees, key=degrees.get)


def degree_attack(G):
    return run_attack(G, pick_highest_degree)