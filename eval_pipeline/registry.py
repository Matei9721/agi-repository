"""Metric registry + activation decorators.

Two families of metrics, each activated by a decorator:

  @performance_metric   -> quality of a single retrieval (one query, one run)
  @determinism_metric   -> agreement across the repeated runs of a single query

A decorated function is registered under its own name, or under an explicit
``name=`` override (handy for labels that are not valid Python identifiers, e.g.
``name="precision@10"``). That name is exactly how the metric appears in
``results.json``.
"""

PERFORMANCE_METRICS = {}
DETERMINISM_METRICS = {}


def _register(registry, fn, name):
    key = name or fn.__name__
    if key in registry:
        raise ValueError(
            f"A metric named {key!r} is already registered. "
            "Give one of them a different name= to avoid silently overwriting it."
        )
    registry[key] = fn
    return fn


def performance_metric(fn=None, *, name=None):
    """Register a per-(query, run) quality metric: ``fn(retrieved, gold, k) -> float``."""
    def wrap(f):
        return _register(PERFORMANCE_METRICS, f, name)
    return wrap(fn) if callable(fn) else wrap


def determinism_metric(fn=None, *, name=None):
    """Register a cross-run agreement metric: ``fn(runs, gold, k) -> float``."""
    def wrap(f):
        return _register(DETERMINISM_METRICS, f, name)
    return wrap(fn) if callable(fn) else wrap
