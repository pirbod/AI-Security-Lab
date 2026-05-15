"""Read-only Docker security checks for local containers."""

from __future__ import annotations

import json
import shutil
import subprocess
from typing import Any

from app.models import Finding

SENSITIVE_MOUNTS = {"/", "/etc", "/var/run", "/var/run/docker.sock"}


def _run_docker(args: list[str]) -> tuple[int, str, str]:
  """Run a Docker CLI command with a short timeout."""
  try:
    completed = subprocess.run(
      ["docker", *args],
      check=False,
      capture_output=True,
      text=True,
      timeout=5,
    )
    return completed.returncode, completed.stdout, completed.stderr
  except (OSError, subprocess.TimeoutExpired) as exc:
    return 1, "", str(exc)


def _container_records() -> tuple[list[dict[str, Any]], str]:
  """Return Docker inspect records for running containers."""
  if shutil.which("docker") is None:
    return [], "Docker CLI was not found."

  code, stdout, stderr = _run_docker(["ps", "-q"])
  if code != 0:
    return [], stderr.strip() or "Docker is not available to the current user."

  ids = [line.strip() for line in stdout.splitlines() if line.strip()]
  if not ids:
    return [], "No running containers were found."

  code, inspect_stdout, inspect_stderr = _run_docker(["inspect", *ids])
  if code != 0:
    return [], inspect_stderr.strip() or "Unable to inspect running containers."
  return json.loads(inspect_stdout), ""


def _image_uses_latest(image: str) -> bool:
  """Detect unpinned or latest image tags."""
  if "@" in image:
    return False
  if ":" not in image.rsplit("/", maxsplit=1)[-1]:
    return True
  return image.endswith(":latest")


def _finding(container: dict[str, Any], name: str, severity: str, summary: str, recommendation: str) -> Finding:
  """Build a Docker finding for a single container."""
  config = container.get("Config", {})
  image = config.get("Image", "unknown")
  container_name = str(container.get("Name", "unknown")).lstrip("/")
  return Finding(
    name=f"Docker {name}",
    status=severity,  # type: ignore[arg-type]
    severity=severity,  # type: ignore[arg-type]
    summary=f"{container_name}: {summary}",
    evidence=f"container={container_name}; image={image}",
    recommendation=recommendation,
    target=container_name,
    metadata={"container": container_name, "image": image, "finding": name},
  )


def run_check() -> list[Finding]:
  """Inspect local Docker containers without changing container state."""
  containers, message = _container_records()
  if message and not containers:
    return [
      Finding(
        name="Docker availability",
        status="WARN" if "not found" in message.lower() else "INFO",
        severity="WARN" if "not found" in message.lower() else "INFO",
        summary=message,
        evidence="Docker inspection was skipped safely.",
        recommendation="Install Docker or start local lab containers if you want container checks.",
        target="local-docker",
      )
    ]

  findings: list[Finding] = []
  for container in containers:
    config = container.get("Config", {})
    host_config = container.get("HostConfig", {})
    image = str(config.get("Image", ""))
    user = str(config.get("User", "")).strip()
    network_mode = str(host_config.get("NetworkMode", ""))
    binds = host_config.get("Binds") or []
    mounts = container.get("Mounts") or []

    if user in {"", "0", "root"}:
      findings.append(
        _finding(
          container,
          "container runs as root",
          "WARN",
          "Container process user is root or unspecified.",
          "Set a non-root USER in the image or container configuration.",
        )
      )
    if host_config.get("Privileged"):
      findings.append(
        _finding(
          container,
          "privileged mode",
          "CRIT",
          "Container is running with privileged mode enabled.",
          "Remove privileged mode and add only the minimum capabilities required.",
        )
      )
    if network_mode == "host":
      findings.append(
        _finding(
          container,
          "host network mode",
          "CRIT",
          "Container is using the host network namespace.",
          "Use bridge networking and bind ports explicitly to localhost for lab services.",
        )
      )

    mount_sources = {str(mount.get("Source", "")) for mount in mounts}
    bind_sources = {str(bind).split(":", maxsplit=1)[0] for bind in binds}
    for source in sorted(mount_sources | bind_sources):
      if source in SENSITIVE_MOUNTS:
        severity = "CRIT" if source == "/var/run/docker.sock" else "WARN"
        findings.append(
          _finding(
            container,
            f"sensitive mount {source}",
            severity,
            f"Sensitive host path is mounted: {source}.",
            "Remove sensitive host mounts unless there is a documented local-only need.",
          )
        )

    memory = int(host_config.get("Memory") or 0)
    nano_cpus = int(host_config.get("NanoCpus") or 0)
    cpu_quota = int(host_config.get("CpuQuota") or 0)
    if memory == 0 and nano_cpus == 0 and cpu_quota in {0, -1}:
      findings.append(
        _finding(
          container,
          "missing resource limits",
          "WARN",
          "No memory or CPU limits were detected.",
          "Set memory and CPU limits to reduce accidental resource exhaustion.",
        )
      )

    if _image_uses_latest(image):
      findings.append(
        _finding(
          container,
          "unpinned image tag",
          "WARN",
          "Image tag is latest or omitted.",
          "Pin images to explicit versions or immutable digests for reproducible labs.",
        )
      )

  if not findings:
    return [
      Finding(
        name="Docker security baseline",
        status="OK",
        severity="OK",
        summary="No configured Docker findings were detected in running containers.",
        evidence="Inspected running containers with Docker CLI.",
        recommendation="Continue pinning images, limiting privileges, and binding lab ports locally.",
        target="local-docker",
      )
    ]
  return findings
