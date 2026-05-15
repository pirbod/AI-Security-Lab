"""Streamlit entrypoint for the clickable local AI security lab."""

from __future__ import annotations

import streamlit as st

from app.config import LAB_DISCLAIMER, LAB_NAME
from app.pages import (
  advisory_builder,
  checkmk_generator,
  cve_casebook,
  dashboard,
  docker_security,
  learning_path,
  local_runtime_checks,
  nginx_hardening,
  service_discovery,
)

PAGES = {
  "Lab overview": dashboard.render,
  "Local service discovery": service_discovery.render,
  "AI runtime exposure checks": local_runtime_checks.render,
  "Docker security checks": docker_security.render,
  "Nginx hardening checks": nginx_hardening.render,
  "CVE casebook": cve_casebook.render,
  "Advisory builder": advisory_builder.render,
  "Checkmk check generator": checkmk_generator.render,
  "Learning path": learning_path.render,
}


def main() -> None:
  """Render the clickable lab UI."""
  st.set_page_config(page_title=LAB_NAME, layout="wide")
  st.sidebar.title(LAB_NAME)
  selected = st.sidebar.radio("Section", list(PAGES), label_visibility="collapsed")
  st.sidebar.warning(LAB_DISCLAIMER)
  PAGES[selected]()


if __name__ == "__main__":
  main()
