"""Placeholder casebook for AI infrastructure CVE study notes."""

from __future__ import annotations

import json

import streamlit as st

PLACEHOLDERS = [
  {
    "CVE ID": "CVE-YYYY-NNNN",
    "Product": "Example AI runtime",
    "Affected versions": "Placeholder only",
    "Root cause": "Example missing authentication boundary",
    "Impact": "Example unauthorized metadata access",
    "Detection idea": "Check local headers and auth enforcement in an approved lab",
    "Remediation": "Require auth, narrow bind address, add rate limits",
    "Lessons learned": "Turn product behavior into safe detection logic and clear reporting",
  },
  {
    "CVE ID": "CVE-YYYY-MMMM",
    "Product": "Example model UI",
    "Affected versions": "Placeholder only",
    "Root cause": "Example insecure reverse proxy configuration",
    "Impact": "Example exposure of local admin UI",
    "Detection idea": "Review local proxy config for missing auth and security headers",
    "Remediation": "Harden proxy, add secure headers, restrict network access",
    "Lessons learned": "Configuration flaws can be reported with strong evidence and safe scope",
  },
]


def render() -> None:
  """Render editable study notes with placeholder examples only."""
  st.title("CVE Casebook")
  st.info("Seed entries are placeholders for learning structure. Fill in real facts during study.")

  if "casebook_entries" not in st.session_state:
    st.session_state.casebook_entries = PLACEHOLDERS.copy()

  with st.form("casebook_form"):
    cve_id = st.text_input("CVE ID", "CVE-YYYY-NNNN")
    product = st.text_input("Product")
    affected = st.text_input("Affected versions")
    root_cause = st.text_area("Root cause")
    impact = st.text_area("Impact")
    detection = st.text_area("Detection idea")
    remediation = st.text_area("Remediation")
    lessons = st.text_area("Lessons learned")
    submitted = st.form_submit_button("Add casebook entry")

  if submitted:
    st.session_state.casebook_entries.append(
      {
        "CVE ID": cve_id,
        "Product": product,
        "Affected versions": affected,
        "Root cause": root_cause,
        "Impact": impact,
        "Detection idea": detection,
        "Remediation": remediation,
        "Lessons learned": lessons,
      }
    )
    st.success("Entry added to this session.")

  st.dataframe(st.session_state.casebook_entries, use_container_width=True)
  st.download_button(
    "Download casebook JSON",
    json.dumps(st.session_state.casebook_entries, indent=2),
    file_name="ai-cve-casebook.json",
    mime="application/json",
  )
