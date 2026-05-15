# Secure Local LLM Baseline

Use this baseline when running local AI services for learning.

## Network

- Bind runtime APIs to `127.0.0.1` by default.
- Avoid `0.0.0.0` unless a private, authorized lab requires it.
- Put authentication and TLS in front of any remote access.
- Use firewall rules or network allowlists for private lab access.

## Runtime APIs

- Require authentication for inference APIs.
- Set request body limits.
- Set rate limits and concurrency limits.
- Document maximum supported request sizes instead of testing limits with stress traffic.

## Web UIs

- Require login.
- Use secure cookies.
- Add security headers through a reverse proxy.
- Prefer HTTPS for any non-local browser access.

## Containers

- Run as non-root.
- Avoid privileged mode and host networking.
- Do not mount the Docker socket into app containers.
- Pin image tags or digests.
- Add CPU and memory limits for lab reliability.
