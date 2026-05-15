"""Docker security check page."""

from __future__ import annotations

import streamlit as st

from app.database import save_report_metadata
from app.report_writer import write_report
from scanners.docker_check import run_check


def render() -> None:
  """Render read-only Docker checks."""
  st.title("Docker Security Checks")
  st.info("This check reads local Docker metadata only and continues safely if Docker is unavailable.")

  if st.button("Inspect local Docker containers"):
    findings = run_check()
    st.dataframe([finding.to_dict() for finding in findings], use_container_width=True)
    paths = write_report(
      report_type="docker-security-report",
      title="Docker Security Report",
      scope="local Docker daemon",
      findings=findings,
      summary="Read-only inspection of local running container security settings.",
    )
    save_report_metadata(
      report_type="docker-security-report",
      title="Docker Security Report",
      markdown_path=str(paths["markdown"]),
      json_path=str(paths["json"]),
    )
    st.success(f"Report written to {paths['markdown']}")
