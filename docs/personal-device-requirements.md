# Personal Device Requirements

## Recommended baseline

- Python 3.11 or newer
- 4 CPU cores
- 8 GB RAM
- 10 GB free disk space
- Docker Desktop or Docker Engine for optional mock services

## Network posture

- Run the lab on a trusted personal network.
- Keep mock service ports bound to loopback.
- Do not expose lab ports through port forwarding, tunnels, or public reverse proxies.

## Data handling

- Keep reports under `reports/generated/`.
- Do not paste real secrets into advisory drafts or casebook notes.
- Remove sensitive local paths before sharing reports.
