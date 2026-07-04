# Interviewer Guide

This exercise is designed for a 15-25 minute live session.

## Suggested Flow

1. Ask the candidate to create a branch and run the tests.
2. Ask them to change `ANSWER_STYLE` in `rag_lab/prompts.py`.
3. Ask them to merge `interview/prompt-refresh` and resolve the conflict.
4. Ask them to investigate and fix the failing retrieval test.
5. Ask them to review `review/sample_pr.diff`.
6. Ask them to generate `docs/generated_pipeline.mmd` and explain the pipeline.

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

## Good Code Review Signals

Strong candidates should notice at least two of these in `review/sample_pr.diff`:

- It can return a hallucinated answer with no citations.
- It swallows all exceptions and hides operational failures.
- The confidence score is hard-coded to `0.99`.
- The fallback path violates the existing evidence-only prompt contract.
- There are no tests for the new fallback behavior.

## Extension Discussion Ideas

- Replace keyword retrieval with embeddings and add evaluation datasets.
- Add citation validation that checks every generated claim against retrieved text.
- Track abstention cases and low-confidence responses.
- Add structured observability for retrieved documents, prompt versions, and latency.
- Introduce tenant-aware document filtering before retrieval.
