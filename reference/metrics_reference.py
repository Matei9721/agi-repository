"""Reference metric implementations -- INTERVIEWER ONLY (answer key).

NOT part of the candidate handout. This is the "coding half" of the rubric and a
verification aid. To check the pipeline end-to-end, copy these into
`eval_pipeline/metrics.py` (replacing the placeholders) and run the pipeline;
the numbers should match `dataset_internal.md`.

All functions match the pipeline's expected signatures:
    performance : fn(retrieved, gold, k) -> float     # one query, one run
    determinism : fn(runs, gold, k) -> float          # one query, all runs
"""
import math

from eval_pipeline.registry import performance_metric, determinism_metric


# --------------------------------------------------------------------------- #
# Performance (quality) metrics
# --------------------------------------------------------------------------- #
@performance_metric(name="precision@10")
def precision_at_k(retrieved, gold, k):
    gold = set(gold)
    return len(set(retrieved[:k]) & gold) / k


@performance_metric(name="recall@10")
def recall_at_k(retrieved, gold, k):
    gold = set(gold)
    if not gold:                      # undefined; dataset guarantees gold >= 1
        return 0.0
    return len(set(retrieved[:k]) & gold) / len(gold)


@performance_metric(name="mrr")
def mrr(retrieved, gold, k):
    gold = set(gold)
    for i, doc in enumerate(retrieved[:k]):
        if doc in gold:
            return 1.0 / (i + 1)
    return 0.0


@performance_metric(name="ndcg@10")
def ndcg_at_k(retrieved, gold, k):
    gold = set(gold)
    rels = [1 if doc in gold else 0 for doc in retrieved[:k]]
    dcg = sum(rel / math.log2(i + 2) for i, rel in enumerate(rels))
    ideal = sorted(rels, reverse=True)
    idcg = sum(rel / math.log2(i + 2) for i, rel in enumerate(ideal))
    return dcg / idcg if idcg > 0 else 0.0


# --------------------------------------------------------------------------- #
# Determinism (cross-run agreement) metrics
# --------------------------------------------------------------------------- #
@determinism_metric(name="jaccard")
def jaccard(runs, gold, k):
    """Mean pairwise Jaccard overlap of the top-k result SETS across runs."""
    sets = [set(r[:k]) for r in runs]
    scores = []
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            union = sets[i] | sets[j]
            scores.append(len(sets[i] & sets[j]) / len(union) if union else 1.0)
    return sum(scores) / len(scores) if scores else 1.0


@determinism_metric(name="recall_std")
def recall_std(runs, gold, k):
    """Std-dev of recall@k across runs -- METRIC-level (not set-level) instability.

    Note it can be ~0 even when jaccard is low: swapping one relevant item for
    another equally-relevant one changes the set but not recall.
    """
    gold_set = set(gold)
    denom = len(gold_set) or 1
    recalls = [len(set(r[:k]) & gold_set) / denom for r in runs]
    mean = sum(recalls) / len(recalls)
    var = sum((x - mean) ** 2 for x in recalls) / len(recalls)
    return math.sqrt(var)
