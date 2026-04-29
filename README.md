# TGPM Backend

Python/Flask/Connexion service that exposes geopolitical event data fetched from Wikidata SPARQL via a REST API defined by the [TGPM OpenAPI specification](https://github.com/TempoGeoPoliticalMap/tgpm-openapi).

---

## Prerequisites

- Python 3.13
- [pipenv](https://pipenv.pypa.io/en/latest/) (`pip install pipenv`)
- Node.js + Java 11+ (for `openapi-generator-cli` — only needed when regenerating models)

---

## Local setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd tgpm-backend-py-flask

# 2. Install all dependencies and activate pre-commit hooks
make setup
```

`make setup` is the single onboarding command. It installs both runtime and dev dependencies and registers the pre-commit hooks. **Do not skip it** — without the hooks, secrets and formatting issues will not be caught before commit.

---

## Running locally

```bash
make run
```

The server starts on `http://localhost:8080`. Swagger UI is at `http://localhost:8080/ui` (also accessible at `/swagger`). The OpenAPI spec is available at `http://localhost:8080/openapi.json`.

---

## Running tests

```bash
make test              # all tests (unit + integration)
make test-unit         # unit tests only (fast, no network)
make test-integration  # integration tests only (full HTTP stack, storage mocked)
```

No test makes a real network call to Wikidata or any external service.

---

## Regenerating server models

Server models are auto-generated from the remote OpenAPI spec. The pinned spec commit SHA is in `scripts/openapi.sh`.

```bash
make openapi
```

**Never edit files inside `src/main/@generated/` by hand.** They are overwritten entirely on every `openapi.sh` run.

---

## Pre-commit hooks

The following hooks run automatically on every `git commit`:

| Hook | Purpose |
|---|---|
| **gitleaks** | Scans staged files for secrets — blocks the commit if any are found |
| **ruff** | Linting with auto-fix (replaces flake8 + isort); excludes `@generated` |
| **black** | Code formatting; excludes `@generated` |
| **mypy** | Static type checking; excludes `@generated` |
| **pipenv requirements export** | Regenerates `requirements.txt` from `Pipfile.lock` and stages it |

If a hook fails, fix the reported issue and retry the commit. **Do not bypass hooks with `--no-verify`**.

---

## requirements.txt

`requirements.txt` is **auto-generated** by the pre-commit hook from `Pipfile.lock`. Do not edit it manually — your changes will be overwritten on the next commit.

It exists for compatibility with external tools (Dependabot, Docker) that expect a `requirements.txt`. The canonical source of truth for dependencies is `Pipfile` and `Pipfile.lock`.

**To add a dependency:**

```bash
pipenv install <package>        # runtime dependency
pipenv install --dev <package>  # development-only dependency
# Commit Pipfile and Pipfile.lock — requirements.txt regenerates automatically on next commit
```

---

## Other useful commands

```bash
make lint       # run ruff linter (reports issues, no file changes)
make format     # auto-format with ruff + black
make typecheck  # run mypy static analysis
make openapi    # regenerate src/main/@generated/ from the remote spec
```

---

## Architecture and AI agent guide

See [`AGENTS.md`](AGENTS.md) for the complete technical reference and onboarding guide.
