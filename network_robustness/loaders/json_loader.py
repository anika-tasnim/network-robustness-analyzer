import json
import networkx as nx


def load_json(path):

    with open(path) as f:
        data = json.load(f)

    G = nx.Graph()
    for node in data["nodes"]:
        G.add_node(node["id"])
    for link in data.get("links", data.get("edges", [])):
        G.add_edge(link["source"], link["target"])
    return G