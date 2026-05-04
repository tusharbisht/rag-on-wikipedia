"""Naive RAG baseline. Module 0 — what every later module fixes.

Intentional shortcomings (each is the diagnosis for a later exercise):

  - Paragraph chunking destroys tables/lists/infoboxes (fixed in M1)
  - Pure semantic retrieval misses exact-name lookups       (fixed in M2)
  - No query rewriting; multi-hop questions fail            (fixed in M3)
  - No reranking; LLM distracted by near-miss chunks         (fixed in M4)
  - No citation contract; model hallucinates from prior knowledge (fixed in M5)
  - No disambiguation; "Mercury" returns mixed entities      (fixed in M6)
  - pgvector at small scale only; doesn't scale              (fixed in M7)
  - Static index; no freshness                               (fixed in M8)
  - No injection defense                                     (fixed in M9)
  - No caching; cost ungated                                 (fixed in M10)
  - No eval discipline                                       (fixed in M11)

Run:
    export OPENAI_API_KEY=sk-...
    export ANTHROPIC_API_KEY=sk-ant-...
    uv sync
    make embed-baseline    # one-time: build the index
    make run               # http://localhost:8000

The baseline scores ~30-45% on the gold set. That's the floor. Every
module pushes it up.
"""

from __future__ import annotations

import os
import time
import uuid
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# --- placeholders — real implementations live in the modules below ----

class Chunk(BaseModel):
    """One retrievable unit. Naive baseline = one paragraph."""
    id: str
    article: str
    section: str | None = None
    text: str
    char_offset: int = 0


class RetrievedChunk(BaseModel):
    chunk: Chunk
    score: float


# --- request/response — must match course.yaml SearchRequest/Response ---

class SearchRequest(BaseModel):
    """MUST match openapi.components.schemas.SearchRequest exactly.
    Fields outside this set will fail jsonschema validation upstream."""
    question: str = Field(min_length=1)
    user_id: str
    top_k: int = Field(default=5, ge=1, le=50)
    max_tokens: int | None = None


class Citation(BaseModel):
    id: int
    article: str
    section: str | None = None
    quote: str
    char_offset: int = 0


class SearchResponse(BaseModel):
    answer: str
    citations: list[Citation]
    confidence: float = Field(ge=0.0, le=1.0)
    trace_id: str
    tokens_in: int = 0
    tokens_out: int = 0
    cost_usd: float = 0.0
    latency_ms: int = 0


class HealthResponse(BaseModel):
    ok: bool
    build: str
    model: str
    modules_active: list[str]


# --- the (intentionally) naive baseline -------------------------------

# Replace with real index in your fork. Modules 1+ teach you what each
# layer should look like.
INDEX: list[Chunk] = []  # populated by `make embed-baseline`


def naive_retrieve(question: str, top_k: int) -> list[RetrievedChunk]:
    """SHORTCOMING: pure substring match. Replace with embeddings + BM25
    in module 1+."""
    q_lower = question.lower()
    scored = []
    for c in INDEX:
        if q_lower.split()[0] in c.text.lower():  # extremely naive
            scored.append(RetrievedChunk(chunk=c, score=1.0))
    return scored[:top_k]


def naive_synthesise(
    question: str, retrieved: list[RetrievedChunk]
) -> tuple[str, list[Citation], float]:
    """SHORTCOMING: stuffs context into a single Claude call with no
    citation contract. Hallucination expected. Module 5 fixes this."""
    if not retrieved:
        return ("I don't know — no relevant sources found.", [], 0.1)

    # Real impl would call Anthropic here. Stub for the baseline.
    answer_text = (
        f"[NAIVE BASELINE] Found {len(retrieved)} candidate chunks. "
        f"First chunk says: {retrieved[0].chunk.text[:200]}..."
    )
    citations = [
        Citation(
            id=i + 1,
            article=r.chunk.article,
            section=r.chunk.section,
            quote=r.chunk.text[:140],  # NOT verified verbatim — module 5 fixes
            char_offset=r.chunk.char_offset,
        )
        for i, r in enumerate(retrieved[:3])
    ]
    return answer_text, citations, 0.5  # confidence is a guess


# --- HTTP layer -------------------------------------------------------

app = FastAPI(title="RAG-on-Wikipedia (naive baseline)")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        ok=True,
        build=os.environ.get("GIT_SHA", "dev"),
        model=os.environ.get("MODEL", "claude-sonnet-4-5"),
        modules_active=[],  # baseline = none. Each module adds itself here.
    )


@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest) -> SearchResponse:
    t0 = time.monotonic()
    retrieved = naive_retrieve(req.question, req.top_k)
    answer, citations, confidence = naive_synthesise(req.question, retrieved)
    return SearchResponse(
        answer=answer,
        citations=citations,
        confidence=confidence,
        trace_id=f"tr_{uuid.uuid4().hex[:12]}",
        tokens_in=0,
        tokens_out=0,
        cost_usd=0.0,
        latency_ms=int((time.monotonic() - t0) * 1000),
    )


@app.get("/trace/{trace_id}")
def trace(trace_id: str) -> dict[str, Any]:
    """Stub — modules 1+ wire real spans here."""
    raise HTTPException(status_code=404, detail="trace storage not implemented in baseline")


@app.get("/eval")
def eval_endpoint() -> dict[str, Any]:
    """Stub — module 11 wires the real eval framework here."""
    return {
        "accuracy": 0.0,
        "ece": 1.0,
        "p95_latency_ms": 0,
        "cost_per_query_usd": 0.0,
        "n_questions": 0,
    }


class FeedbackRequest(BaseModel):
    trace_id: str
    rating: int = Field(ge=-1, le=1)
    per_citation: list[dict] | None = None
    comment: str | None = None
    missed_source_url: str | None = None


@app.post("/feedback")
def feedback(req: FeedbackRequest) -> dict[str, bool]:
    """Stub — module 5 + onwards wire real feedback storage."""
    return {"ok": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agent:app", host="0.0.0.0", port=8000, reload=True)
