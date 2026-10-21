# Network Robustness Analyzer

**How well does a network survive when its nodes fail?**

This tool loads a network from a file, checks that it is usable, measures its structure, and then removes nodes one by one, either at random or by targeting the most important ones. After every removal it recalculates how connected the network still is, plots how quickly it falls apart, and sums each strategy up in a single robustness score.

Built with Python and [NetworkX](https://networkx.org/).

The idea for this project comes from *A First Course in Network Science* by Filippo Menczer, Santo Fortunato and Clayton A. Davis (Cambridge University Press, 2020), and its discussion of how networks respond to random failures and targeted attacks.

## Features

- **Loads any common graph format**: CSV/TSV edge lists, JSON (node-link), GraphML, GML and GEXF. The format is picked from the file extension.
- **Validates the network** before analysis: too few nodes, no edges, self-loops, isolated nodes, disconnected pieces.
- **Baseline metrics**: nodes, edges, average degree, connected components, largest connected component (LCC), average shortest path, diameter, global efficiency, clustering coefficient.
- **Weak points**: articulation points (nodes whose removal splits the network) and bridges (links whose removal splits it).
- **Four failure strategies**, recalculating after every single removal:
  | Strategy | Removes first |
  |---|---|
  | `random` | a random node (random failure) |
  | `degree` | the node with the most links (hub attack) |
  | `betweenness` | the node on the most shortest paths (the biggest "middleman") |
  | `kcore` | the node in the densest core of the network |
- **Robustness score R**: the area under the curve of LCC size (or efficiency) against the fraction of nodes removed. Higher means more robust; the maximum for node removal is about 0.5.
- **Plots** of the LCC and efficiency curves for all four strategies side by side.

## Installation

```bash
git clone https://github.com/anika-tasnim/network-robustness-analyzer.git
cd network-robustness-analyzer
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py data/geant_europe.csv
python main.py data/got_book1.csv --output results
python main.py --help
```

The plot is saved as `output/<file name>_robustness.png` (or in the folder given with `--output`).

### Input format

A CSV edge list with a header row and one link per line. Commas, spaces or tabs all work, and only the first two columns are used:

```
source,target
A,B
B,C
C,D
```

## Project structure

```
network_robustness/
├── loaders/          # one loader per file format + load_graph() that picks the right one
├── validation/       # graph_validator.py: errors, warnings, clean-up
├── analysis/         # metrics.py, centrality.py, connectivity.py
├── attacks/          # base.py (shared removal loop + robustness score) and the four strategies
└── visualization/    # plots.py: robustness curves
data/                 # sample networks
main.py               # command-line entry point
```

## Limitations

- Networks are treated as **undirected and unweighted**.
- Targeted attacks recalculate scores after every removal. This is accurate but slow on large networks: about 800 nodes takes a few minutes, mostly in the betweenness attack.
- The CSV loader expects a header row and does not handle quoted names that contain commas.

## Data sources

- Game of Thrones: Andrew Beveridge, [mathbeveridge/asoiaf](https://github.com/mathbeveridge/asoiaf) (book 1 edges).
- GEANT 2012: [Internet Topology Zoo](https://github.com/sk2/topologyzoo), converted to CSV with country codes as node names.
- European airports: [OpenFlights](https://github.com/jpatokal/openflights) routes and airports data (2014), routes between airports in 20 European countries.

## References

- Menczer, Fortunato & Davis (2020). *A First Course in Network Science.* Cambridge University Press. (inspiration for this project)
- Albert, Jeong & Barabási (2000). *Error and attack tolerance of complex networks.* Nature 406, 378–382.
- Schneider et al. (2011). *Mitigation of malicious attacks on networks.* PNAS 108(10), 3838–3841. (robustness measure R)
- Latora & Marchiori (2001). *Efficient behavior of small-world networks.* Physical Review Letters 87, 198701. (global efficiency)
