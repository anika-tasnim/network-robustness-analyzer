import argparse
from pathlib import Path

from network_robustness.loaders import load_graph
from network_robustness.validation.graph_validator import validate_graph, clean_graph
from network_robustness.analysis.metrics import baseline_metrics
from network_robustness.analysis.connectivity import weak_points
from network_robustness.attacks.base import robustness_score
from network_robustness.attacks.degree_attack import degree_attack
from network_robustness.attacks.betweenness_attack import betweenness_attack
from network_robustness.attacks.kcore_attack import kcore_attack
from network_robustness.attacks.random_failure import random_failure
from network_robustness.visualization.plots import plot_robustness

ATTACKS = {"degree": degree_attack, "betweenness": betweenness_attack,
           "kcore": kcore_attack, "random": random_failure}


def main():
    parser = argparse.ArgumentParser(description="How well does this network survive when nodes fail?")
    parser.add_argument("file", help="network file (.csv, .json, .graphml, .gml, .gexf)")
    parser.add_argument("--output", default="output", help="folder for the plot")
    args = parser.parse_args()

    # 1. Load and validate
    G = load_graph(args.file)
    errors, warnings = validate_graph(G)
    for w in warnings:
        print("warning:", w)
    if errors:
        for e in errors:
            print("ERROR:", e)
        return
    G = clean_graph(G)

    # 2. Baseline metrics
    print("\nBaseline metrics")
    for key, value in baseline_metrics(G).items():
        print(f"  {key:<22} {value:.3f}" if isinstance(value, float) else f"  {key:<22} {value}")

    weak = weak_points(G)
    cut_nodes = sorted(weak["articulation_points"], key=G.degree, reverse=True)
    print("\nWeak points")
    print(f"  {len(cut_nodes)} nodes would split the network if removed")
    print(f"  the most connected of them: {', '.join(str(v) for v in cut_nodes[:5])}")
    print(f"  {len(weak['bridges'])} links would split the network if cut")
    print(f"  for example: {', '.join(f'{u}–{v}' for u, v in weak['bridges'][:5])}")

    # 3-4. Attacks, 6. robustness scores
    print("\nRobustness (higher = more robust)")
    results = {}
    biggest_hit = {}
    for name, attack in ATTACKS.items():
        removed, lcc, eff, order = attack(G)
        results[name] = (removed, lcc, eff)
        r_lcc = robustness_score(removed, lcc)
        r_eff = robustness_score(removed, [e / eff[0] for e in eff])
        print(f"  {name:<12} R(LCC) = {r_lcc:.3f}   R(efficiency) = {r_eff:.3f}")
        print(f"  {'':<12} first removed: {', '.join(str(v) for v in order[:3])}")
        drops = [lcc[i - 1] - lcc[i] for i in range(1, len(lcc))]
        step = drops.index(max(drops))
        biggest_hit[name] = (order[step], max(drops))
        print(f"  {'':<12} biggest single hit: removing {order[step]} cut the LCC by {max(drops):.0%}")

    scores = {name: robustness_score(r, l) for name, (r, l, e) in results.items()}
    worst = min(scores, key=scores.get)
    share = scores[worst] / scores["random"]
    print(f"\nMost damaging attack: {worst} (R = {scores[worst]:.3f}, "
          f"only {share:.0%} of the random-failure score)")
    node, drop = biggest_hit[worst]
    print(f"  its most damaging removal: {node} (LCC fell by {drop:.0%} in one step)")

    # 5. Plot
    Path(args.output).mkdir(exist_ok=True)
    plot_path = Path(args.output) / f"{Path(args.file).stem}_robustness.png"
    plot_robustness(results, f"{Path(args.file).name}: robustness under attack", plot_path)
    print(f"\nPlot saved to {plot_path}")


if __name__ == "__main__":
    main()