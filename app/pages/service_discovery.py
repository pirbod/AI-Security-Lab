"""Clickable local service discovery page."""

from __future__ import annotations

import streamlit as st

from app.database import save_report_metadata
from app.report_writer import write_report
from scanners.localhost_ports import scan_localhost_ports


def render() -> None:
  """Render local-only service discovery controls."""
  st.title("Local Service Discovery")
  st.warning("Targets are restricted to 127.0.0.1, localhost, and ::1.")
  host = st.selectbox("Target", ["127.0.0.1", "localhost", "::1"])
  timeout = st.slider("Connection timeout seconds", 0.1, 2.0, 0.75, 0.05)

  if st.button("Scan local AI ports"):
    findings = scan_localhost_ports(host=host, timeout=timeout)
    st.dataframe([finding.to_dict() for finding in findings], use_container_width=True)

    paths = write_report(
      report_type="local-service-discovery",
      title="Local Service Discovery Report",
      scope=host,
      findings=findings,
      summary="Local-only TCP reachability checks for common AI infrastructure ports.",
    )
    save_report_metadata(
      report_type="local-service-discovery",
      title="Local Service Discovery Report",
      markdown_path=str(paths["markdown"]),
      json_path=str(paths["json"]),
    )
    st.success(f"Report written to {paths['markdown']}")
