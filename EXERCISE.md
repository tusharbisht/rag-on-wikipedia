# Cost optimization to SLO

After modules 1-9 the agent works well but is expensive. Per-query cost runs ~$0.02-0.05 (large embed + rerank model + Sonnet synth + long prompts). Production SLO target: < $0.005/query — 4-10× too expensive. At scale, cost determines whether a feature ships.

## How to diagnose it

Inspect /trace cost breakdown per query. You'll see synth dominates (~70% of cost), then embeddings (~15%), then rerank (~15%). Repeated queries hit the synthesizer fresh every time — no caching. Long retrieved-context prompts pay for tokens the model doesn't need.

## The fix

Four layers. (1) Exact-match cache: hash (normalised_question, user_id_role) → response. Repeat queries return in <50ms. (2) Semantic cache: embed the question, find nearest cached question within similarity > 0.95, return cached response if found. (3) Prompt compression: drop chunks below relevance threshold post- rerank; summarize long chunks before sending to synth. (4) Tiered models: Haiku for the planner / classifier; Sonnet for synth only.

## Success criteria

Cost p95 per query drops from baseline ~$0.02 to < $0.005; cache hit rate ≥ 30% on a realistic query distribution; no regression on accuracy (cached responses must be correctness- equivalent to fresh).

## Grading

This module ships 6 probe(s):

- `health` (health)
- `cost-slo-p95` (regression)
- `cache-hit-marked-on-repeat` (contract)
- `cost-breakdown-non-trivial` (contract)
- `semantic-cache-near-match-detected` (contract)
- `prose-no-regression` (regression)

Pass threshold: **70%**

## Submission

Implement the fix. Run `make eval` locally to confirm metrics move. Host your service (ngrok / fly.io / render). Submit the URL on the LMS slide-3 form. The LMS judge probes your endpoint with the tests listed above.

---

_Module 10 of **Production-Scale RAG on Wikipedia** (branch `exercise/10-cost-slo`). Generated from `course.yaml`'s x-modules entry on `main`. Do not hand-edit — re-run the renderer to regenerate._
