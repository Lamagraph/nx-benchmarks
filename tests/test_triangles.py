from __future__ import annotations

import networkx as nx
import pytest

from tests.conftest import get_triangles_graphs


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    if "name" in metafunc.fixturenames and "graph" in metafunc.fixturenames:
        graphs = get_triangles_graphs()
        metafunc.parametrize("name,graph", graphs)


def test_triangles(benchmark, name: str, graph: nx.Graph) -> None:
    def run_triangles() -> None:
        _ = nx.triangles(graph)

    benchmark(run_triangles)
    benchmark.extra_info["graph_name"] = name
    benchmark.extra_info["nodes"] = graph.number_of_nodes()
    benchmark.extra_info["edges"] = graph.number_of_edges()
