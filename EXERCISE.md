# Structure-aware chunking

The naive baseline chunks by paragraph, destroying tables, infoboxes, lists, and section context. Failed queries on factual lookups in tabular content reveal retrieved chunks with mid-row breaks.

## How to diagnose it

Inspect /trace for failed queries. Find chunks with broken structure. Audit Wikipedia markup parser output.

## The fix

Parse Wikipedia markup; treat tables, infoboxes, lists, and headed sections as atomic units. Sliding-window with overlap for prose.

## Success criteria

factual-table-lookup gold-set accuracy improves by ≥15pp; no regression on prose-lookup queries.

## Grading

This module ships 4 probe(s):

- `health` (health)
- `factual-table-lookup-state-capital` (regression)
- `factual-table-lookup-population` (regression)
- `prose-lookup-no-regression` (regression)

Pass threshold: **70%**

## Submission

Implement the fix. Run `make eval` locally to confirm metrics move. Host your service (ngrok / fly.io / render). Submit the URL on the LMS slide-3 form. The LMS judge probes your endpoint with the tests listed above.

---

_Module 1 of **Production-Scale RAG on Wikipedia** (branch `exercise/01-structure-aware-chunking`). Generated from `course.yaml`'s x-modules entry on `main`. Do not hand-edit — re-run the renderer to regenerate._
