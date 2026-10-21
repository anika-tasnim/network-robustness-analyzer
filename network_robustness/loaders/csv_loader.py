import csv
import networkx as nx


def load_csv(path):
    G = nx.Graph()
    with open(path) as f:
        header = f.readline()
        sep = "," if "," in header else None
        for line in f:
            parts = line.strip().split(sep)
            if len(parts) < 2:
                continue
            G.add_edge(parts[0].strip(), parts[1].strip())
    return G