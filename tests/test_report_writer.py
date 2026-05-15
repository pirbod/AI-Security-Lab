"""Tests for Markdown and JSON report generation."""

from __future__ import annotations

import json

from app.models import Finding
from app.report_writer import write_report


def test_write_report_creates_markdown_and_json(tmp_path) -> None:
  """Report writer saves matching Markdown and JSON files."""
  finding = Finding(
    name="Test finding",
    status="WARN",
    severity="WARN",
    summary="A local warning was detected.",
    evidence="unit test evidence",
    recommendation="Review the local configuration.",
  )
  paths = write_report(
    report_type="unit-test-report",
    title="Unit Test Report",
    scope="localhost only",
    findings=[finding],
    output_dir=tmp_path,
  )

  assert paths["markdown"].exists()
  assert paths["json"].exists()
  markdown = paths["markdown"].read_text(encoding="utf-8")
  payload = json.loads(paths["json"].read_text(encoding="utf-8"))
  assert "Unit Test Report" in markdown
  assert payload["findings"][0]["status"] == "WARN"
  assert "local defensive testing" in payload["disclaimer"].lower()
