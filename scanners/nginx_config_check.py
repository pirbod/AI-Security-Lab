"""Static Nginx hardening checks for bundled lab configs only."""

from __future__ import annotations

import re
from pathlib import Path

from app.config import NGINX_CONFIG_DIR
from app.models import Finding

SECURITY_HEADERS = (
  "Content-Security-Policy",
  "X-Frame-Options",
  "X-Content-Type-Options",
  "Referrer-Policy",
)


def _has_any(text: str, patterns: tuple[str, ...]) -> bool:
  """Return true when any regular expression matches."""
  return any(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) for pattern in patterns)


def check_nginx_config(path: Path) -> list[Finding]:
  """Check one local lab Nginx config file without modifying it."""
  text = path.read_text(encoding="utf-8")
  target = str(path)
  findings: list[Finding] = []

  checks = [
    (
      "client_max_body_size",
      _has_any(text, (r"\bclient_max_body_size\b",)),
      "Set client_max_body_size to cap request bodies for AI runtime routes.",
    ),
    (
      "rate limiting",
      _has_any(text, (r"\blimit_req_zone\b", r"\blimit_req\b")),
      "Add limit_req_zone and limit_req for local reverse proxy examples.",
    ),
    (
      "proxy timeout settings",
      _has_any(text, (r"\bproxy_read_timeout\b", r"\bproxy_connect_timeout\b")),
      "Set proxy_connect_timeout, proxy_read_timeout, and proxy_send_timeout.",
    ),
    (
      "authentication notes",
      _has_any(text, (r"\bauth_basic\b", r"authentication", r"auth proxy")),
      "Document authentication expectations or enable auth_basic for examples.",
    ),
  ]

  for label, passed, recommendation in checks:
    findings.append(
      Finding(
        name=f"Nginx {label}",
        status="OK" if passed else "WARN",
        severity="OK" if passed else "WARN",
        summary=f"{path.name}: {label} {'is present' if passed else 'is missing'}.",
        evidence=f"Static review of {path.name}.",
        recommendation=recommendation,
        target=target,
      )
    )

  for header in SECURITY_HEADERS:
    present = re.search(rf"add_header\s+{re.escape(header)}\b", text, flags=re.IGNORECASE)
    findings.append(
      Finding(
        name=f"Nginx security header {header}",
        status="OK" if present else "WARN",
        severity="OK" if present else "WARN",
        summary=f"{path.name}: {header} {'is configured' if present else 'is missing'}.",
        evidence=f"Static review of {path.name}.",
        recommendation=f"Add an appropriate {header} header for browser-facing routes.",
        target=target,
      )
    )

  unsafe_proxy = re.search(
    r"proxy_pass\s+http://(0\.0\.0\.0|\[::\]|[^;\s]*example\.com|[^;\s]*public)",
    text,
    flags=re.IGNORECASE,
  )
  findings.append(
    Finding(
      name="Nginx unsafe proxy_pass example",
      status="WARN" if unsafe_proxy else "OK",
      severity="WARN" if unsafe_proxy else "OK",
      summary=f"{path.name}: unsafe proxy_pass examples {'were found' if unsafe_proxy else 'were not found'}.",
      evidence=unsafe_proxy.group(0) if unsafe_proxy else "No unsafe proxy_pass pattern matched.",
      recommendation="Proxy only to explicit local upstreams in the lab examples.",
      target=target,
    )
  )

  return findings


def check_nginx_configs(config_dir: Path = NGINX_CONFIG_DIR) -> list[Finding]:
  """Check all bundled lab Nginx config files."""
  if not config_dir.exists():
    return [
      Finding(
        name="Nginx config directory",
        status="WARN",
        severity="WARN",
        summary="The lab Nginx configuration directory was not found.",
        evidence=str(config_dir),
        recommendation="Restore lab_services/nginx before running this check.",
        target=str(config_dir),
      )
    ]

  configs = sorted(config_dir.glob("*.conf"))
  if not configs:
    return [
      Finding(
        name="Nginx config files",
        status="WARN",
        severity="WARN",
        summary="No bundled Nginx config files were found.",
        evidence=str(config_dir),
        recommendation="Add local lab Nginx config files before running this check.",
        target=str(config_dir),
      )
    ]

  findings: list[Finding] = []
  for config in configs:
    findings.extend(check_nginx_config(config))
  return findings
