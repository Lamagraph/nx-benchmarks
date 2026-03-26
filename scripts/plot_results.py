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
    if "dijkstra" in test_name.lower():
        return "sssp"
    if "triangles" in test_name.lower():
        return "triangles"
    return "unknown"


def plot_scatter(
    data: list[dict],
    output_dir: Path,
    x_metric: str = "nodes",
    y_metric: str = "mean",
    yerr_metric: str = "std",
) -> None:
    algorithms = {d["test"].split("[")[0].strip() for d in data}
    colors = {"bfs": "blue", "sssp": "green", "triangles": "orange"}

    fig, ax = plt.subplots(figsize=(10, 6))

    for algo in algorithms:
        algo_data = [d for d in data if algo in d["test"].lower()]
        if not algo_data:
            continue

        x_values = [d[x_metric] for d in algo_data]
        y_values = [d[y_metric] * 1000 for d in algo_data]  # Convert to ms
        yerr = [d.get(yerr_metric, 0) * 1000 for d in algo_data]

        color = colors.get(algo, "gray")
        label = algo.upper() if algo != "dijkstra" else "SSSP"
        ax.errorbar(
            x_values,
            y_values,
            yerr=yerr,
            fmt="o",
            label=label,
            color=color,
            capsize=3,
            alpha=0.7,
        )

    ax.set_xlabel(x_metric.capitalize())
    ax.set_ylabel("Time (ms)")
    ax.set_title(f"Benchmark Results: {y_metric.capitalize()} Time vs {x_metric.capitalize()}")
    ax.legend()
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

    json_files = list(results_dir.glob("benchmark*.json"))

    all_data: list[dict] = []
    for json_file in json_files:
        bench_json = load_benchmark_json(json_file)
        all_data.extend(extract_benchmark_data(bench_json))

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
