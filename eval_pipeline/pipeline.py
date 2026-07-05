"""Evaluation pipeline: load the dataset, run every registered metric, write JSON.

Usage:
    uv run python -m eval_pipeline               # uses ./dataset.json -> ./results.json
    uv run python -m eval_pipeline --dataset X --out Y
"""
import argparse
import json
from pathlib import Path

import pandas as pd

from eval_pipeline.registry import PERFORMANCE_METRICS, DETERMINISM_METRICS
from eval_pipeline import metrics  # noqa: F401  -- imported for its decorator side effects

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATASET = ROOT / "dataset.json"
DEFAULT_OUT = ROOT / "results.json"


def load_dataset(path):
    with open(path) as f:
        return json.load(f)


def compute_rows(dataset):
    """Return (performance_rows, determinism_rows), one dict per (metric, query)."""
    k = dataset["meta"]["k"]
    perf_rows, det_rows = [], []
    for q in dataset["queries"]:
        gold = q["gold"]
        runs = [r["retrieved"] for r in q["runs"]]

        # performance: score each run, then average over runs -> one value per query
        for name, fn in PERFORMANCE_METRICS.items():
            per_run = [fn(retrieved, gold, k) for retrieved in runs]
            perf_rows.append({"metric": name, "category": q["category"],
                              "query_id": q["query_id"], "value": sum(per_run) / len(per_run)})

        # determinism: the metric sees all runs at once -> one value per query
        for name, fn in DETERMINISM_METRICS.items():
            det_rows.append({"metric": name, "category": q["category"],
                             "query_id": q["query_id"], "value": fn(runs, gold, k)})
    return perf_rows, det_rows


def aggregate(rows, ndigits=4):
    """Macro-average each metric: overall (mean over queries) + by_category breakdown."""
    out = {}
    if not rows:
        return out
    df = pd.DataFrame(rows)
    for name, g in df.groupby("metric"):
        by_cat = g.groupby("category")["value"].mean().round(ndigits)
        out[name] = {
            "overall": round(float(g["value"].mean()), ndigits),
            "by_category": {cat: float(v) for cat, v in by_cat.items()},
        }
    return out


def main():
    ap = argparse.ArgumentParser(description="RAG retrieval evaluation pipeline")
    ap.add_argument("--dataset", default=str(DEFAULT_DATASET))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    dataset = load_dataset(args.dataset)
    perf_rows, det_rows = compute_rows(dataset)

    results = {
        "meta": {
            "k": dataset["meta"]["k"],
            "num_queries": len(dataset["queries"]),
            "performance_metrics": sorted(PERFORMANCE_METRICS),
            "determinism_metrics": sorted(DETERMINISM_METRICS),
        },
        "performance": aggregate(perf_rows),
        "determinism": aggregate(det_rows),
    }

    with open(args.out, "w") as f:
        json.dump(results, f, indent=2)

    if not PERFORMANCE_METRICS and not DETERMINISM_METRICS:
        print("No metrics defined yet - add some in eval_pipeline/metrics.py")
    else:
        print(f"Wrote {args.out}  "
              f"({len(PERFORMANCE_METRICS)} performance, {len(DETERMINISM_METRICS)} determinism)")


if __name__ == "__main__":
    main()
