"""Optional FastAPI backend for local automation around the lab."""

from __future__ import annotations

from fastapi import FastAPI

from app.database import recent_reports
from scanners.localhost_ports import scan_localhost_ports
from scanners.nginx_config_check import check_nginx_configs

app = FastAPI(
  title="AI Security Lab Local API",
  description="Local-only defensive security lab API.",
  version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
  """Return a simple local health response."""
  return {"status": "ok", "scope": "localhost-only"}


@app.get("/checks/ports")
def local_ports() -> dict[str, object]:
  """Run the local-only port discovery check."""
  findings = scan_localhost_ports()
  return {"findings": [finding.to_dict() for finding in findings]}


@app.get("/checks/nginx")
def nginx_checks() -> dict[str, object]:
  """Run static checks against bundled lab Nginx configs."""
  findings = check_nginx_configs()
  return {"findings": [finding.to_dict() for finding in findings]}


@app.get("/reports/recent")
def reports() -> dict[str, object]:
  """Return recent local report metadata."""
  return {"reports": recent_reports()}
