"""Safe local Ollama exposure checks."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.config import HTTP_TIMEOUT_SECONDS
from app.models import Finding
from scanners.safety import ensure_safe_target


def _safe_json_get(url: str, timeout: float) -> tuple[int, dict[str, object] | None, str]:
  """Fetch a metadata endpoint without sending prompts or changing server state."""
  request = Request(url, method="GET")
  try:
    with urlopen(request, timeout=timeout) as response:
      body = response.read(8192).decode("utf-8", errors="replace")
      try:
        return response.status, json.loads(body or "{}"), body[:500]
      except json.JSONDecodeError:
        return response.status, None, body[:500]
  except HTTPError as exc:
    return exc.code, None, str(exc)
  except URLError as exc:
    return 0, None, str(exc.reason)
  except TimeoutError:
    return 0, None, "request timed out"


def run_check(
  host: str = "127.0.0.1",
  port: int = 11434,
  timeout: float = HTTP_TIMEOUT_SECONDS,
) -> list[Finding]:
  """Check harmless Ollama metadata endpoints on localhost only."""
  safe_host = ensure_safe_target(host)
  url_host = f"[{safe_host}]" if ":" in safe_host else safe_host
  base_url = f"http://{url_host}:{port}"
  version_status, version_json, version_body = _safe_json_get(f"{base_url}/api/version", timeout)
  tags_status, tags_json, tags_body = _safe_json_get(f"{base_url}/api/tags", timeout)

  if version_status == 0 and tags_status == 0:
    return [
      Finding(
        name="Ollama localhost reachability",
        status="OK",
        severity="OK",
        summary="Ollama was not reachable on the local default port.",
        evidence=f"/api/version: {version_body}; /api/tags: {tags_body}",
        recommendation="No action needed unless you expect Ollama to be running locally.",
        target=f"{safe_host}:{port}",
      )
    ]

  reachable = version_status in {200, 401, 403} or tags_status in {200, 401, 403}
  status = "WARN" if reachable else "INFO"
  model_count = 0
  if isinstance(tags_json, dict) and isinstance(tags_json.get("models"), list):
    model_count = len(tags_json["models"])

  return [
    Finding(
      name="Ollama metadata endpoint",
      status=status,
      severity=status,
      summary="Ollama appears reachable through local metadata endpoints."
      if reachable
      else "A service responded on the Ollama port but did not look like Ollama.",
      evidence=(
        f"/api/version HTTP {version_status}; /api/tags HTTP {tags_status}; "
        f"visible model records: {model_count}"
      ),
      recommendation=(
        "Keep Ollama bound to localhost. If remote access is required, place strong "
        "authentication, TLS, rate limits, and network allowlists in front of it."
      ),
      target=f"{safe_host}:{port}",
      metadata={"version": version_json or {}, "tags_preview": tags_json or {}},
    )
  ]
