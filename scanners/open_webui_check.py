"""Safe local Open WebUI-style exposure and header checks."""

from __future__ import annotations

from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.config import HTTP_TIMEOUT_SECONDS
from app.models import Finding
from scanners.safety import ensure_safe_target

SECURITY_HEADERS = (
  "content-security-policy",
  "x-frame-options",
  "x-content-type-options",
  "referrer-policy",
  "permissions-policy",
)


def _get_headers(url: str, timeout: float) -> tuple[int, dict[str, str], str]:
  """Fetch only page headers and a small body preview."""
  request = Request(url, method="GET")
  try:
    with urlopen(request, timeout=timeout) as response:
      body = response.read(2048).decode("utf-8", errors="replace")
      headers = {key.lower(): value for key, value in response.headers.items()}
      return response.status, headers, body[:300]
  except HTTPError as exc:
    headers = {key.lower(): value for key, value in exc.headers.items()}
    return exc.code, headers, str(exc)
  except URLError as exc:
    return 0, {}, str(exc.reason)
  except TimeoutError:
    return 0, {}, "request timed out"


def run_check(
  host: str = "127.0.0.1",
  port: int = 8080,
  timeout: float = HTTP_TIMEOUT_SECONDS,
) -> list[Finding]:
  """Check a local UI endpoint and report missing basic security headers."""
  safe_host = ensure_safe_target(host)
  url_host = f"[{safe_host}]" if ":" in safe_host else safe_host
  url = f"http://{url_host}:{port}/"
  status_code, headers, body_preview = _get_headers(url, timeout)
  if status_code == 0:
    return [
      Finding(
        name="Open WebUI localhost reachability",
        status="OK",
        severity="OK",
        summary="No Open WebUI-like service was reachable on the local default port.",
        evidence=body_preview,
        recommendation="No action needed unless you expect a local UI to be running.",
        target=f"{safe_host}:{port}",
      )
    ]

  missing = [header for header in SECURITY_HEADERS if header not in headers]
  finding_status = "WARN" if missing else "OK"
  return [
    Finding(
      name="Open WebUI security headers",
      status=finding_status,
      severity=finding_status,
      summary="Local UI responded and was checked for baseline browser security headers.",
      evidence=(
        f"HTTP {status_code}; missing headers: {', '.join(missing) if missing else 'none'}; "
        f"body preview: {body_preview[:120]}"
      ),
      recommendation=(
        "Require authentication, use HTTPS for any remote access, set secure cookies, "
        "and place the UI behind a hardened reverse proxy with security headers."
      ),
      target=f"{safe_host}:{port}",
      metadata={"missing_headers": missing, "headers": headers},
    )
  ]
