# Vector index at production scale

Simple English Wikipedia is ~200k articles → ~1M chunks at the chunking strategy you built in module 1. At 1M chunks, the naive in-memory cosine search you've been running falls over: p95 retrieval > 5s, memory exceeds 8GB, every restart re-warms the index from scratch (multi-minute startup). The "throw it in a flat list and search linearly" approach doesn't scale even to Simple English.

## How to diagnose it

Run `make benchmark-retrieval` against the full Simple English embedding bundle. Observe: p95 retrieval > 5s under load, p99 > 30s. Memory profile shows the entire embedding matrix (~6GB at 1536 dims float32) is held in RAM for every replica. Adding a second worker doubles memory cost.

## The fix

Switch to HNSW indexing in a production vector DB (Qdrant or Weaviate, both run as Docker locally for the course). HNSW gives sub-millisecond retrieval at this scale. Run a batched embedding pipeline (concurrent fetch + embed + upsert; resumable on crash) so re-indexing doesn't require holding everything in memory. Persist the index to disk so restarts are fast. Optionally shard by topic cluster if memory pressure persists.

## Success criteria

p95 retrieval < 200ms at 1M-chunk scale; index rebuild from cold finishes in < 10 minutes; restart-warm time < 5 seconds; the deployed service handles 50 RPS sustained without OOM.

## Grading

This module ships 5 probe(s):

- `health-declares-real-index` (contract)
- `latency-slo-p95-under-load` (regression)
- `cold-restart-index-persists` (contract)
- `under-load-no-regression` (regression)
- `prose-no-regression` (regression)

Pass threshold: **70%**

## Submission

Implement the fix. Run `make eval` locally to confirm metrics move. Host your service (ngrok / fly.io / render). Submit the URL on the LMS slide-3 form. The LMS judge probes your endpoint with the tests listed above.

---

_Module 7 of **Production-Scale RAG on Wikipedia** (branch `exercise/07-vector-scale`). Generated from `course.yaml`'s x-modules entry on `main`. Do not hand-edit — re-run the renderer to regenerate._
