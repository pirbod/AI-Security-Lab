"""Harmless Ollama-shaped mock service for local lab checks."""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="Mock Ollama", version="0.1.0")


@app.get("/")
def root() -> dict[str, str]:
  """Return a simple marker for browser checks."""
  return {"service": "mock-ollama", "scope": "local-only"}


@app.get("/health")
def health() -> dict[str, str]:
  """Return local health status."""
  return {"status": "ok"}


@app.get("/api/version")
def version() -> dict[str, str]:
  """Return a mock version response."""
  return {"version": "0.0.0-local-mock"}


@app.get("/api/tags")
def tags() -> dict[str, list[dict[str, str]]]:
  """Return mock model tags without model files or inference."""
  return {"models": [{"name": "local-placeholder", "modified_at": "1970-01-01T00:00:00Z"}]}
