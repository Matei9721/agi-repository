# Interviewer Guide

This exercise is designed for a 20-30 minute live session with the notebook, or
15-25 minutes if you skip that section.

## Suggested Flow

1. Ask the candidate to create a branch and run the tests.
2. Ask them to change `ANSWER_STYLE` in `rag_lab/prompts.py`.
3. Ask them to merge `interview/prompt-refresh` and resolve the conflict.
4. Ask them to investigate and fix the failing retrieval test.
5. Ask them to review the GitHub PR from `review/fallback-safety` into `main`.
6. Ask them to open `notebooks/retrieval_evaluation.ipynb`, choose metrics, and
   evaluate the synthetic retrieval runs.
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

## Retrieval Evaluation Notebook

The notebook intentionally asks candidates to choose metrics rather than giving
them a fixed recipe. Good candidates should usually propose at least one
relevance metric and one consistency metric.

Useful relevance metrics:

- Hit rate@k: whether any expected relevant document appears in the top k.
- Recall@k: how much of the expected relevant set appears in the top k.
- Precision@k: how much of the top k is actually relevant.
- MRR: whether the first relevant result appears early.

Useful consistency metrics:

- Exact top-k match rate across the three runs for a query.
- Average pairwise Jaccard overlap across top-k document ids.
- Rank movement for expected relevant documents.

Good interpretation signals:

- `q_privacy_boundary` should look strong and stable.
- `q_billing_invoice` should look like a hard failure because the expected
  billing policy never appears.
- `q_enterprise_rollout` should show some relevance but unstable rankings across
  runs.
- `q_eval_launch` retrieves relevant documents but occasionally pushes one below
  top 2, which is important if the prompt only consumes the first few chunks.

## Extension Discussion Ideas

- Replace keyword retrieval with embeddings and add evaluation datasets.
- Add citation validation that checks every generated claim against retrieved text.
- Track abstention cases and low-confidence responses.
- Add structured observability for retrieved documents, prompt versions, and latency.
- Introduce tenant-aware document filtering before retrieval.
