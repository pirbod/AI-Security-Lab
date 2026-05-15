"""Tests for scanner target safety boundaries."""

from __future__ import annotations

import pytest

from scanners.safety import ensure_safe_target, validate_target


def test_allows_loopback_targets() -> None:
  """Loopback names and addresses are allowed."""
  assert validate_target("localhost").allowed
  assert validate_target("127.0.0.1").allowed
  assert validate_target("::1").allowed
  assert validate_target("http://127.0.0.1:11434/api/version").allowed


def test_blocks_public_ips_and_domains_by_default() -> None:
  """Public targets and domains stay outside the lab scope."""
  assert not validate_target("8.8.8.8").allowed
  assert not validate_target("example.com").allowed
  with pytest.raises(ValueError):
    ensure_safe_target("https://example.com")


def test_private_networks_require_explicit_enablement() -> None:
  """Private lab networks are opt-in."""
  assert not validate_target("192.168.1.10").allowed
  assert validate_target("192.168.1.10", allow_private_networks=True).allowed


def test_rejects_large_cidr_ranges() -> None:
  """Ranges larger than four addresses are blocked."""
  assert validate_target("10.0.0.0/30", allow_private_networks=True).allowed
  assert not validate_target("10.0.0.0/29", allow_private_networks=True).allowed
  assert not validate_target("127.0.0.0/24").allowed
