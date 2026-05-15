"""Tests for localhost-only port scanning."""

from __future__ import annotations

import socket

import pytest

from scanners.localhost_ports import scan_localhost_ports


def test_detects_open_local_port() -> None:
  """A listening localhost socket is reported as reachable."""
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind(("127.0.0.1", 0))
  server.listen(1)
  port = server.getsockname()[1]
  try:
    findings = scan_localhost_ports(host="127.0.0.1", ports=[port], timeout=0.2)
  finally:
    server.close()

  assert findings[0].status == "INFO"
  assert findings[0].metadata["port"] == port
  assert "reachable" in findings[0].summary


def test_rejects_non_localhost_target() -> None:
  """The scanner refuses non-loopback targets."""
  with pytest.raises(ValueError):
    scan_localhost_ports(host="8.8.8.8", ports=[53], timeout=0.1)
