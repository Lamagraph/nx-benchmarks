# NetworkX Benchmark Suite

Benchmark BFS, SSSP (Bellman-Ford), and Triangle Counting algorithms in NetworkX using graphs in Matrix Market format.

## Algorithms

| Algorithm | NetworkX Function | Description |
|-----------|-------------------|-------------|
| BFS | `networkx.bfs_layers(G, source)` | Breadth-first search layers |
| SSSP | `networkx.single_source_bellman_ford(G, source)` | Single-source shortest path (Bellman-Ford) |
| Triangles | `networkx.triangles(G)` | Count triangles in graph |

## Quick Start

```bash
# Install dependencies
just install

# Run linters
just lint

# Run benchmarks (default rounds)
just benchmark

# Run benchmarks with 50+ min rounds for better accuracy
just benchmark-long

# Generate scatterplots and CSV
just plot

# Full pipeline
just all
```

## Running Without `just`

If `just` is not available, use `uv run`:

```bash
# Install
uv sync

# Run benchmarks
uv run pytest

# Generate plots
uv run python scripts/plot_results.py

# Full lint
uv run ruff check .
uv run ruff format --check .
uv run mypy .
```

## Project Structure

```
nx_bench/
├── bfs/                  # Matrix Market files for BFS benchmarks
├── sssp/                 # Matrix Market files for SSSP benchmarks
├── triangles/           # Matrix Market files for triangles benchmarks
├── results/              # Benchmark output (JSON, CSV, plots)
├── tests/
│   ├── conftest.py       # Graph loading fixtures
│   ├── test_bfs.py       # BFS benchmarks
│   ├── test_sssp.py      # SSSP benchmarks
│   └── test_triangles.py # Triangles benchmarks
├── scripts/
│   └── plot_results.py   # Plot generation script
├── pyproject.toml        # Project configuration
├── ruff.toml             # Ruff linter rules
├── .pre-commit-config.yaml # Pre-commit hooks
├── justfile              # Build commands
└── README.md
```

## Output

- **JSON**: Auto-saved to `results/Linux-CPython-*-64bit/*.json` (controlled by pytest-benchmark)
- **CSV**: `results/timings.csv` - contains algorithm, graph, nodes, edges, min, max, mean, std, median
- **Plots**: `results/scatter_nodes_mean.png` and `results/scatter_edges_mean.png`

## Commands

| Command | Description |
|---------|-------------|
| `just install` | Install dependencies with uv |
| `just lint` | Run ruff and mypy |
| `just lint-fix` | Auto-fix lint issues |
| `just benchmark` | Run all benchmarks |
| `just benchmark-long` | Run with 50+ min rounds |
| `just plot` | Generate scatterplots and CSV |
| `just test` | Run tests |
| `just clean` | Clean results and cache |
| `just precommit-install` | Install pre-commit hooks |
| `just all` | Run lint + benchmark + plot |

## Adding New Graphs

1. Place `.mtx` Matrix Market files in the appropriate directory:
   - `bfs/` for BFS benchmarks
   - `sssp/` for SSSP benchmarks
   - `triangles/` for triangles benchmarks

2. Each algorithm directory is auto-scanned on test collection

3. Run benchmarks:
   ```bash
   just benchmark
   ```

Example:
```bash
# Add a new graph for BFS
cp /path/to/new_graph.mtx bfs/
just benchmark
```

## Extending with New Algorithms

### Option 1: Add to Existing Test File

Edit `tests/test_<algorithm>.py`:

```python
from __future__ import annotations

import networkx as nx

from tests.conftest import get_<algo>_graphs


def pytest_generate_tests(metafunc):
    if "name" in metafunc.fixturenames and "graph" in metafunc.fixturenames:
        graphs = get_<algo>_graphs()
        metafunc.parametrize("name,graph", graphs)


def test_<algo>(benchmark, name, graph, first_node):
    # Your benchmark code here
    benchmark(lambda: your_function(graph, first_node))
```

### Option 2: Create New Test File

1. Create `tests/test_<newalgo>.py` following the pattern above
2. Add graph fixtures to `tests/conftest.py`:
   ```python
   def get_<newalgo>_graphs():
       graphs = []
       for mtx_path in discover_mtx_files("<newalgo>"):
           try:
               G = load_mtx_graph(mtx_path)
               graphs.append((mtx_path.stem, G))
           except Exception:
               pass
       return graphs
   ```
3. Create `<newalgo>/` directory and add `.mtx` files

### Option 3: Add New Graph Fixtures

To add graph loading for a new source:

1. Add discovery function to `tests/conftest.py`:
   ```python
   def discover_csv_files(directory: str) -> list[Path]:
       # Custom loading logic
       pass

   def get_csv_graphs():
       graphs = []
       for path in discover_csv_files("csv"):
           G = load_csv_graph(path)
           graphs.append((path.stem, G))
       return graphs
   ```
2. Create corresponding directory with graph files

## Configuration

### Benchmark Parameters

Edit `pyproject.toml` `[tool.pytest.ini_options]`:

- `addopts`: Control benchmark behavior (rounds, gc, autosave)
- `testpaths`: Where to find tests

### Linting

- **Ruff**: Rules in `ruff.toml`
- **Mypy**: Configured in `justfile` lint command

### Pre-commit Hooks

Install with:
```bash
just precommit-install
```

Hooks run ruff and mypy on every commit.

## Benchmark Parameters

- **Default**: pytest-benchmark auto-calibrates rounds
- **Long mode**: `--benchmark-min-rounds=50` for more stable results
- **Source node**: First node (node 0)

## Requirements

- Python >= 3.10
- uv (package manager)
- just (task runner)

## Installation Options

### Full Installation (with linting/type tools)

```bash
uv sync
```

### Minimal Installation (benchmarking only)

```bash
uv sync --no-group dev
```

This installs only:
- networkx
- scipy
- matplotlib
- pytest
- pytest-benchmark

## Dependencies

| Package | Purpose | Install Type |
|---------|---------|--------------|
| networkx | Algorithms | runtime |
| scipy | Matrix Market loading | runtime |
| matplotlib | Plotting | runtime |
| pytest | Test runner | runtime |
| pytest-benchmark | Benchmarking | runtime |
| ruff | Linting | dev |
| mypy | Type checking | dev |
| types-networkx | Type stubs | dev |
| scipy-stubs | Type stubs | dev |
| pre-commit | Git hooks | dev |

## Running on Another Machine

### With uv available

```bash
git clone <repo>
uv sync --no-group dev  # minimal - just benchmarks
just benchmark
just plot
```

### With only pip available

```bash
git clone <repo>

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install runtime + benchmark deps
pip install networkx scipy matplotlib pytest pytest-benchmark

# Run benchmarks
pytest

# Generate plots (if matplotlib installed)
python scripts/plot_results.py
```

### Portable requirements file

Generate requirements.txt for machines without uv:

```bash
uv pip freeze > requirements.txt
```

Then on target machine:

```bash
pip install -r requirements.txt
pytest
python scripts/plot_results.py
```
