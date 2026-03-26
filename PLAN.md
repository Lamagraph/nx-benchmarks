# NetworkX Benchmark Project

## Goal
Benchmark BFS, SSSP, and Triangle Counting algorithms in NetworkX using graphs in Matrix Market format.

## Algorithms
- **BFS**: `networkx.bfs_layers(G, source)` - use first node as source
- **SSSP**: `networkx.single_source_dijkstra(G, source)` - use first node as source
- **Triangles**: `networkx.triangles(G)` - count triangles in graph

## Directory Structure
```
nx_bench/
├── bfs/                  # symlink .mtx files for BFS
├── sssp/                 # symlink .mtx files for SSSP
├── triangles/           # symlink .mtx files for triangles
├── results/              # benchmark JSON/CSV + scatterplots
├── tests/
│   ├── conftest.py       # auto-scan fixtures
│   ├── test_bfs.py       # BFS benchmarks
│   ├── test_sssp.py      # SSSP benchmarks
│   └── test_triangles.py # triangles benchmarks
├── scripts/
│   └── plot_results.py   # scatterplots from benchmark JSON
├── pyproject.toml        # uv + pytest-benchmark config
├── ruff.toml             # ruff rules
├── pyrightconfig.json    # pyright strict config
├── .pre-commit-config.yaml # ruff + pyright hooks
├── .gitignore
└── justfile              # build commands
```

## Implementation Steps

### Step 1: Project Setup
- [ ] Create directory structure (`bfs/`, `sssp/`, `triangles/`, `results/`, `tests/`, `scripts/`)
- [ ] Create `pyproject.toml` with uv, pytest-benchmark, networkx, matplotlib dependencies
- [ ] Create `ruff.toml` with linting rules
- [ ] Create `pyrightconfig.json` with strict type checking
- [ ] Create `.gitignore`
- [ ] Create `.pre-commit-config.yaml` for ruff + pyright hooks
- [ ] Create `justfile` with all commands

### Step 2: Benchmark Infrastructure
- [ ] Create `tests/conftest.py` with auto-scan fixtures for each algorithm directory
- [ ] Create `tests/test_bfs.py` with parametrized BFS benchmarks
- [ ] Create `tests/test_sssp.py` with parametrized SSSP benchmarks
- [ ] Create `tests/test_triangles.py` with parametrized triangles benchmarks

### Step 3: Plotting
- [ ] Create `scripts/plot_results.py` to generate scatterplots from benchmark JSON
- [ ] Output CSV with columns: algorithm, graph, nodes, edges, min, max, mean, std, median

### Step 4: Testing
- [ ] Run `just install` to install dependencies
- [ ] Run `just lint` to verify ruff + pyright pass
- [ ] Run `just benchmark` to execute all benchmarks (50 iterations)
- [ ] Run `just plot` to generate scatterplots
- [ ] Verify CSV and plots are created in `results/`

### Step 5: Git Setup
- [ ] Initialize git repository
- [ ] Run `just precommit-install` to set up pre-commit hooks
- [ ] Make initial commit

## Commands

```bash
# Install dependencies
just install

# Run linters
just lint

# Run all benchmarks
just benchmark

# Run specific algorithm benchmarks
just benchmark-bfs
just benchmark-sssp
just benchmark-triangles

# Generate scatterplots
just plot

# Run full pipeline
just all

# Pre-commit setup
just precommit-install
```

## Benchmark Parameters
- **Iterations**: 50 runs per graph
- **Source node**: First node in graph (node 0 or first in sorted order)
- **Output**: JSON from pytest-benchmark, CSV with timing statistics, scatterplots

## Graph Input
Place `.mtx` Matrix Market files in respective directories:
- `bfs/` - graphs for BFS benchmarking
- `sssp/` - graphs for SSSP benchmarking
- `triangles/` - graphs for triangles benchmarking

Symlink or copy graph files to each directory as needed (different algorithms may use different graphs).
