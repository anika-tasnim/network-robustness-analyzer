import networkx as nx


def lcc_fraction(H, n):
    if H.number_of_nodes() == 0:
        return 0.0
    return len(max(nx.connected_components(H), key=len)) / n


def efficiency(H, n):
    k = H.number_of_nodes()
    if k < 2:
        return 0.0
    return nx.global_efficiency(H) * k * (k - 1) / (n * (n - 1))


def run_attack(G, pick_target):
    H = G.copy()
    n = G.number_of_nodes()
    order = []
    removed = [0.0]
    lcc = [lcc_fraction(H, n)]
    eff = [efficiency(H, n)]

    while H.number_of_nodes() > 0:
        target = pick_target(H)
        H.remove_node(target)
        order.append(target)

        removed.append((n - H.number_of_nodes()) / n)
        lcc.append(lcc_fraction(H, n))
        eff.append(efficiency(H, n))

    return removed, lcc, eff, order


def robustness_score(removed, values):
    area = 0.0
    for i in range(1, len(removed)):
        width = removed[i] - removed[i - 1]
        height = (values[i] + values[i - 1]) / 2
        area += width * height
    return area