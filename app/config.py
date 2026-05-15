"""Central configuration for local-only lab behavior."""

from __future__ import annotations

import os
from pathlib import Path

LAB_NAME = "AI Security Lab"
LAB_DISCLAIMER = (
  "This lab is for local defensive testing on a personal device only. "
  "It must not be used to scan public systems or third-party networks."
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_ROOT / "reports" / "generated"
TEMPLATE_DIR = PROJECT_ROOT / "reports" / "templates"
DATABASE_PATH = PROJECT_ROOT / "reports" / "lab.sqlite3"
NGINX_CONFIG_DIR = PROJECT_ROOT / "lab_services" / "nginx"
CHECKMK_DIR = PROJECT_ROOT / "checks" / "checkmk"

HTTP_TIMEOUT_SECONDS = float(os.getenv("AI_LAB_HTTP_TIMEOUT_SECONDS", "2.0"))
SOCKET_TIMEOUT_SECONDS = float(os.getenv("AI_LAB_SOCKET_TIMEOUT_SECONDS", "0.75"))
ALLOW_PRIVATE_LAB_NETWORKS = os.getenv("AI_LAB_ALLOW_PRIVATE_NETWORKS", "0") == "1"

LOCAL_TARGETS = ("127.0.0.1", "localhost", "::1")

COMMON_LOCAL_PORTS = [
  {
    "port": 11434,
    "service": "Ollama",
    "risk": "WARN",
    "recommendation": "Keep bound to localhost; add authentication before any remote access.",
  },
  {
    "port": 8000,
    "service": "vLLM or FastAPI",
    "risk": "WARN",
    "recommendation": "Require authentication, rate limits, and request body limits.",
  },
  {
    "port": 8080,
    "service": "Open WebUI",
    "risk": "WARN",
    "recommendation": "Require login, secure cookies, and reverse proxy hardening.",
  },
  {
    "port": 3000,
    "service": "Local UI service",
    "risk": "INFO",
    "recommendation": "Confirm the UI is local-only and not proxying sensitive services.",
  },
  {
    "port": 9090,
    "service": "Prometheus",
    "risk": "WARN",
    "recommendation": "Avoid exposing metrics remotely without authentication.",
  },
  {
    "port": 80,
    "service": "Local HTTP",
    "risk": "INFO",
    "recommendation": "Use only for local lab traffic; add TLS and auth for remote use.",
  },
  {
    "port": 443,
    "service": "Local HTTPS",
    "risk": "INFO",
    "recommendation": "Verify certificates and proxy rules before any non-local use.",
  },
]
