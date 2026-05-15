"""Runtime-specific local AI exposure checks."""

from __future__ import annotations

import streamlit as st

from app.database import save_report_metadata
from app.report_writer import write_report
from scanners.open_webui_check import run_check as open_webui_check
from scanners.ollama_check import run_check as ollama_check
from scanners.vllm_check import run_check as vllm_check


def _show_findings(title: str, report_type: str, findings: list[object]) -> None:
  """Display findings and offer a report export."""
  st.subheader(title)
  rows = [finding.to_dict() for finding in findings]
  st.dataframe(rows, use_container_width=True)
  if st.button(f"Generate {title} report"):
    paths = write_report(
      report_type=report_type,
      title=f"{title} Report",
      scope="localhost only",
      findings=findings,  # type: ignore[arg-type]
      summary=f"Safe local metadata checks for {title}.",
    )
    save_report_metadata(
      report_type=report_type,
      title=f"{title} Report",
      markdown_path=str(paths["markdown"]),
      json_path=str(paths["json"]),
    )
    st.success(f"Report written to {paths['markdown']}")


def render() -> None:
  """Render safe runtime checks."""
  st.title("AI Runtime Exposure Checks")
  st.info("These checks query only harmless local metadata endpoints and never send prompts.")

  tabs = st.tabs(["Ollama", "vLLM-style API", "Open WebUI-style UI"])
  with tabs[0]:
    if st.button("Run Ollama check"):
      _show_findings("Ollama Exposure", "ollama-exposure", ollama_check())
  with tabs[1]:
    if st.button("Run vLLM-style check"):
      _show_findings("vLLM Exposure", "vllm-exposure", vllm_check())
  with tabs[2]:
    if st.button("Run Open WebUI-style check"):
      _show_findings("Open WebUI Exposure", "open-webui-exposure", open_webui_check())
