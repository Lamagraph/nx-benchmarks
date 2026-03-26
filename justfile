default:
    @just --list

install:
    uv sync

lint:
    uv run ruff check .
    uv run ruff format --check .
    uv run pyright .

lint-fix:
    uv run ruff check . --fix
    uv run ruff format .

benchmark:
    uv run pytest --benchmark-json=results/benchmark.json

benchmark-long:
    uv run pytest --benchmark-json=results/benchmark.json --benchmark-min-rounds=50

benchmark-bfs:
    uv run pytest tests/test_bfs.py --benchmark-json=results/bfs.json

benchmark-sssp:
    uv run pytest tests/test_sssp.py --benchmark-json=results/sssp.json

benchmark-triangles:
    uv run pytest tests/test_triangles.py --benchmark-json=results/triangles.json

plot:
    uv run python scripts/plot_results.py

all: lint benchmark plot

precommit-install:
    uv pip install pre-commit
    uv run pre-commit install

test:
    uv run pytest tests/

clean:
    rm -rf results/*.json results/*.csv results/*.png
    rm -rf .pytest_cache __pycache__ tests/__pycache__ scripts/__pycache__
    rm -rf .ruff_cache .mypy_cache
