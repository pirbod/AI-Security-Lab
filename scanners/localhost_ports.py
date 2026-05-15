"""Localhost-only TCP port discovery for common AI infrastructure services."""

from __future__ import annotations

import socket
from collections.abc import Iterable

from app.config import COMMON_LOCAL_PORTS, SOCKET_TIMEOUT_SECONDS
from app.models import Finding
from scanners.safety import ensure_safe_target, is_loopback_host


def _port_metadata(port: int) -> dict[str, str | int]:
  """Return the configured service metadata for a port."""
  for item in COMMON_LOCAL_PORTS:
    if item["port"] == port:
      return item
  return {
    "port": port,
    "service": "Unknown local service",
    "risk": "INFO",
    "recommendation": "Identify the owner and confirm it is bound only to loopback.",
  }


def is_port_open(host: str, port: int, timeout: float = SOCKET_TIMEOUT_SECONDS) -> bool:
  """Check a single local TCP port with a short timeout."""
  try:
    with socket.socket(socket.AF_INET6 if ":" in host else socket.AF_INET, socket.SOCK_STREAM) as sock:
      sock.settimeout(timeout)
      address = (host, port, 0, 0) if ":" in host else (host, port)
      return sock.connect_ex(address) == 0
  except OSError:
    return False


def scan_localhost_ports(
  host: str = "127.0.0.1",
  ports: Iterable[int] | None = None,
  timeout: float = SOCKET_TIMEOUT_SECONDS,
) -> list[Finding]:
  """Scan only explicitly allowed loopback targets for known local lab ports."""
  normalized_host = ensure_safe_target(host)
  if not is_loopback_host(normalized_host):
    raise ValueError("Local service discovery only supports localhost targets.")

  selected_ports = list(ports or [int(item["port"]) for item in COMMON_LOCAL_PORTS])
  findings: list[Finding] = []
  for port in selected_ports:
    metadata = _port_metadata(int(port))
    open_port = is_port_open(normalized_host, int(port), timeout)
    service = str(metadata["service"])
    if open_port:
      status = str(metadata["risk"])
      summary = f"{service} appears reachable on {normalized_host}:{port}."
      evidence = "TCP connection succeeded against an explicitly local target."
    else:
      status = "OK"
      summary = f"{service} is not listening on {normalized_host}:{port}."
      evidence = "TCP connection failed or timed out within the safe timeout."

    findings.append(
      Finding(
        name=f"Local port {port}",
        status=status,  # type: ignore[arg-type]
        severity=status,  # type: ignore[arg-type]
        summary=summary,
        evidence=evidence,
        recommendation=str(metadata["recommendation"]),
        target=f"{normalized_host}:{port}",
        metadata={
          "port": port,
          "possible_service": service,
          "risk_level": status,
          "timeout_seconds": timeout,
        },
      )
    )
  return findings
