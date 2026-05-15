"""Dashboard page for current risk posture and report history."""

from __future__ import annotations

import streamlit as st

from app.database import recent_reports, save_report_metadata
from app.models import Finding, STATUS_ORDER
from app.report_writer import write_report
from scanners.localhost_ports import scan_localhost_ports
from scanners.nginx_config_check import check_nginx_configs
from scanners.open_webui_check import run_check as open_webui_check
from scanners.ollama_check import run_check as ollama_check
from scanners.vllm_check import run_check as vllm_check


def _counts(findings: list[Finding]) -> dict[str, int]:
  """Count findings by status."""
  return {status: sum(item.status == status for item in findings) for status in STATUS_ORDER}


def _recommended_action(findings: list[Finding]) -> str:
  """Pick the next action from the highest-risk finding."""
  critical = [item for item in findings if item.status == "CRIT"]
  warning = [item for item in findings if item.status == "WARN"]
  if critical:
    return critical[0].recommendation
  if warning:
    return warning[0].recommendation
  return "Continue documenting safe findings and hardening decisions."


def _risk_summary(counts: dict[str, int]) -> str:
  """Summarize dashboard posture for quick reading."""
  if counts["CRIT"]:
    return "Critical local hardening issues need attention."
  if counts["WARN"]:
    return "Warnings found. Review whether each local service needs tighter controls."
  return "No critical or warning findings in the default local checks."


def render() -> None:
  """Render the lab overview dashboard."""
  st.title("Local AI Infrastructure Security Lab")
  st.info("Practice safe validation, detection engineering, reporting, and hardening locally.")

  with st.spinner("Running safe default local checks..."):
    findings = []
    findings.extend(scan_localhost_ports(timeout=0.35))
    findings.extend(ollama_check(timeout=0.75))
    findings.extend(vllm_check(timeout=0.75))
    findings.extend(open_webui_check(timeout=0.75))
    findings.extend(check_nginx_configs())

  counts = _counts(findings)
  cols = st.columns(5)
  cols[0].metric("Total checks", len(findings))
  cols[1].metric("OK", counts["OK"])
  cols[2].metric("WARN", counts["WARN"])
  cols[3].metric("CRIT", counts["CRIT"])
  cols[4].metric("INFO", counts["INFO"])

  st.subheader("Risk summary")
  st.write(_risk_summary(counts))
  st.subheader("Recommended next action")
  st.write(_recommended_action(findings))

  st.subheader("Current findings")
  st.dataframe([finding.to_dict() for finding in findings], use_container_width=True)

  if st.button("Generate local AI exposure report"):
    paths = write_report(
      report_type="local-ai-exposure-report",
      title="Local AI Exposure Report",
      scope="localhost only",
      findings=findings,
      summary="Default local dashboard checks for AI runtime exposure and proxy hardening.",
    )
    save_report_metadata(
      report_type="local-ai-exposure-report",
      title="Local AI Exposure Report",
      markdown_path=str(paths["markdown"]),
      json_path=str(paths["json"]),
    )
    st.success(f"Report written to {paths['markdown']}")

  st.subheader("Recent reports")
  reports = recent_reports()
  if reports:
    st.dataframe(reports, use_container_width=True)
  else:
    st.write("No reports generated yet.")
