# RAG Retrieval Evaluation — Assignment

You are given a dataset of **runs** from a retrieval pipeline over a restaurant-search
corpus. For each natural-language query, a retriever returned a **ranked list of 10
restaurant IDs**, repeated over **3 runs**. Each query also has a **gold set** of relevant
restaurants (treat it as ground truth).

Your task:

1. **Implement a few evaluation metrics** in `eval_pipeline/metrics.py`.
2. **Run the pipeline** to produce `results.json`.
3. **Discuss the results** — what do the numbers tell you about this retriever?

See `dataset.md` for the full data dictionary.

## Setup

Requires [uv](https://docs.astral.sh/uv/). No manual venv needed — uv handles it.

```bash
uv run python -m eval_pipeline
```

This loads `dataset.json`, runs every metric you've defined, and writes `results.json`.
(Optional: `--dataset <path>` / `--out <path>`.)

## Writing metrics

Open `eval_pipeline/metrics.py` and decorate a function. Two kinds:

```python
from eval_pipeline.registry import performance_metric, determinism_metric

@performance_metric(name="precision@10")
def precision(retrieved, gold, k):
    # ONE query, ONE run.
    #   retrieved : ranked list of k ids (best first)
    #   gold      : unordered list of relevant ids
    #   k         : cutoff (10)
    return len(set(retrieved[:k]) & set(gold)) / k

@determinism_metric(name="jaccard")
def jaccard(runs, gold, k):
    # ONE query, ALL runs.  runs = [[...run1...], [...run2...], [...run3...]]
    ...
```

- **Performance metrics** measure the quality of a single retrieval `(retrieved, gold, k)`.
  The pipeline averages them over the 3 runs, then macro-averages over queries.
- **Determinism metrics** measure agreement across a query's runs `(runs, gold, k)`.
- The `name=` argument sets the label in `results.json`; omit it to use the function name.
- You may use `numpy`, `pandas`, and `scikit-learn` (all installed) — or plain Python.

`metrics.py` ships with a placeholder `precision@10` and `jaccard` so the pipeline runs
out of the box. Replace or extend them.

## Output

`results.json` reports, for each metric, an `overall` macro value and a `by_category`
breakdown:

```json
{
  "performance": {
    "precision@10": { "overall": 0.48, "by_category": { "Italian": 0.58, "...": 0.0 } }
  },
  "determinism": {
    "jaccard": { "overall": 0.79, "by_category": { "Vegan": 0.24, "...": 0.0 } }
  }
}
```
