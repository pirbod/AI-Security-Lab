"""Responsible disclosure advisory builder page."""

from __future__ import annotations

import re
from datetime import UTC, datetime

import streamlit as st

from app.config import REPORT_DIR
from app.report_writer import build_advisory_markdown

FIELD_DEFS = [
  ("Title", "title"),
  ("Product", "product"),
  ("Vendor or maintainer", "vendor_or_maintainer"),
  ("Affected version", "affected_version"),
  ("Fixed version", "fixed_version"),
  ("Vulnerability type", "vulnerability_type"),
  ("CWE candidate", "cwe_candidate"),
  ("CVSS candidate", "cvss_candidate"),
  ("Attack preconditions", "attack_preconditions"),
  ("Impact", "impact"),
  ("Reproduction summary", "reproduction_summary"),
  ("Evidence", "evidence"),
  ("Mitigation", "mitigation"),
  ("Disclosure timeline", "disclosure_timeline"),
  ("Credits", "credits"),
]


def _slug(value: str) -> str:
  """Create a simple report filename slug."""
  return re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-") or "advisory"


def render() -> None:
  """Render advisory drafting form."""
  st.title("Advisory Builder")
  st.info("Draft responsible disclosure reports from safe, authorized, local findings.")

  with st.form("advisory_form"):
    fields: dict[str, str] = {}
    for label, key in FIELD_DEFS:
      fields[key] = st.text_area(label) if key in {"impact", "evidence", "mitigation"} else st.text_input(label)
    submitted = st.form_submit_button("Export Markdown advisory")

  if submitted:
    markdown = build_advisory_markdown(fields)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}-{_slug(fields.get('title', 'advisory'))}.md"
    path = REPORT_DIR / filename
    path.write_text(markdown, encoding="utf-8")
    st.success(f"Advisory draft written to {path}")
    st.download_button("Download advisory Markdown", markdown, file_name=filename, mime="text/markdown")
    st.markdown(markdown)
