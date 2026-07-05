# AGI Repository

This repository contains a small live-coding interview exercise. 

The app is a mocked RAG pipeline that retrieves policy snippets, builds a prompt,
and asks a slightly random `FakeLLM` to produce an answer with citations.

## Candidate Exercise

Target time: 20-30 minutes with the retrieval-evaluation exercise, or 15-25
minutes if you skip that section.

You can use your usual editor and terminal. Please narrate tradeoffs as you work.

### Setup

```powershell
uv sync
uv run python -m unittest
uv run python -m rag_lab.pipeline "How should we handle authentication for enterprise customers?"
```

This project uses `uv` for setup and command execution.

### Tasks

1. Create a working branch.

2. Make a small prompt change in `rag_lab/prompts.py`.

   Change `ANSWER_STYLE` so answers are `action-oriented`.

3. Merge the interview prompt update branch and resolve the conflict.

   Keep both ideas in the final prompt style: answers should be action-oriented
   and should call out caveats.

4. Find and fix the existing bug.

   `uv run python -m unittest` currently exposes a retrieval bug. Fix the bug without
   changing the test expectation.

5. Do a short code review.

   Open the GitHub pull request from `review/fallback-safety` into `main` and
   write or verbally give 2-3 review comments. Focus on correctness,
   reliability, and product risk.

6. Evaluate synthetic retrieval runs.

   Open `docs/retrieval-evaluation.md`, then implement or extend metrics in
   `eval_pipeline/metrics.py`. The pipeline loads repeated retrieval runs from
   `dataset.json` and writes a summary to `results.json`:

   ```powershell
   uv run python -m eval_pipeline
   ```

   Decide what to measure and explain what the outputs say about the mocked
   retrieval system.

7. Open and discuss the pipeline diagram.

   Open `docs/pipeline.mmd`, explain the current pipeline, and describe one
   extension you would make to improve the pipeline. You do not need to implement the extension.

## What We Evaluate

- Basic git fluency: branching, merging, resolving a simple conflict, committing.
- Debugging: finding a small bug in existing code and fixing it cleanly.
- GenAI/RAG reasoning: interpreting retrieval, prompt construction, citations, and
  confidence in a mocked pipeline.
- Evaluation judgment: choosing useful retrieval metrics and interpreting noisy
  synthetic evaluation results.
- Code review judgment: spotting risks in a small proposed change.
- Communication: explaining decisions while working under light time pressure.
