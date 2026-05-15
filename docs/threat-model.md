# Threat Model

## Assets

- Local AI runtime APIs
- Local model management UIs
- Reverse proxy configuration
- Local Docker container configuration
- Generated reports and advisory drafts

## Trust boundaries

- Browser to Streamlit UI
- Streamlit UI to local scanners
- Scanners to loopback services
- Docker CLI read-only metadata access
- Static config review of bundled Nginx files

## In-scope risks

- AI runtime API reachable without authentication
- UI missing basic browser security headers
- Local reverse proxy missing request limits, timeouts, headers, or auth notes
- Containers running with excessive privileges
- Reports missing enough evidence to support remediation

## Out-of-scope activity

- Public target scanning
- Internet-wide enumeration
- Prompt-based abuse testing
- Credential theft
- Destructive validation
- Load or denial-of-service testing
