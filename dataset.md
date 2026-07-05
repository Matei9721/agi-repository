# `dataset.json` — Data Dictionary

A synthetic dataset of retrieval "runs" from a RAG pipeline over a restaurant-search
corpus. Each natural-language query was answered by a retriever that returned a **ranked
list of 10 restaurant IDs**, repeated over **3 runs**. Each query also has a **gold set**
of genuinely relevant restaurants.

> Treat `gold` as **ground truth** — don't second-guess whether a restaurant "really"
> matches. Your job is to measure and interpret, not to relabel.

## Schema

Single JSON file with three top-level keys.

```jsonc
{
  "meta": {
    "k": 10,                 // fixed retrieval cutoff — every list has exactly 10 ids
    "runs_per_query": 3,     // each query was run 3 times
    "num_queries": 40,
    "num_restaurants": 80,
    "note": "retrieved lists are ranked (best first); gold is an unordered set"
  },
  "restaurants": [           // the corpus (80 items)
    { "id": "R001", "name": "Luigi's Trattoria", "cuisine": "Italian",
      "neighborhood": "Old Town", "price": "$$", "tags": ["romantic","wine_list"] }
  ],
  "queries": [               // 40 items
    { "query_id": "Q01",
      "query": "cozy italian near old town",
      "category": "Italian",           // grouping label
      "gold": ["R001","R012", "..."],  // UNORDERED set of relevant ids
      "runs": [
        { "run": 1, "retrieved": ["R001","R044", "... 10 ranked ids"] },
        { "run": 2, "retrieved": ["... 10 ranked ids"] },
        { "run": 3, "retrieved": ["... 10 ranked ids"] }
      ] }
  ]
}
```

### Fields

**`restaurants[]`** — the corpus:
| field | type | notes |
|---|---|---|
| `id` | string | primary key, e.g. `R001`; referenced by `gold` and `retrieved` |
| `name` | string | display name |
| `cuisine` | string | one of Italian, Mexican, Japanese, Vegan, Cafe, Bar, American, Thai, Indian |
| `neighborhood` | string | location label |
| `price` | string | `$`, `$$`, or `$$$` |
| `tags` | string[] | free-text attributes, e.g. `outdoor_seating`, `kid_friendly`, `late_night`, `romantic`, `good_for_groups`, `budget`, `upscale` |

**`queries[]`**:
| field | type | notes |
|---|---|---|
| `query_id` | string | e.g. `Q01` |
| `query` | string | the natural-language search |
| `category` | string | grouping label (8 categories) — handy for slicing results |
| `gold` | string[] | **unordered** set of relevant restaurant IDs; size varies per query; always ≥ 1 |
| `runs` | object[] | exactly 3 runs |

**`queries[].runs[]`**:
| field | type | notes |
|---|---|---|
| `run` | int | 1, 2, or 3 |
| `retrieved` | string[] | **ranked** list (index 0 = top result) of exactly 10 distinct restaurant IDs |

## Invariants

- 80 restaurants; 40 queries; every query has exactly 3 runs.
- Every `retrieved` list contains exactly 10 **distinct** IDs, all present in `restaurants`.
- Every `gold` set is non-empty; all gold IDs exist in `restaurants`.
- `retrieved` is **ranked** (index 0 = top). `gold` is an **unordered set** — order is not meaningful.

## Shape of the data

- **Fixed cutoff:** every retrieval returns exactly 10 results (`k = 10`).
- **Gold-set sizes vary widely** across queries (from ~2 to ~20), because the queries span
  different intents — from narrow, specific lookups to broad attribute searches.
- **Repeated runs:** the same query was executed 3 times; the results may or may not be
  identical across runs.
- Fully synthetic; generated with a fixed seed for reproducibility.
