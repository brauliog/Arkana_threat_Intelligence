# Arkana Threat Intelligence

**Map the attack. Not just the URL.**

Arkana is a phishing intelligence platform that detects, clusters, and tracks phishing campaigns by analyzing infrastructure reuse, page similarity, and domain behavior.

Instead of answering:
> “Is this URL malicious?”

Arkana answers:
> “What campaign is this part of, how is it evolving, and what infrastructure is behind it?”

---

## Why Arkana Exists

Modern phishing detection tools operate at the **indicator level**:
- One URL at a time
- Little context
- No campaign awareness

Attackers don’t operate that way.

They reuse:
- hosting infrastructure
- TLS certificates
- phishing kits
- domain patterns

Arkana is built to model phishing as a **connected system**, not isolated events.

---

## Core Capabilities

### 🔍 URL Intelligence & Enrichment
- DNS resolution
- TLS certificate analysis
- HTTP + HTML extraction
- Domain metadata (age, registrar, entropy)

---

### Campaign Detection Engine (Key Feature)
Arkana groups related phishing assets into campaigns using:

- shared IP / ASN infrastructure  
- HTML template similarity  
- TLS certificate reuse  
- domain naming patterns  

---

### Graph-Based Threat Modeling
Phishing data is stored as a graph:

This enables:
- multi-hop threat discovery
- infrastructure tracing
- hidden domain discovery

---

### Risk Scoring Engine
Each URL is scored based on weighted signals:

- domain age
- URL entropy / obfuscation
- phishing kit similarity
- infrastructure reputation

---

### Campaign Intelligence Reports
Arkana generates analyst-ready reports including:

- campaign summary
- infrastructure overview
- indicators of compromise (IOCs)
- recommended response actions



---
# Current status

Right now the project includes:
- the core Python package layout under `arkana/`
- a `config.py` file powered by `pydantic-settings`
- a root `.env.example` file
- a `pyproject.toml` with runtime, dev, and test dependencies
- a minimal FastAPI app with `/healthz` and `/readyz` endpoints
- Docker and Docker Compose setup for local API, PostgreSQL, and test runs
- test folders for `unit`, `integration`, and `fixtures`

Still in progress:
- database models, migrations, and repository wiring
- enrichment, scoring, and campaign detection logic
- CI workflow (GitHub Actions)

## Getting started

This section is written for a new developer joining the project for the first time.

### 1. Install the tools you need

Make sure you have the following installed on your machine:
- Python 3.12
- `pip`
- Git
- a terminal such as Terminal, iTerm, or VS Code terminal

You can check your Python version with:

```bash
python --version
```

If your system uses `python3` instead of `python`, run:

```bash
python3 --version
```

### 2. Clone the repository

Clone the project and move into the project folder:

```bash
git clone <REPO_URL>
cd <REPO_FOLDER>
```

Replace `<REPO_URL>` with the actual Git URL and `<REPO_FOLDER>` with the folder name created by Git.

### 3. Create a virtual environment

A virtual environment keeps this project's Python packages separate from the rest of your computer.

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

If your machine uses `python3`, use:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

When the environment is active, you should usually see `(.venv)` at the beginning of your terminal prompt.

### 4. Install the project dependencies

Install the project in editable mode so local code changes are picked up immediately:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

If that finishes without errors, the local package is installed correctly.

### 5. Create your local environment file

Copy the example environment file:

```bash
cp .env.example .env
```

For the current scaffold, the default value in `.env` is enough. Later, this file will hold local database and app settings.

### 6. Verify the config loads correctly

Run this command from the project root:

```bash
python -c "from arkana.config import settings; print(settings.database_url)"
```

If everything is working, you should see a PostgreSQL connection string printed in the terminal.

### 7. Review the project layout

The current codebase is organized like this:

```text
arkana/
  api/
  application/
  domain/
  infrastructure/
    db/
  config.py
migrations/
tests/
  unit/
  integration/
  fixtures/
README.md
pyproject.toml
.env.example
```

Use this as a guide for where new code should live:
- `api/` for FastAPI routes and request/response models
- `application/` for orchestration and workflow services
- `domain/` for core business logic
- `infrastructure/` for database and external system adapters
- `tests/unit/` for fast isolated tests
- `tests/integration/` for app and database level tests

### 8. Run a simple smoke check

You can also confirm the package is importable with:

```bash
python -c "import arkana; print('Arkana package imported successfully')"
```

This is not a full test suite, but it gives a new developer a quick confidence check that the scaffold is working.

## Docker workflow

You can run the full local stack with Docker instead of installing Python dependencies directly on your machine.

### Prerequisites

- Docker Desktop or Docker Engine
- Docker Compose v2 (`docker compose`)

### Start Postgres and the API

From the project root:

```bash
docker compose up --build
```

This starts:
- PostgreSQL on port `5432`
- the FastAPI API on port `8000` with hot reload enabled

Verify the health endpoints:

```bash
curl http://localhost:8000/healthz
curl http://localhost:8000/readyz
```

`/healthz` confirms the API process is running. `/readyz` confirms the API can reach PostgreSQL.

### Run tests in a container

```bash
docker compose run --rm test
```

This uses the same image as the API service and runs the pytest suite.

### Rebuild after dependency changes

If you change `pyproject.toml`, rebuild the image before running again:

```bash
docker compose build api
```

The API service bind-mounts your local source code, so Python file changes are picked up automatically via uvicorn reload. Dependency changes require a rebuild.

## Common problems

### `ModuleNotFoundError: No module named 'arkana'`

Make sure:
- you are inside the project root
- your virtual environment is activated
- you ran `python -m pip install -e .`

### `No module named pydantic_settings`

This usually means dependencies were not installed in the active virtual environment. Run:

```bash
python -m pip install -e .
```

### Wrong Python version

If the project behaves strangely, confirm you are using Python 3.12:

```bash
python --version
```

## Next developer tasks

The next planned build steps are:
- add Alembic migrations and database models under `infrastructure/db/`
- wire repository and session management for PostgreSQL
- add GitHub Actions CI workflow (build image + run pytest)
- begin URL enrichment and campaign detection services

## Contributing

Until the contribution workflow is fully documented, keep changes small and focused:
- create one branch per task
- keep commits readable and specific
- avoid moving folders unless the ticket requires it
- place new code in the correct module from the start