"""Practical learning path for AI infrastructure CVE contribution."""

from __future__ import annotations

import streamlit as st

MILESTONES = [
  "Understand CVE, CNA, CVSS, and CWE roles in vulnerability coordination.",
  "Build the local AI lab and confirm every target is localhost-only.",
  "Run safe exposure checks against mock AI services.",
  "Write detection logic that produces OK, WARN, CRIT, or INFO results.",
  "Study existing AI infrastructure CVEs with verified source material.",
  "Create hardening pull requests that reduce real operational risk.",
  "Practice responsible disclosure with clear evidence and a careful timeline.",
  "Publish defensive case studies focused on validation and remediation.",
]


def render() -> None:
  """Render learning milestones."""
  st.title("Learning Path")
  st.info("A practical route from local lab practice to responsible AI infrastructure research.")

  for index, milestone in enumerate(MILESTONES, start=1):
    st.checkbox(milestone, key=f"milestone_{index}")

  st.subheader("Portfolio habits")
  st.write(
    "Keep reports reproducible, screenshots local, detection logic readable, and claims tied to "
    "safe evidence. Focus on reducing risk, not proving impact through unsafe behavior."
  )
