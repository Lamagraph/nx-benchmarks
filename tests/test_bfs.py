from __future__ import annotations

import networkx as nx
import pytest

from tests.conftest import get_bfs_graphs


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    if "name" in metafunc.fixturenames and "graph" in metafunc.fixturenames:
        graphs = get_bfs_graphs()
        metafunc.parametrize("name,graph", graphs)


def test_bfs_layers(benchmark, name: str, graph: nx.Graph, first_node: int) -> None:
    def run_bfs() -> None:
        _ = list(nx.bfs_layers(graph, first_node))

    benchmark(run_bfs)
    benchmark.extra_info["graph_name"] = name
    benchmark.extra_info["nodes"] = graph.number_of_nodes()
    benchmark.extra_info["edges"] = graph.number_of_edges()
    benchmark.extra_info["algorithm"] = "bfs"
