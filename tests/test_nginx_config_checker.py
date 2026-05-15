"""Tests for bundled Nginx static hardening checks."""

from __future__ import annotations

from scanners.nginx_config_check import check_nginx_config


def test_nginx_checker_warns_on_missing_controls(tmp_path) -> None:
  """Minimal proxy config should produce warnings."""
  config = tmp_path / "insecure.conf"
  config.write_text(
    """
    server {
      listen 80;
      location / {
        proxy_pass http://mock-open-webui:8080;
      }
    }
    """,
    encoding="utf-8",
  )

  findings = check_nginx_config(config)
  assert any(finding.status == "WARN" for finding in findings)
  assert any(finding.name == "Nginx client_max_body_size" for finding in findings)


def test_nginx_checker_accepts_hardened_controls(tmp_path) -> None:
  """Config with baseline controls should pass the core checks."""
  config = tmp_path / "hardened.conf"
  config.write_text(
    """
    limit_req_zone $binary_remote_addr zone=local_ai_limit:10m rate=5r/s;
    server {
      listen 80;
      client_max_body_size 2m;
      add_header Content-Security-Policy "default-src 'self'" always;
      add_header X-Frame-Options "DENY" always;
      add_header X-Content-Type-Options "nosniff" always;
      add_header Referrer-Policy "no-referrer" always;
      # authentication note for non-local use
      location / {
        limit_req zone=local_ai_limit burst=10 nodelay;
        proxy_connect_timeout 3s;
        proxy_read_timeout 30s;
        proxy_send_timeout 30s;
        proxy_pass http://mock-open-webui:8080;
      }
    }
    """,
    encoding="utf-8",
  )

  findings = check_nginx_config(config)
  assert all(finding.status == "OK" for finding in findings)
