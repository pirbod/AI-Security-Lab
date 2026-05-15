"""Harmless vLLM-shaped mock service for local metadata checks."""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="Mock vLLM", version="0.1.0")


@app.get("/")
def root() -> dict[str, str]:
  """Return a simple marker for browser checks."""
  return {"service": "mock-vllm", "scope": "local-only"}


@app.get("/health")
def health() -> dict[str, str]:
  """Return local health status."""
  return {"status": "ok"}


@app.get("/v1/models")
def models() -> dict[str, object]:
  """Return OpenAI-compatible mock model metadata only."""
  return {
    "object": "list",
    "data": [
      {
        "id": "local-placeholder-model",
        "object": "model",
        "created": 0,
        "owned_by": "local-lab",
      }
    ],
  }
