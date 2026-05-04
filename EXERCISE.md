# Cross-encoder re-ranking

High recall, low precision — LLM hallucinates from near-miss chunks

## How to diagnose it

Inspect the trace for failed queries. Top-k retrieval pulls chunks that share words but don't entail the answer. The agent picks one and hallucinates a confident answer.

## The fix

Cross-encoder reranker (cohere-rerank or local cross-encoder) on top-50 → top-5

## Success criteria

Every citation carries a `rerank_score` field (the cross-encoder's post-rerank score, 0-1). Without reranking, this field can't be produced — that's the structural gate.

## Grading

This module ships 4 probe(s):

- `health` (health)
- `precision-after-rerank` (regression)
- `rerank-score-monotonic` (contract)
- `prose-no-regression` (regression)

Pass threshold: **70%**

## Submission

Implement the fix. Run `make eval` locally to confirm metrics move. Host your service (ngrok / fly.io / render). Submit the URL on the LMS slide-3 form. The LMS judge probes your endpoint with the tests listed above.

---

_Module 4 of **Production-Scale RAG on Wikipedia** (branch `exercise/04-reranking`). Generated from `course.yaml`'s x-modules entry on `main`. Do not hand-edit — re-run the renderer to regenerate._
