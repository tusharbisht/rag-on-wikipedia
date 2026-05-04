# Query rewriting and decomposition

Multi-hop and complex queries fail. Compound questions retrieve nothing useful because no single chunk contains the full answer.

## How to diagnose it

Inspect failed queries. Notice they contain implicit sub-questions the retriever can't satisfy in one shot.

## The fix

LLM-based query rewriter; query decomposition (split into sub-queries, retrieve per sub-query, merge contexts).

## Success criteria

multi-hop gold-set accuracy improves by ≥30pp.

## Grading

This module ships 2 probe(s):

- `health` (health)
- `multi-hop-jfk-wife-at-assassination` (regression)

Pass threshold: **70%**

## Submission

Implement the fix. Run `make eval` locally to confirm metrics move. Host your service (ngrok / fly.io / render). Submit the URL on the LMS slide-3 form. The LMS judge probes your endpoint with the tests listed above.

---

_Module 3 of **Production-Scale RAG on Wikipedia** (branch `exercise/03-query-decomposition`). Generated from `course.yaml`'s x-modules entry on `main`. Do not hand-edit — re-run the renderer to regenerate._
