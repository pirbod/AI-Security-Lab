# Setup

## Create a Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Start the clickable UI

```bash
streamlit run app/ui.py
```

## Optional mock services

```bash
docker compose up -d
```

The Compose file binds service ports to `127.0.0.1` so checks stay on the local machine.

## Stop mock services

```bash
docker compose down
```

## Validate the project

```bash
pytest
ruff check .
```
