# Hybrid retrieval

Pure semantic retrieval misses exact-name lookups. Queries like "What's the capital of Burundi?" return Africa-related context but not the actual Gitega article — embeddings aren't tuned for rare named entities.

## How to diagnose it

Run a long-tail entity-lookup gold set. Observe that top-k semantic results are thematically similar but don't contain the answer.

## The fix

Run BM25 in parallel with dense retrieval; merge with reciprocal rank fusion. Tune `hybrid_alpha` (weight) per query class.

## Success criteria

long-tail-entity gold-set accuracy improves by ≥25pp; no regression on module 1's metric.

## Grading

This module ships 5 probe(s):

- `health` (health)
- `longtail-entity-burundi` (regression)
- `longtail-entity-tucows` (regression)
- `hybrid-alpha-respected` (contract)
- `prose-lookup-no-regression` (regression)

Pass threshold: **70%**

## Submission

Implement the fix. Run `make eval` locally to confirm metrics move. Host your service (ngrok / fly.io / render). Submit the URL on the LMS slide-3 form. The LMS judge probes your endpoint with the tests listed above.

---

_Module 2 of **Production-Scale RAG on Wikipedia** (branch `exercise/02-hybrid-retrieval`). Generated from `course.yaml`'s x-modules entry on `main`. Do not hand-edit — re-run the renderer to regenerate._
