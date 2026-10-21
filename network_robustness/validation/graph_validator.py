import networkx as nx


def validate_graph(G):
    errors = []    # problems that stop the analysis
    warnings = []  # things worth knowing, but we can carry on

    if G.number_of_nodes() < 3:
        errors.append("The network needs at least 3 nodes.")
    if G.number_of_edges() == 0:
        errors.append("The network has no edges.")

    loops = nx.number_of_selfloops(G)
    if loops > 0:
        warnings.append(f"{loops} self-loop(s) found; they will be removed.")

    isolated = nx.number_of_isolates(G)
    if isolated > 0:
        warnings.append(f"{isolated} node(s) have no connections.")

    if G.number_of_nodes() > 0 and not nx.is_connected(G):
        parts = nx.number_connected_components(G)
        warnings.append(f"The network is split into {parts} separate pieces.")

    return errors, warnings


def clean_graph(G):
    H = G.copy()
    H.remove_edges_from(list(nx.selfloop_edges(H)))
    return H