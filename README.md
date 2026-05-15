# AI Security Lab

A Python-first, clickable, local-only AI infrastructure security lab for defensive learning.

The goal is to practice the workflow behind high-quality AI infrastructure vulnerability research:
safe validation, detection engineering, clear reporting, responsible disclosure drafting, and hardening.

## Safety Boundaries

- Use this lab only on your personal device or an explicitly authorized lab host.
- Scanners default to `127.0.0.1`, `localhost`, and `::1`.
- Public IP ranges and domains are blocked by default.
- Private lab networks are blocked unless explicitly enabled by configuration.
- CIDR ranges larger than four addresses are rejected.
- The lab does not send prompts, pull models, delete models, steal credentials, or run destructive commands.
- Mock services are harmless local services for practicing detection and reporting.

## Requirements

- Python 3.11+
- Docker Compose for optional mock services
- A shell that can run `python`, `pytest`, `ruff`, and `docker compose`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run App

```bash
streamlit run app/ui.py
```

## Run Mock Lab

```bash
docker compose up -d
```

The mock services bind only to loopback:

- Mock Ollama: `http://127.0.0.1:11434`
- Mock vLLM: `http://127.0.0.1:8000`
- Mock Open WebUI: `http://127.0.0.1:8080`
- Insecure Nginx example: `http://127.0.0.1:8081`
- Hardened Nginx example: `http://127.0.0.1:8082`

## Stop Mock Lab

```bash
docker compose down
```

## Run Tests

```bash
pytest
ruff check .
```

## Project Structure

```text
AI-Security-Lab/
  app/                 Streamlit UI, FastAPI API, database, reports
  app/pages/           Clickable lab pages
  scanners/            Local-only safety guard and scanners
  checks/checkmk/      Safe Checkmk local checks
  lab_services/        Harmless mock services and Nginx examples
  reports/templates/   Report and disclosure templates
  reports/generated/   Generated local reports
  docs/                Practical lab documentation
  tests/               pytest coverage
```

## Suggested Next Steps

1. Run the app and review the dashboard.
2. Start the mock lab with Docker Compose.
3. Run local service discovery and runtime exposure checks.
4. Generate Markdown and JSON reports.
5. Draft a responsible disclosure-style advisory from a local mock finding.
6. Study real AI infrastructure CVEs separately and add verified notes to the casebook.
7. Turn hardening ideas into small, well-documented defensive pull requests.

## Local Defensive Testing Disclaimer

This project is for local defensive testing only. Do not use it against public systems,
third-party networks, or any target outside your authorization.
