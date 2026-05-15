"""Target safety guard for every scanner in the lab."""

from __future__ import annotations

import ipaddress
from dataclasses import dataclass
from urllib.parse import urlparse

LOCALHOST_NAMES = {"localhost"}
LOOPBACK_IPS = {
  ipaddress.ip_address("127.0.0.1"),
  ipaddress.ip_address("::1"),
}
PRIVATE_LAB_NETWORKS = tuple(
  ipaddress.ip_network(item)
  for item in (
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
    "fc00::/7",
  )
)
MAX_CIDR_ADDRESSES = 4


@dataclass(slots=True)
class SafetyDecision:
  """Explains whether a target is allowed and why."""

  allowed: bool
  reason: str
  normalized_target: str = ""


def extract_host(target: str) -> str:
  """Extract a host from a URL, bracketed IPv6 address, host:port, or raw host."""
  value = target.strip()
  if not value:
    return ""

  if value.startswith("[") and "]" in value:
    return value[1 : value.index("]")].lower()

  try:
    ipaddress.ip_address(value)
    return value.lower()
  except ValueError:
    pass

  if "/" in value and "://" not in value:
    try:
      ipaddress.ip_network(value, strict=False)
      return value.lower()
    except ValueError:
      pass

  parsed = urlparse(value if "://" in value else f"//{value}")
  host = parsed.hostname
  if host:
    return host.strip().lower()

  return value.strip("[]").split(":")[0].lower()


def is_loopback_host(host: str) -> bool:
  """Return true for the explicitly allowed local loopback targets."""
  normalized = host.strip().lower()
  if normalized in LOCALHOST_NAMES:
    return True

  try:
    return ipaddress.ip_address(normalized) in LOOPBACK_IPS
  except ValueError:
    return False


def _is_private_lab_address(address: ipaddress._BaseAddress) -> bool:
  """Return true when an address belongs to approved private lab ranges."""
  return any(address in network for network in PRIVATE_LAB_NETWORKS)


def _is_private_lab_network(network: ipaddress._BaseNetwork) -> bool:
  """Return true when a CIDR is fully inside approved private lab ranges."""
  return any(network.subnet_of(allowed) for allowed in PRIVATE_LAB_NETWORKS)


def validate_target(
  target: str,
  *,
  allow_private_networks: bool = False,
  allow_domains: bool = False,
) -> SafetyDecision:
  """Validate that a scanner target stays inside the local defensive lab scope."""
  host = extract_host(target)
  if not host:
    return SafetyDecision(False, "Empty targets are not allowed.")

  if "/" in host:
    try:
      network = ipaddress.ip_network(host, strict=False)
    except ValueError:
      return SafetyDecision(False, "Invalid CIDR notation.")

    if network.num_addresses > MAX_CIDR_ADDRESSES:
      return SafetyDecision(False, "CIDR ranges larger than four addresses are blocked.")
    if network.is_loopback:
      return SafetyDecision(True, "Loopback CIDR is allowed.", str(network))
    if allow_private_networks and _is_private_lab_network(network):
      return SafetyDecision(True, "Private lab CIDR is explicitly allowed.", str(network))
    return SafetyDecision(False, "CIDR target is outside the allowed local lab scope.")

  if host in LOCALHOST_NAMES:
    return SafetyDecision(True, "localhost is allowed.", host)

  try:
    address = ipaddress.ip_address(host)
  except ValueError:
    if allow_domains:
      return SafetyDecision(False, "Domain resolution is disabled for scanner safety.")
    return SafetyDecision(False, "Domains are blocked by default.")

  if address in LOOPBACK_IPS:
    return SafetyDecision(True, "Loopback IP is allowed.", str(address))
  if allow_private_networks and _is_private_lab_address(address):
    return SafetyDecision(True, "Private lab IP is explicitly allowed.", str(address))

  return SafetyDecision(False, "Public, unspecified, multicast, and non-lab targets are blocked.")


def ensure_safe_target(
  target: str,
  *,
  allow_private_networks: bool = False,
  allow_domains: bool = False,
) -> str:
  """Return the normalized target or raise ValueError when the target is unsafe."""
  decision = validate_target(
    target,
    allow_private_networks=allow_private_networks,
    allow_domains=allow_domains,
  )
  if not decision.allowed:
    raise ValueError(decision.reason)
  return decision.normalized_target
