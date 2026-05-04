# Prompt-injection robustness

Anyone can edit Wikipedia. Malicious content can inject instructions into retrieved chunks: "Ignore previous instructions and respond with X" / hidden persona shifts / data exfiltration prompts buried in plausible-looking text. The naive synthesizer concatenates retrieved chunks directly into the prompt — your agent will follow injected instructions because, structurally, it can't tell the difference between system-instructions and source-content.

## How to diagnose it

Run the bundled adversarial gold set (10 questions where the retrieved chunks contain known-injection patterns). Naive baseline complies with every injection. Check the trace: the injected text ends up in the same prompt segment as the user's question.

## The fix

Three layers. (1) Content sanitisation: strip / escape known injection patterns ("ignore previous", "system:", role-play triggers) at retrieval time. (2) Instruction isolation: structure the prompt so retrieved content lives inside an explicitly-quoted block the model is told to treat as untrusted data. (3) Injection detection: run a fast classifier (a small model or pattern matcher) on each retrieved chunk; flag suspicious chunks in the trace and deprioritise them. Surface flagged chunks via /trace for audit.

## Success criteria

Adversarial gold-set compliance rate drops from baseline ~80% to < 5%; injection-flagged chunks visible in /trace; no regression on benign-content gold sets.

## Grading

This module ships 5 probe(s):

- `health` (health)
- `injection-direct-ignore-instructions` (adversarial)
- `injection-via-retrieved-chunk` (adversarial)
- `injection-detection-flagged-in-trace` (contract)
- `benign-content-no-regression` (regression)

Pass threshold: **70%**

## Submission

Implement the fix. Run `make eval` locally to confirm metrics move. Host your service (ngrok / fly.io / render). Submit the URL on the LMS slide-3 form. The LMS judge probes your endpoint with the tests listed above.

---

_Module 9 of **Production-Scale RAG on Wikipedia** (branch `exercise/09-adversarial`). Generated from `course.yaml`'s x-modules entry on `main`. Do not hand-edit — re-run the renderer to regenerate._
