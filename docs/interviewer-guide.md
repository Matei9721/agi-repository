# Interviewer Guide

This exercise is designed for a 20-30 minute live session with the retrieval
evaluation exercise, or 15-25 minutes if you skip that section.

## Suggested Flow

1. Ask the candidate to create a branch and run the tests.
2. Ask them to change `ANSWER_STYLE` in `rag_lab/prompts.py`.
3. Ask them to merge `interview/prompt-refresh` and resolve the conflict.
4. Ask them to investigate and fix the failing retrieval test.
5. Ask them to review the GitHub PR from `review/fallback-safety` into `main`.
6. Ask them to open `docs/retrieval-evaluation.md`, decide what to measure,
   and evaluate the synthetic retrieval runs in `dataset.json`.
7. Ask them to open `docs/pipeline.mmd` and explain the pipeline.

Candidate commands should go through `uv`, for example `uv run python -m unittest`.

## Expected Bug Fix

`retrieve_context` currently returns one fewer document than requested:

```python
return ranked[: limit - 1]
```

The expected fix is:

```python
return ranked[:limit]
```

## Expected Conflict Resolution

Final `ANSWER_STYLE` should preserve both requirements:

```python
ANSWER_STYLE = "Use an action-oriented, evidence-first tone and call out caveats."
```

Exact wording does not matter as long as both ideas remain.

## Code Review PR

Create or open a GitHub PR from `review/fallback-safety` into `main`.

Suggested title:

```text
Add fallback handling for pipeline failures
```

If the PR does not already exist, this compare URL should open the PR creation
flow once the branch is pushed:

```text
https://github.com/Matei9721/agi-repository/compare/main...review/fallback-safety?quick_pull=1
```

## Good Code Review Signals

Strong candidates should notice at least two of these in the review PR:

- It can return a hallucinated answer with no citations.
- It swallows all exceptions and hides operational failures.
- The confidence score is hard-coded to `0.99`.
- The fallback path violates the existing evidence-only prompt contract.
- There are no tests for the new fallback behavior.

## Retrieval Evaluation Exercise

The exercise intentionally gives candidates data, not a metric recipe. Avoid
prompting them with metric names at first. Strong candidates should define what
success means for retrieval, account for ranking position, and notice that the
same query has multiple runs.

The data is stored in `dataset.json`. The `eval_pipeline` package loads it,
discovers decorated metrics in `eval_pipeline/metrics.py`, aggregates them with
pandas, and writes `results.json`. Several queries have multiple expected
relevant documents.

Good interpretation signals:

- They use at least one retrieval-quality metric such as precision@k, recall@k,
  MRR, nDCG, or hit rate.
- They use at least one cross-run stability metric such as pairwise Jaccard
  overlap or score variance across the three runs.
- They group results by category instead of relying only on one aggregate.
- They notice the precision/recall tradeoff caused by different gold-set sizes.
- They distinguish stable-but-poor ranking from unstable retrieval.
- They can explain why sklearn is optional here: many ranked-list metrics are
  simple to implement directly.

`reference/metrics_reference.py` is an interviewer-only answer key. The
dataset-specific notes in `dataset_internal.md` call out the planted failure
modes and expected aggregate values.

## Extension Discussion Ideas

- Replace keyword retrieval with embeddings and add evaluation datasets.
- Add citation validation that checks every generated claim against retrieved text.
- Track abstention cases and low-confidence responses.
- Add structured observability for retrieved documents, prompt versions, and latency.
- Introduce tenant-aware document filtering before retrieval.
