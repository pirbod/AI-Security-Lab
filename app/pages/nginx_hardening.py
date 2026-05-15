"""Nginx hardening page for bundled lab configs."""

from __future__ import annotations

import streamlit as st

from app.config import NGINX_CONFIG_DIR
from app.database import save_report_metadata
from app.report_writer import write_report
from scanners.nginx_config_check import check_nginx_configs


def render() -> None:
  """Render static Nginx config checks."""
  st.title("Nginx Hardening Checks")
  st.info(f"Reviewing bundled lab configs only: {NGINX_CONFIG_DIR}")

  if st.button("Review lab Nginx configs"):
    findings = check_nginx_configs()
    st.dataframe([finding.to_dict() for finding in findings], use_container_width=True)
    paths = write_report(
      report_type="nginx-hardening-report",
      title="Nginx Hardening Report",
      scope=str(NGINX_CONFIG_DIR),
      findings=findings,
      summary="Static hardening review of local lab Nginx reverse proxy examples.",
    )
    save_report_metadata(
      report_type="nginx-hardening-report",
      title="Nginx Hardening Report",
      markdown_path=str(paths["markdown"]),
      json_path=str(paths["json"]),
    )
    st.success(f"Report written to {paths['markdown']}")
