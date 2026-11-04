---
name: repo_navigation
description: Progressive narrowing for navigating unfamiliar software repositories with semantic search and code graphs.
---
# Repository navigation

1. Start from the issue's nouns, verbs, exception text, API names, and expected behavior.
2. Search exact strings and identifiers before broad semantic queries.
3. Use `search_similar_code` to find semantically related symbols, not as proof that a symbol is faulty.
4. Expand only high-confidence candidates with `get_code_neighbors`.
5. Use `get_code_subgraph` for a small set of candidate symbols; large subgraphs create noise.
6. Read candidate implementations and their tests before proposing a change.
7. Trace both directions: callers explain how inputs arrive; callees explain downstream effects.
8. Stop expanding when two independent evidence sources converge on the same behavior and source location.

## Evidence ranking
- Strong: failing test, exact exception path, or directly observed incorrect behavior.
- Medium: caller/callee relationship plus matching semantics.
- Weak: filename/name similarity alone.

Never edit code during navigation.
