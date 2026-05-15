"""Shared models used by scanners, reports, and the UI."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

Status = Literal["OK", "WARN", "CRIT", "INFO"]

STATUS_ORDER: tuple[Status, ...] = ("OK", "WARN", "CRIT", "INFO")


@dataclass(slots=True)
class Finding:
  """A single check result with evidence and a practical recommendation."""

  name: str
  status: Status
  severity: Status
  summary: str
  evidence: str = ""
  recommendation: str = ""
  target: str = "localhost"
  metadata: dict[str, Any] = field(default_factory=dict)

  def to_dict(self) -> dict[str, Any]:
    """Return a JSON-friendly representation of the finding."""
    return asdict(self)


@dataclass(slots=True)
class ScanResult:
  """A named collection of findings from one scanner run."""

  scanner: str
  scope: str
  findings: list[Finding]

  def counts(self) -> dict[str, int]:
    """Count findings by status for dashboard display."""
    return {status: sum(item.status == status for item in self.findings) for status in STATUS_ORDER}

  def to_dict(self) -> dict[str, Any]:
    """Return a JSON-friendly representation of the scan result."""
    return {
      "scanner": self.scanner,
      "scope": self.scope,
      "findings": [finding.to_dict() for finding in self.findings],
      "counts": self.counts(),
    }
