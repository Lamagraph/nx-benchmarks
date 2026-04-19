from __future__ import annotations

import networkx as nx
import pytest

from tests.conftest import get_sssp_graphs


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    if "name" in metafunc.fixturenames and "graph" in metafunc.fixturenames:
        graphs = get_sssp_graphs()
        metafunc.parametrize("name,graph", graphs)


def test_bellman_ford(benchmark, name: str, graph: nx.Graph, first_node: int) -> None:
    def run_bellman_ford() -> None:
        _ = nx.single_source_bellman_ford(graph, first_node)

    benchmark(run_bellman_ford)
    benchmark.extra_info["graph_name"] = name
    benchmark.extra_info["nodes"] = graph.number_of_nodes()
    benchmark.extra_info["edges"] = graph.number_of_edges()
    benchmark.extra_info["algorithm"] = "sssp"
