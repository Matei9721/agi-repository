# AGI Repository

This repository contains a small live-coding interview exercise. It is intentionally
fake GenAI: there are no model calls, API keys, or external dependencies.

The app is a mocked RAG pipeline that retrieves policy snippets, builds a prompt,
and asks a slightly random `FakeLLM` to produce an answer with citations.

## Candidate Exercise

Target time: 15-25 minutes.

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

   ```powershell
   git checkout -b candidate/<your-name>
   ```

2. Make a small prompt change in `rag_lab/prompts.py`.

   Change `ANSWER_STYLE` so answers are `action-oriented`.

3. Merge the interview prompt update branch and resolve the conflict.

   ```powershell
   git merge interview/prompt-refresh
   ```

   Keep both ideas in the final prompt style: answers should be action-oriented
   and should call out caveats.

4. Find and fix the existing bug.

   `uv run python -m unittest` currently exposes a retrieval bug. Fix the bug without
   changing the test expectation.

5. Do a short code review.

   Open `review/sample_pr.diff` and write or verbally give 2-3 review comments.
   Focus on correctness, reliability, and product risk.

6. Generate and discuss the pipeline diagram.

   ```powershell
   uv run python -m rag_lab.diagram > docs/generated_pipeline.mmd
   ```

   Open `docs/generated_pipeline.mmd`, explain the current pipeline, and describe
   one extension you would make if this were moving toward production.

7. Commit your work.

   ```powershell
   git status
   git add .
   git commit -m "Complete interview exercise"
   ```

## What We Evaluate

- Basic git fluency: branching, merging, resolving a simple conflict, committing.
- Debugging: finding a small bug in existing code and fixing it cleanly.
- Testing discipline: using the existing tests and keeping the behavioral contract.
- GenAI/RAG reasoning: interpreting retrieval, prompt construction, citations, and
  confidence in a mocked pipeline.
- Code review judgment: spotting risks in a small proposed change.
- Communication: explaining decisions while working under light time pressure.
