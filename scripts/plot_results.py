from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt


def load_benchmark_json(filepath: Path) -> dict:
    with filepath.open() as f:
        return json.load(f)


def extract_benchmark_data(bench_json: dict) -> list[dict]:
    results = []
    benchmarks = bench_json.get("benchmarks", [])
    for bench in benchmarks:
        name = bench["name"]
        stats = bench["stats"]
        extra = bench.get("extra_info", {})
        results.append(
            {
                "test": name,
                "graph_name": extra.get("graph_name", name.split("[")[0].strip()),
                "nodes": extra.get("nodes", 0),
                "edges": extra.get("edges", 0),
                "min": stats.get("min", 0),
                "max": stats.get("max", 0),
                "mean": stats.get("mean", 0),
                "std": stats.get("stddev", 0),
                "median": stats.get("median", 0),
            }
        )
    return results


def get_algorithm_from_testname(test_name: str) -> str:
    if "bfs" in test_name.lower():
        return "bfs"
    if "bellman_ford" in test_name.lower():
        return "sssp"
    if "tc" in test_name.lower():
        return "tc"
    return "unknown"


def plot_scatter(
    data: list[dict],
    output_dir: Path,
    x_metric: str = "nodes",
    y_metric: str = "mean",
    yerr_metric: str = "std",
) -> None:
    algorithms = sorted({get_algorithm_from_testname(d["test"]) for d in data})
    graphs = sorted({d["graph_name"] for d in data})

    algo_colors = {"bfs": "blue", "sssp": "green", "tc": "orange", "unknown": "gray"}
    graph_markers = {g: i for i, g in enumerate(graphs)}
    markers = ["o", "s", "^", "D", "v", "<", ">", "p", "h", "*"]

    fig, ax = plt.subplots(figsize=(12, 8))

    for algo in algorithms:
        algo_data = [d for d in data if get_algorithm_from_testname(d["test"]) == algo]
        if not algo_data:
            continue

        for graph in graphs:
            graph_data = [d for d in algo_data if d["graph_name"] == graph]
            if not graph_data:
                continue

            x_values = [d[x_metric] for d in graph_data]
            y_values = [d[y_metric] * 1000 for d in graph_data]
            yerr = [d.get(yerr_metric, 0) * 1000 for d in graph_data]

            color = algo_colors.get(algo, "gray")
            marker = markers[graph_markers[graph] % len(markers)]
            label = f"{algo.upper()} - {graph}"

            ax.errorbar(
                x_values,
                y_values,
                yerr=yerr,
                fmt=marker,
                label=label,
                color=color,
                markeredgecolor=color,
                markerfacecolor="white",
                capsize=3,
                alpha=0.8,
                markersize=8,
            )

    ax.set_xlabel(x_metric.capitalize())
    ax.set_ylabel("Time (ms)")
    ax.set_title(f"Benchmark Results: {y_metric.capitalize()} Time vs {x_metric.capitalize()}")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
    ax.grid(True, alpha=0.3)

    output_path = output_dir / f"scatter_{x_metric}_{y_metric}.png"
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved plot: {output_path}")


def generate_csv(data: list[dict], output_dir: Path) -> None:
    csv_path = output_dir / "timings.csv"
    fieldnames = ["algorithm", "graph", "nodes", "edges", "min", "max", "mean", "std", "median"]

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(
                {
                    "algorithm": get_algorithm_from_testname(row["test"]),
                    "graph": row["graph_name"],
                    "nodes": row["nodes"],
                    "edges": row["edges"],
                    "min": row["min"],
                    "max": row["max"],
                    "mean": row["mean"],
                    "std": row["std"],
                    "median": row["median"],
                }
            )
    print(f"Saved CSV: {csv_path}")


def main() -> None:
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    json_files = sorted(
        results_dir.glob("**/*.json"), key=lambda p: p.stat().st_mtime, reverse=True
    )

    if not json_files:
        print("No benchmark data found. Run benchmarks first with:")
        print("  just benchmark")
        return

    latest_json = json_files[0]
    print(f"Loading benchmark data from: {latest_json.name}")

    bench_json = load_benchmark_json(latest_json)
    all_data = extract_benchmark_data(bench_json)

    if not all_data:
        print("No benchmark data found. Run benchmarks first with:")
        print("  just benchmark")
        return

    generate_csv(all_data, results_dir)

    plot_scatter(all_data, results_dir, x_metric="nodes")
    plot_scatter(all_data, results_dir, x_metric="edges")

    print(f"\nProcessed {len(all_data)} benchmark results")


if __name__ == "__main__":
    main()
