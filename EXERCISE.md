# Production deploy at SLO

Bring all modules together; meet every SLO simultaneously

## Success criteria

accuracy ≥ 85%, p95 < 500ms, cost < $0.005/q, hallucination < 2%, freshness lag < 1h

## Grading

This module ships 2 probe(s):

- `health` (health)
- `composite-end-to-end` (regression)

Pass threshold: **70%**

## Submission

Implement the fix. Run `make eval` locally to confirm metrics move. Host your service (ngrok / fly.io / render). Submit the URL on the LMS slide-3 form. The LMS judge probes your endpoint with the tests listed above.

---

_Module 12 of **Production-Scale RAG on Wikipedia** (branch `final/integrated`). Generated from `course.yaml`'s x-modules entry on `main`. Do not hand-edit — re-run the renderer to regenerate._
