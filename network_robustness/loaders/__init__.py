from pathlib import Path

from .csv_loader import load_csv
from .json_loader import load_json
from .graphml_loader import load_graphml
from .gml_loader import load_gml
from .gexf_loader import load_gexf

LOADERS = {
    ".csv": load_csv,
    ".json": load_json,
    ".graphml": load_graphml,
    ".gml": load_gml,
    ".gexf": load_gexf,
}


def load_graph(path):
    ext = Path(path).suffix.lower()
    if ext not in LOADERS:
        raise ValueError(f"Unsupported file type '{ext}'. Supported: {', '.join(LOADERS)}")
    return LOADERS[ext](path)