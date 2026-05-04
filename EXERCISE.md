# Citation faithfulness and confidence calibration

Even with good retrieval, the model fills gaps with prior knowledge instead of marking uncertainty. Citations exist but don't actually support their claims.

## The fix

Per-claim verbatim citation contract; confidence calibration; "I don't know" gating when sources are insufficient.

## Success criteria

Hallucination rate drops below 2%; calibration ECE < 0.05 on a 50-Q calibration eval set.

## Grading

This module ships 3 probe(s):

- `health` (health)
- `unanswerable-gating` (adversarial)
- `citation-supports-claim` (regression)

Pass threshold: **70%**

## Submission

Implement the fix. Run `make eval` locally to confirm metrics move. Host your service (ngrok / fly.io / render). Submit the URL on the LMS slide-3 form. The LMS judge probes your endpoint with the tests listed above.

---

_Module 5 of **Production-Scale RAG on Wikipedia** (branch `exercise/05-citation-faithfulness`). Generated from `course.yaml`'s x-modules entry on `main`. Do not hand-edit — re-run the renderer to regenerate._
