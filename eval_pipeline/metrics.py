"""Define your evaluation metrics here.

Activate a metric by decorating it. There are two kinds:

    @performance_metric
    def my_metric(retrieved, gold, k):
        # ONE query, ONE run.
        # retrieved : ranked list of `k` restaurant ids, best first
        # gold      : unordered list of relevant restaurant ids (treat as ground truth)
        # k         : cutoff (10)
        return <float>

    @determinism_metric
    def my_check(runs, gold, k):
        # ONE query, ALL runs.
        # runs : list of ranked lists, one per run -> [[...run1...], [...run2...], ...]
        return <float>

The pipeline auto-discovers every decorated function, runs it over all queries
(performance metrics are averaged over runs first), then macro-averages across
queries -- reporting an `overall` value and a `by_category` breakdown in
results.json. Use `name="..."` in the decorator to control the label that appears
there.

The two functions below are PLACEHOLDERS so you can run the pipeline immediately.
Feel free to change or remove them.
"""
from eval_pipeline.registry import performance_metric, determinism_metric


@performance_metric(name="precision@10")
def precision(retrieved, gold, k):
    """Fraction of the top-k retrieved items that are relevant."""
    gold = set(gold)
    return len(set(retrieved[:k]) & gold) / k


@determinism_metric(name="jaccard")
def jaccard(runs, gold, k):
    """Mean pairwise Jaccard overlap of the top-k result sets across runs."""
    sets = [set(r[:k]) for r in runs]
    scores = []
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            union = sets[i] | sets[j]
            scores.append(len(sets[i] & sets[j]) / len(union) if union else 1.0)
    return sum(scores) / len(scores) if scores else 1.0
