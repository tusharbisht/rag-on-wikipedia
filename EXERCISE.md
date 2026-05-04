# Index freshness via change stream

Wikipedia changes constantly — ~5 edits/second across all languages. A static dump from 6 months ago returns out-of-date answers for current-events queries: outdated population numbers, dead/replaced public figures, retracted claims. The naive index has no notion of time-of-fetch.

## How to diagnose it

Diff a fresh-fetched article against the indexed version. For 100 sample articles you'll find ~30% have changed materially since index build. Test queries about recent events (last 6 months) and observe answers reference outdated facts.

## The fix

Subscribe to Wikipedia's recent-changes API (Server-Sent Events stream). For each changed article: re-fetch, re-chunk, re-embed the diff, upsert into the vector DB. Track per-article last-update timestamp. Surface a `freshness_lag_seconds` in /eval and gate on a < 1h SLO.

## Success criteria

Recent-events gold-set accuracy improves by ≥30pp; freshness lag p95 < 1h sustained; cache invalidation correctly purges stale responses on source change.

## Grading

This module ships 5 probe(s):

- `health` (health)
- `freshness-lag-slo` (regression)
- `recent-event-knowledge` (regression)
- `cache-invalidation-on-change` (regression)
- `regression-no-old-events-broken` (regression)

Pass threshold: **70%**

## Submission

Implement the fix. Run `make eval` locally to confirm metrics move. Host your service (ngrok / fly.io / render). Submit the URL on the LMS slide-3 form. The LMS judge probes your endpoint with the tests listed above.

---

_Module 8 of **Production-Scale RAG on Wikipedia** (branch `exercise/08-freshness`). Generated from `course.yaml`'s x-modules entry on `main`. Do not hand-edit — re-run the renderer to regenerate._
