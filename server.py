"""
server.py
=========
Thin FastAPI wrapper around the existing HR Assistant RAG pipeline.
This file does NOT replace or modify any existing backend code.
It simply imports and exposes `run_pipeline()` as an HTTP endpoint.

Start with:
    uvicorn server:app --reload --port 8000

Or:
    python server.py
"""

import os
import uuid
import time
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ── Load environment variables ─────────────────────────────────────────────
load_dotenv()

GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")
GROQ_GUARD_KEY = os.getenv("GROQ_GUARD_KEY", "")

# ── Import existing backend modules ────────────────────────────────────────
# Patch: config.py defines `sensitive_output_patterns` (lowercase) but
# pipeline.py imports `SENSITIVE_OUTPUT_PATTERNS` (uppercase).  Add the alias
# before importing pipeline so the import succeeds.
import src.config as _config_module
if not hasattr(_config_module, "SENSITIVE_OUTPUT_PATTERNS"):
    _config_module.SENSITIVE_OUTPUT_PATTERNS = getattr(
        _config_module, "sensitive_output_patterns", {}
    )

from src.config import GUARD_MODEL_DEFAULT, CHAT_MODEL_DEFAULT
from src.pipeline import run_pipeline
from src.rag import build_vectorstore
from src.hr_docs import HR_POLICIES

# Patch: rag.py references HR_DOCUMENTS — inject it so build_vectorstore works
import src.rag as _rag_module
if not hasattr(_rag_module, "HR_DOCUMENTS"):
    _rag_module.HR_DOCUMENTS = HR_POLICIES


# ── Application state ─────────────────────────────────────────────────────
_vectorstore = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Build the FAISS vectorstore once at startup."""
    global _vectorstore
    print("⏳ Building FAISS vectorstore from HR knowledge base...")
    _vectorstore = build_vectorstore()
    print(f"✅ Vectorstore ready — {len(HR_POLICIES)} policy documents indexed.")
    yield
    print("🛑 Shutting down.")


# ── FastAPI app ────────────────────────────────────────────────────────────
app = FastAPI(
    title="HR Assistant API",
    description="RAG-based HR policy assistant with NeMo guardrails.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow the local frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response models ─────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000,
                         description="The user's HR question.")
    session_id: str | None = Field(None,
                         description="Optional conversation session ID.")


class SourceItem(BaseModel):
    title: str
    content: str
    relevance: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceItem]
    blocked: bool
    block_reason: str | None
    session_id: str
    processing_time_ms: int


class HealthResponse(BaseModel):
    status: str
    vectorstore_ready: bool
    policies_loaded: int


# ── Endpoints ──────────────────────────────────────────────────────────────

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Check API readiness and vectorstore status."""
    return HealthResponse(
        status="online" if _vectorstore else "initializing",
        vectorstore_ready=_vectorstore is not None,
        policies_loaded=len(HR_POLICIES),
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Send a message through the HR Assistant pipeline.
    Returns the answer, retrieved sources, and guardrail status.
    """
    if not _vectorstore:
        raise HTTPException(status_code=503,
                            detail="HR knowledge base is still loading. Please try again in a moment.")

    if not GROQ_API_KEY:
        raise HTTPException(status_code=500,
                            detail="Server configuration error — GROQ API key not set.")

    session_id = req.session_id or str(uuid.uuid4())

    try:
        # Call the existing pipeline (unchanged)
        answer, trace = run_pipeline(
            message=req.message,
            groq_key=GROQ_API_KEY,
            guard_model=GUARD_MODEL_DEFAULT,
            chat_model=CHAT_MODEL_DEFAULT,
            vectorstore=_vectorstore,
        )
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail="An error occurred while processing your request. Please try again.")

    # ── Normalize the response for the frontend ────────────────────────
    # Extract source information from the trace
    sources = []
    retrieval = trace.get("retrieval", {})
    for chunk in retrieval.get("chunks", []):
        sources.append(SourceItem(
            title=chunk.get("source", "HR Policy Document"),
            content=chunk.get("content", "")[:300],   # Truncate for display
            relevance=chunk.get("score", 0.0),
        ))

    # Check if the query was blocked by guardrails
    rail_info = trace.get("rail", {})
    blocked = rail_info.get("blocked", False)
    block_reason = rail_info.get("reason", None)

    # If it was a dialog response (e.g., greeting), it's not blocked
    is_dialog = rail_info.get("dialog", False)

    total_ms = trace.get("total_ms", 0)

    return ChatResponse(
        answer=answer,
        sources=sources,
        blocked=blocked,
        block_reason=block_reason,
        session_id=session_id,
        processing_time_ms=total_ms,
    )


# ── Run directly ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
