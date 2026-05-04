# Production-Scale RAG on Wikipedia

Build naive RAG over Wikipedia. Hit production shortcomings module by module. Evolve to a system that handles full-Wikipedia scale with calibrated confidence, verbatim citations, and SLO-grade reliability.

## What this course teaches

By the end you can:

- **Diagnose any RAG failure by inspecting the trace.** Failed query → look at retrieved chunks → classify the failure mode → know which layer to fix.
- **Build every layer of a production RAG pipeline.** Chunking, embedding, BM25, vector index, reranking, prompt construction, citation extraction, eval.
- **Operate a RAG system to SLOs.** Cost, latency, freshness, hallucination rate. Eval gates in CI. No ship without a green eval.
- **Pick the right tool for each layer from experience.** pgvector vs Qdrant vs Vespa, OpenAI embed vs voyage-3 vs nomic, Cohere rerank vs cross-encoder.

These are the most-hireable AI skills in 2026. Every B2B SaaS company is building RAG; almost all of them are doing it badly. After this course you can walk into any of those teams and immediately make their RAG measurably better.

## Quick start

```bash
# 1. Fork (one-time) — your work lives in your fork, not this repo
gh repo fork tusharbisht/rag-on-wikipedia --clone
cd rag-on-wikipedia

# 2. Confirm the naive baseline runs
uv sync
export OPENAI_API_KEY=sk-...           # for embeddings
export ANTHROPIC_API_KEY=sk-ant-...    # for synthesis
make embed-baseline                    # downloads Simple English Wikipedia (~$5 to embed)
make run                               # http://localhost:8000

# 3. Run the gold-set baseline
make eval                              # baseline accuracy ~30-45% — this is the floor

# 4. Pick an exercise — every branch has the same starter + a brief
git checkout exercise/01-structure-aware-chunking
#    EXERCISE.md  — the brief
#    SUBMISSION.md — the API contract (generated; don't edit)
#    grading/<slug>/judge.json — the gold-set probes (generated; don't edit)

# 5. Edit + run + eval
$EDITOR agent.py
make run                               # smoke
make eval                              # check the metric moves

# 6. Host (any of)
#    - ngrok / Cloudflare Tunnel from `make run` locally   (fastest)
#    - render.com / fly.io / railway.app deploy            (production-grade)
#    - your VPS                                            (full control)

# 7. Submit the hosted URL on the LMS slide-3 form for the matching module
```

## Course shape

12 modules, each surfaces ONE class of production failure.

| # | Module | What breaks | What you build |
|---|---|---|---|
| 1 | Structure-aware chunking | Naive paragraph chunking destroys tables, lists, infoboxes | Markup-aware chunker; sliding-window with overlap |
| 2 | Hybrid retrieval | Pure semantic misses exact-name lookups | BM25 + dense + reciprocal rank fusion |
| 3 | Query decomposition | Multi-hop questions retrieve nothing | LLM rewriter + sub-query decomposition |
| 4 | Re-ranking | Top-k high recall, low precision | Cross-encoder rerank on top-50 → top-5 |
| 5 | Citation faithfulness | Model hallucinates from near-miss chunks | Per-claim verbatim contract; calibration; "I don't know" gating |
| 6 | Disambiguation | "Mercury" mixes planet/element/god | NER → Wikidata entity link → resolved-entity priority |
| 7 | Vector index at scale | pgvector chokes at 33M chunks | HNSW + Qdrant; sharded; batched embed pipeline |
| 8 | Freshness | Wikipedia changes; index stale | Recent-changes API → upsert pipeline; freshness SLO |
| 9 | Adversarial robustness | Wikipedia content tries to inject instructions | Sanitisation; instruction isolation; injection detection |
| 10 | Cost SLO | Per-query cost over target | Caching; smaller models; prompt compression |
| 11 | Eval-driven iteration | Can't tell if changes help | Structured eval; A/B; CI regression gate |
| **F** | Production deploy | Hit every SLO simultaneously | Wire it all together |

Every module ships gold-set probes. Each module's grade = improvement on its target metric + no regression on prior modules. **This is the production discipline: every change must improve target metric without regressing others.**

## Wikipedia substrate — Simple English throughout

The course uses **Simple English Wikipedia** (~200k articles, ~1M chunks at the chunking strategy from module 1) for every module. This keeps everything tractable on a laptop and bounds learner cost.

Why Simple English is enough:
- **Scale lessons still work.** At 1M chunks, the naive in-memory search dies; you need real vector indexing. The "scale" module (M7) teaches HNSW + Qdrant on this realistic-but-bounded substrate, not theoretical big-Wiki sizing.
- **Disambiguation, freshness, citation, calibration** — all skills exercise cleanly on the smaller corpus. Simple English has the same content classes (tables, infoboxes, lists, ambiguous entities, contested topics) just with fewer articles.
- **Cost is bounded.** Embedding the full Simple English corpus once: ~$4 with text-embedding-3-small (or free using a local Ollama embedder like nomic-embed-text). Total course cost: ~$5–20 across all modules.
- **Iteration is fast.** A rebuild takes minutes, not hours. Tight feedback loop, more learning per hour.

A pre-embedded Simple English bundle is available as a downloadable asset (~6GB), so learners can skip the embedding step entirely if they want to focus on retrieval/synthesis.

- **Wikidata** as the structured layer for entity resolution in module 6
- **Wikipedia recent-changes API** for freshness in module 8 (filtered to Simple English's article set)

## How grading works

Hosted-URL probe. The LMS judge fires `judge.json` tests at your deployed `/search` endpoint and a few ancillary endpoints (`/health`, `/trace/{id}`, `/eval`, `/feedback`).

Test types:
- `health` — liveness
- `regression` — the gold set; carry-over questions must not regress
- `contract` — endpoint accepts new optional fields per the spec
- `adversarial` — must gracefully handle unanswerable / contested / injected

The killer test: **citation verbatim check.** For every cited quote, the judge fetches the source article and asserts the quote is a literal substring. No LLM-judging needed; deterministic. *Hallucinated citations fail by construction.*

## Authoring contract

This course is authored from a single source of truth: [`course.yaml`](./course.yaml).

- The `x-course` block is course meta
- The `x-modules` block declares 12 modules + their grading tests
- The OpenAPI section declares the API contract every learner implements

Everything else — `SUBMISSION.md`, `grading/<slug>/judge.json`, `grading/<slug>/rubric.md` — is **generated** from `course.yaml`. Don't hand-edit those.

```bash
# Author loop (in this repo)
$EDITOR course.yaml                   # edit the spec
cli validate course.yaml              # structural + drift checks
cli render-judge course.yaml          # write grading/*/judge.json
cli render-docs course.yaml           # write SUBMISSION.md
git add . && git commit && git push
```
