# Disambiguation and entity resolution

Ambiguous entity names retrieve mixed content. "Mercury" returns the planet, the element, the Roman god, the band, and Freddie Mercury all in one top-k. Equally bad: alias drift — "JFK" and "John F. Kennedy" and "John Fitzgerald Kennedy" embed as if they were different entities. Result: contextually wrong chunks reach the synthesizer.

## How to diagnose it

Run an ambiguous-entity gold set. Inspect retrieved top-k for any "Mercury" query: you'll see a mix of entity classes. For aliases, compare retrieval quality on "JFK biography" vs "John F. Kennedy biography" — they should converge but don't.

## The fix

Run NER on the query; link extracted entities to Wikidata QIDs; prioritise chunks whose source article is the resolved entity. Boost score for chunks tagged with the same QID as the query's head entity. For genuinely ambiguous queries (no entity context), return a clarifying-questions response rather than guessing.

## Success criteria

Ambiguous-entity gold-set accuracy improves by ≥40pp; alias-query recall improves by ≥30pp; no regression on prior modules.

## Grading

This module ships 7 probe(s):

- `health` (health)
- `disambiguation-mercury-planet` (regression)
- `disambiguation-mercury-element` (regression)
- `alias-resolution-jfk` (regression)
- `alias-resolution-full-name` (regression)
- `clarifying-on-ambiguous` (adversarial)
- `prose-no-regression` (regression)

Pass threshold: **70%**

## Submission

Implement the fix. Run `make eval` locally to confirm metrics move. Host your service (ngrok / fly.io / render). Submit the URL on the LMS slide-3 form. The LMS judge probes your endpoint with the tests listed above.

---

_Module 6 of **Production-Scale RAG on Wikipedia** (branch `exercise/06-disambiguation`). Generated from `course.yaml`'s x-modules entry on `main`. Do not hand-edit — re-run the renderer to regenerate._
