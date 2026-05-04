# Exercise 1 — Structure-aware chunking

> **The naive baseline (on `main`) chunks Wikipedia by paragraph. This destroys tables, infoboxes, lists, and cross-section context. Your job: replace the chunker so structural units stay atomic.**

## Why this matters

The naive baseline's `naive_retrieve()` operates on paragraph chunks. That's fine for prose — "Hamlet was written by Shakespeare in 1601" is a single paragraph and survives chunking intact. It falls apart for **structured content**:

- **Tables**: `| Capital | Cheyenne | ... |` row-1 lands in chunk A, row-2 in chunk B. The query "What's the capital of Wyoming?" retrieves chunk B (which says "Cheyenne") with no context — the LLM doesn't know it's a state capital.
- **Infoboxes**: the right-hand summary boxes on Wikipedia articles are key-value dense. Naive chunking treats them as ordinary prose and loses the structure.
- **Lists**: ordered/unordered lists get split mid-item. Population rankings, election results, drug interactions — all destroyed.
- **Section context**: a chunk in the middle of "==Geography==" doesn't know it's about geography. Cross-section retrieval becomes random.

Run `make eval` against the baseline. You'll see ~30-45% accuracy on the gold set. **Most failures are structural.** Look at the trace for any failed query — you'll see the retrieved chunks have broken structure.

## Your task

Rewrite the chunking pipeline so:

1. **Tables stay atomic.** Each table is one chunk, with a header row preserved as context.
2. **Infoboxes stay atomic.** Same rule — one chunk per infobox, all key-value pairs together.
3. **Lists stay atomic.** Each list (`<ul>` / `<ol>`) is one chunk, with its lead-in sentence.
4. **Prose uses sliding-window with overlap.** 512 tokens per chunk, 64-token overlap, so a fact split across paragraphs lands in at least one chunk.
5. **Each chunk carries its section path.** "United States > Wyoming > Geography > Cities" — embed this in the chunk's metadata so the retriever can use it.

You'll need to parse the Wikipedia markup. The dataset bundles MediaWiki XML; use `mwparserfromhell` or hand-roll a parser for the subset of markup you need. The starter has a `kb_loader.py` module to extend.

## How you'll know you got it right

Run `make eval` after your changes. The gold set's `factual-table-lookup-*` and `factual-list-lookup-*` questions should improve by ≥15pp. The `prose-lookup-no-regression` questions should stay at baseline-or-better. **Both conditions must hold** — improving table lookups at the cost of regressing prose is not a pass.

You can also inspect specific traces via `GET /trace/{trace_id}`. After your fix, retrieved chunks for a "What's the capital of Wyoming?" query should contain the full state-summary infobox or the relevant table row with header context — not a half-row mid-table.

## Submission

```bash
make run                          # smoke
make eval                         # confirm metric movement
# Host (ngrok / fly / render)
# Submit the hosted URL on the LMS slide-3 form
```

The LMS judge probes your endpoint with the gold set declared in [`grading/exercise-01-structure-aware-chunking/judge.json`](grading/exercise-01-structure-aware-chunking/judge.json) — that file is **generated** from `course.yaml` and represents the binding contract. Don't hand-edit it; if the test set needs to change, edit `course.yaml` upstream.

## Pass criteria

- All `health` tests return 200 with the right shape
- All `factual-table-lookup` tests return the expected entity in `body_contains`
- `citation_verbatim: true` is enforced — every cited quote MUST be a literal substring of the source article
- `prose-lookup-no-regression` tests still pass
- Aggregate weighted score ≥ `pass_threshold_pct` (70 by default)

## Non-goals for this module

- Don't add hybrid retrieval yet — module 2 covers that
- Don't add reranking yet — module 4
- Don't add disambiguation yet — module 6
- The eval/CI infrastructure is separate from the chunker; you only need to touch chunking + the loader
