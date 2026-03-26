from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import networkx as nx
import pytest
from scipy.io import mmread

if TYPE_CHECKING:
    pass


def load_mtx_graph(filepath: Path) -> nx.Graph:
    m = mmread(filepath)
    return nx.from_scipy_sparse_array(m)


def discover_mtx_files(directory: str) -> list[Path]:
    dir_path = Path(directory)
    if not dir_path.exists():
        return []
    return sorted(dir_path.glob("*.mtx"))


def get_bfs_graphs() -> list[tuple[str, nx.Graph]]:
    graphs: list[tuple[str, nx.Graph]] = []
    for mtx_path in discover_mtx_files("bfs"):
        try:
            G = load_mtx_graph(mtx_path)
            graphs.append((mtx_path.stem, G))
        except Exception:
            pass
    return graphs


def get_sssp_graphs() -> list[tuple[str, nx.Graph]]:
    graphs: list[tuple[str, nx.Graph]] = []
    for mtx_path in discover_mtx_files("sssp"):
        try:
            G = load_mtx_graph(mtx_path)
            graphs.append((mtx_path.stem, G))
        except Exception:
            pass
    return graphs


def get_triangles_graphs() -> list[tuple[str, nx.Graph]]:
    graphs: list[tuple[str, nx.Graph]] = []
    for mtx_path in discover_mtx_files("triangles"):
        try:
            G = load_mtx_graph(mtx_path)
            graphs.append((mtx_path.stem, G))
        except Exception:
            pass
    return graphs


@pytest.fixture(scope="session")
def first_node() -> int:
    return 0


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "benchmark: mark test as a benchmark")
