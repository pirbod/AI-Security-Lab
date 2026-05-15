"""Tests for advisory Markdown export."""

from __future__ import annotations

from app.report_writer import build_advisory_markdown


def test_advisory_export_contains_required_fields() -> None:
  """Advisory builder includes the expected disclosure sections."""
  markdown = build_advisory_markdown(
    {
      "title": "Local Mock Finding",
      "product": "Mock AI Runtime",
      "vendor_or_maintainer": "Local lab",
      "impact": "Local defensive learning impact.",
    }
  )

  assert "# Local Mock Finding" in markdown
  assert "## Product" in markdown
  assert "Mock AI Runtime" in markdown
  assert "## CWE candidate" in markdown
  assert "local defensive testing" in markdown.lower()
