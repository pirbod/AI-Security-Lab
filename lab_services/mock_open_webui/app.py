"""Harmless Open WebUI-shaped mock service for local UI checks."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Mock Open WebUI", version="0.1.0")


@app.get("/", response_class=HTMLResponse)
def root() -> str:
  """Return a small local-only UI marker page."""
  return """
  <!doctype html>
  <html lang="en">
    <head><title>Mock Open WebUI</title></head>
    <body>
      <h1>Mock Open WebUI</h1>
      <p>Local-only mock service for defensive lab checks.</p>
    </body>
  </html>
  """


@app.get("/health")
def health() -> dict[str, str]:
  """Return local health status."""
  return {"status": "ok"}
