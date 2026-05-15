"""Safe local checks for vLLM-like OpenAI-compatible APIs."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.config import HTTP_TIMEOUT_SECONDS
from app.models import Finding
from scanners.safety import ensure_safe_target


def _get_json(url: str, timeout: float) -> tuple[int, dict[str, object] | None, str]:
  """Fetch a harmless metadata endpoint and cap the response body."""
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
  port: int = 8000,
  timeout: float = HTTP_TIMEOUT_SECONDS,
) -> list[Finding]:
  """Detect local OpenAI-compatible metadata endpoints without issuing inference."""
  safe_host = ensure_safe_target(host)
  url_host = f"[{safe_host}]" if ":" in safe_host else safe_host
  base_url = f"http://{url_host}:{port}"
  models_status, models_json, models_body = _get_json(f"{base_url}/v1/models", timeout)
  health_status, _, health_body = _get_json(f"{base_url}/health", timeout)

  if models_status == 0 and health_status == 0:
    return [
      Finding(
        name="vLLM localhost reachability",
        status="OK",
        severity="OK",
        summary="No vLLM-like service was reachable on the local default port.",
        evidence=f"/v1/models: {models_body}; /health: {health_body}",
        recommendation="No action needed unless you expect a local inference API to be running.",
        target=f"{safe_host}:{port}",
      )
    ]

  looks_openai = models_status in {200, 401, 403}
  data = models_json.get("data", []) if isinstance(models_json, dict) else []
  model_count = len(data) if isinstance(data, list) else 0
  status = "WARN" if looks_openai else "INFO"
  return [
    Finding(
      name="OpenAI-compatible metadata endpoint",
      status=status,
      severity=status,
      summary="A local OpenAI-compatible models endpoint appears reachable."
      if looks_openai
      else "A service responded on the vLLM port but did not expose expected metadata.",
      evidence=(
        f"/v1/models HTTP {models_status}; /health HTTP {health_status}; "
        f"model records: {model_count}"
      ),
      recommendation=(
        "Add authentication, rate limits, request body limits, network restrictions, "
        "and documented maximum request sizes before remote use. Do not validate "
        "limits with load or denial-of-service tests in this lab."
      ),
      target=f"{safe_host}:{port}",
      metadata={"models_preview": models_json or {}, "limit_note": "Documented review only"},
    )
  ]
