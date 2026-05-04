# Eval-driven iteration

After 10 modules the agent has 10 moving parts. Each tweak — a new chunker, a different reranker, a tighter cost cap — could improve target metric and silently regress others. Without a real eval framework the team flies blind: changes ship on vibes, regressions accrue, you wake up at 60% accuracy and don't know which change caused it.

## How to diagnose it

Try a deliberate regression: revert module 4's reranker. Run whatever eval you have. Does it catch the regression? Most agents at this point have ad-hoc test scripts that only exercise the happy path — silent regressions on adversarial / long-tail coverage are invisible.

## The fix

(1) Authoritative gold set: 200+ questions across difficulty tiers (factual / multi-hop / contested / unanswerable / adversarial), labelled with expected entities. (2) Structured eval pipeline: runs the gold set, slices results by tier + by query class, emits accuracy + ECE + p95 latency + cost as structured output. (3) Coverage check: every rubric criterion has ≥1 question; every failure mode found in production becomes a permanent eval question. (4) CI regression gate: every commit re-runs the eval; PR fails if any sliced metric drops > 2pp without explicit override. (5) A/B framework: ship two prompt/retrieval variants, compare on a held-out 50-Q set; pick winner.

## Success criteria

Eval-set coverage ≥ 95% of rubric criteria; sliced reporting per difficulty tier; regression gate provably catches a planted regression; A/B framework demonstrates a measured improvement between two synthesizer prompts.

## Grading

This module ships 6 probe(s):

- `health` (health)
- `eval-endpoint-shape` (contract)
- `eval-coverage-rubric-criteria` (contract)
- `regression-gate-catches-planted-regression` (contract)
- `a-b-framework-present` (contract)
- `cumulative-end-to-end` (regression)

Pass threshold: **70%**

## Submission

Implement the fix. Run `make eval` locally to confirm metrics move. Host your service (ngrok / fly.io / render). Submit the URL on the LMS slide-3 form. The LMS judge probes your endpoint with the tests listed above.

---

_Module 11 of **Production-Scale RAG on Wikipedia** (branch `exercise/11-eval-driven`). Generated from `course.yaml`'s x-modules entry on `main`. Do not hand-edit — re-run the renderer to regenerate._
