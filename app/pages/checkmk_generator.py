"""Checkmk local check display and guidance page."""

from __future__ import annotations

import streamlit as st

from app.config import CHECKMK_DIR


def render() -> None:
  """Render included Checkmk local checks."""
  st.title("Checkmk Check Generator")
  st.info("These checks inspect only local machine state and use Checkmk local check output format.")

  scripts = sorted(CHECKMK_DIR.glob("*.sh"))
  if not scripts:
    st.warning("No Checkmk scripts found.")
    return

  for script in scripts:
    st.subheader(script.name)
    st.write(
      "Copy this script into a Checkmk local checks directory on a lab host when you want "
      "passive local monitoring of AI runtime exposure signals."
    )
    st.code(script.read_text(encoding="utf-8"), language="bash")
